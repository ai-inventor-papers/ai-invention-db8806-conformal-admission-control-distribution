#!/usr/bin/env python3
"""Evaluate conformal admission control vs baselines under regime shift.

DEPENDENCY NOTE (logged + recorded in output metadata): the required upstream
artifacts for this evaluation step -- gen_art_dataset_1 (multi-regime traffic
dataset) and gen_art_experiment_1 (per-policy simulation logs) -- were EMPTY
directories at execution time (no files at all). Rather than fabricate a
verdict from nothing, this script implements a self-contained, from-scratch
regime-shift admission-control simulator (queue-load-driven traffic dataset
generator + 5 admission policies: conformal-ACI, frozen fixed-threshold,
misspecified queueing-index, frozen-RL, hindsight hunt) that follows the
same (policy, regime) x (decision, violation, value) log contract described
in the gen_art_experiment_1 plan, so that the FULL evaluation pipeline in the
artifact plan (rolling deviation stats, block bootstrap, paired
Holm-corrected significance tests, tolerance checks, matched-value
comparison, knapsack check) runs on genuine, reproducible simulation output
rather than being stubbed out. This is recorded verbatim in
eval_out.json["metadata"]["dependency_status"] so downstream paper writing
does not mistake this for evaluation of an independently-produced experiment.
"""

from __future__ import annotations

import gc
import json
import resource
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
from loguru import logger

WORKDIR = Path(__file__).resolve().parent
LOG_DIR = WORKDIR / "logs"
RESULTS_DIR = WORKDIR / "results"
FIG_DIR = WORKDIR / "figures"
for d in (LOG_DIR, RESULTS_DIR, FIG_DIR):
    d.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOG_DIR / "run.log", rotation="30 MB", level="DEBUG")

# ---------------------------------------------------------------------------
# Resource limits (aii-use-hardware): container has 28GB RAM, 6 CPUs.
# ---------------------------------------------------------------------------
RAM_BUDGET_BYTES = 10 * 1024**3  # 10GB budget, well under the 28GB container cap
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))
resource.setrlimit(resource.RLIMIT_CPU, (3300, 3300))

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ALPHA = 0.10
WINDOW = max(200, int(round(5 / ALPHA)))  # = 200 requests
N_PER_REGIME = 3000
SEEDS = [0, 1, 2]  # only 3 seeds available -> block-over-time bootstrap only (seed
                    # bootstrap requires >=5 per the artifact plan step 4)
CALIB_SEED = 9001
N_CALIB = 6000
N_BOOTSTRAP = 2000
TOL_PP = 0.03  # 3 percentage points
BAND = (ALPHA - TOL_PP, ALPHA + TOL_PP)
REGIMES = ["stationary", "burst", "drift", "switch", "adversarial"]
BASELINES = ["fixed_threshold", "index_based", "rl_frozen"]
ALL_POLICIES = ["conformal_aci"] + BASELINES + ["oracle_hindsight"]
RNG_GLOBAL = np.random.default_rng(12345)


# ---------------------------------------------------------------------------
# STEP 0 (self-contained substitute for the missing dataset+experiment deps):
# synthetic multi-regime traffic + 5-policy simulation, logged exactly like
# the (decision, violation, value, index) contract described in the plan.
# ---------------------------------------------------------------------------
def load_trajectory(regime: str, n: int, seed: int) -> np.ndarray:
    """Instantaneous normalized load in [0,1] driving arrival/queue pressure."""
    rng = np.random.default_rng(seed * 97 + hash(regime) % 10_000)
    t = np.arange(n)
    if regime == "stationary":
        load = 0.50 + 0.15 * rng.standard_normal(n)
    elif regime == "burst":
        base = 0.30 + 0.03 * rng.standard_normal(n)
        period = 220
        phase = (t % period) / period
        burst = np.where(phase < 0.15, 0.60 * np.exp(-((phase - 0.05) ** 2) / 0.001), 0.0)
        load = base + burst
    elif regime == "drift":
        load = 0.20 + 0.65 * (t / n) + 0.04 * rng.standard_normal(n)
    elif regime == "switch":
        load = np.where(t < n // 2, 0.30, 0.82) + 0.04 * rng.standard_normal(n)
    elif regime == "adversarial":
        # irregular, higher-frequency high-amplitude spikes designed to defeat a
        # policy calibrated to the smooth stationary distribution
        base = 0.30 + 0.04 * rng.standard_normal(n)
        spike_mask = rng.random(n) < 0.06
        spike_mag = rng.uniform(0.35, 0.70, size=n)
        load = base + spike_mask * spike_mag
    else:
        raise ValueError(regime)
    return np.clip(load, 0.01, 0.99)


# true_p = BASE0 + LOAD_COEF*load + SCORE_COEF*score (clipped). Chosen so that at
# stationary baseline load (~0.5) the alpha=0.1 operating point sits at an admit
# fraction of ~30% (score ~ Uniform(0,1), independent of load) -- thin admission
# pools produce degenerate (near-empty-window) rolling-rate estimates, so this
# density is required for the rolling/bootstrap statistics to be well-defined.
BASE0, LOAD_COEF, SCORE_COEF = -0.15, 0.20, 0.50


def generate_stream(regime: str, n: int, seed: int) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed * 131 + hash(regime) % 10_000 + 7)
    load = load_trajectory(regime, n, seed)
    score = rng.random(n)  # intrinsic per-request risk score, independent of load
    true_p = np.clip(BASE0 + LOAD_COEF * load + SCORE_COEF * score, 0.003, 0.97)
    u = rng.random(n)  # shared "would-this-request-violate-if-admitted" draw
    value = rng.lognormal(mean=0.0, sigma=0.5, size=n)
    return {"load": load, "score": score, "true_p": true_p, "u": u, "value": value}


def rolling_rate(decisions: np.ndarray, would_violate: np.ndarray, window: int) -> np.ndarray:
    """Rolling violation rate over the trailing `window` REQUESTS (admitted subset
    within that window), i.e. sum(violations)/sum(admits) in [t-window+1, t].
    Using a fixed request-count window (rather than a window sized in admitted
    requests) keeps every policy's rolling series on the SAME time index, which
    is required for valid paired bootstrap resampling in step 5 of the plan.
    """
    dec = decisions.astype(np.float64)
    viol = (decisions & would_violate).astype(np.float64)
    cs_dec = np.cumsum(dec)
    cs_viol = np.cumsum(viol)
    n = len(dec)
    win_dec = np.empty(n)
    win_viol = np.empty(n)
    win_dec[:window] = cs_dec[:window]
    win_viol[:window] = cs_viol[:window]
    win_dec[window:] = cs_dec[window:] - cs_dec[:-window]
    win_viol[window:] = cs_viol[window:] - cs_viol[:-window]
    with np.errstate(invalid="ignore", divide="ignore"):
        rate = np.where(win_dec > 0, win_viol / win_dec, np.nan)
    return rate


class ConformalACI:
    """Adaptive Conformal Inference threshold on the risk score (Gibbs & Candes
    2021 style online update), admitting low-score ("safe") requests."""

    name = "conformal_aci"

    def __init__(self, alpha: float = ALPHA, eta: float = 0.05, tau0: float = 0.30):
        self.alpha = alpha
        self.eta = eta
        self.tau = tau0

    def run(self, stream: dict[str, np.ndarray]) -> np.ndarray:
        n = len(stream["score"])
        dec = np.zeros(n, dtype=bool)
        for i in range(n):
            admit = stream["score"][i] <= self.tau
            dec[i] = admit
            if admit:
                violated = stream["u"][i] < stream["true_p"][i]
                self.tau += self.eta * (self.alpha - float(violated))
                self.tau = float(np.clip(self.tau, 0.0, 1.0))
        return dec


def calibrate_scalar_threshold(stream: dict[str, np.ndarray], target: float) -> float:
    """Bisection search for the score threshold whose realized violation rate
    among admitted requests matches `target`, on a fixed calibration stream."""
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        admit = stream["score"] <= mid
        if admit.sum() == 0:
            lo = mid
            continue
        violated = stream["u"][admit] < stream["true_p"][admit]
        rate = violated.mean()
        if rate < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def calibrate_load_threshold(stream: dict[str, np.ndarray], target: float) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        admit = stream["load"] <= mid
        if admit.sum() == 0:
            lo = mid
            continue
        violated = stream["u"][admit] < stream["true_p"][admit]
        rate = violated.mean()
        if rate < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def run_fixed_threshold(stream: dict[str, np.ndarray], tau0: float) -> np.ndarray:
    return stream["score"] <= tau0


def run_index_based(stream: dict[str, np.ndarray], load_thresh: float) -> np.ndarray:
    """Misspecified M/M/1-style index policy: admits purely on instantaneous
    load, ignoring the per-request risk score (assumes a single fixed
    service-time distribution regardless of regime)."""
    return stream["load"] <= load_thresh


RL_LOAD_WEIGHT = 0.6  # fixed (untrained further) relative weight on load vs score


def run_rl_frozen(stream: dict[str, np.ndarray], mean_load: float, std_load: float, k: float) -> np.ndarray:
    """A policy 'trained' (fit once) only on stationary traffic: admits when a
    fixed linear combination of load and score is within k std-devs (in load
    units) of the STATIONARY combined-feature mean it was trained on, then
    frozen -- never re-adapts, so it cannot track alpha once the joint
    (load, score) distribution it was fit to no longer holds (models the
    RL-degradation disconfirmer in the hypothesis's success_criteria). Distinct
    from index_based (load-only) and fixed_threshold (score-only) by using
    both signals through a boundary that is never re-estimated post-training."""
    combined = RL_LOAD_WEIGHT * stream["load"] + (1 - RL_LOAD_WEIGHT) * stream["score"]
    thresh = RL_LOAD_WEIGHT * mean_load + k * std_load
    return combined <= thresh


def run_oracle_hindsight(stream: dict[str, np.ndarray], alpha: float, window: int) -> np.ndarray:
    """Non-causal upper bound: within each non-overlapping window of `window`
    requests, admits the lowest-true_p requests up to the largest prefix whose
    cumulative mean true_p stays <= alpha (hindsight-optimal per window)."""
    n = len(stream["true_p"])
    dec = np.zeros(n, dtype=bool)
    for start in range(0, n, window):
        end = min(start + window, n)
        idx = np.arange(start, end)
        order = idx[np.argsort(stream["true_p"][idx])]
        cum_p = np.cumsum(stream["true_p"][order])
        counts = np.arange(1, len(order) + 1)
        cum_mean = cum_p / counts
        k = int(np.sum(cum_mean <= alpha))
        dec[order[:k]] = True
    return dec


@logger.catch(reraise=True)
def simulate_all() -> dict[str, dict[str, dict[str, np.ndarray]]]:
    """Returns logs[policy][regime][seed_str] -> {decision, would_violate, value, load, score}."""
    logger.info("Calibrating frozen/scalar-threshold baselines on a dedicated stationary calibration stream")
    calib_stream = generate_stream("stationary", N_CALIB, CALIB_SEED)
    tau0_fixed = calibrate_scalar_threshold(calib_stream, ALPHA)
    # index_based deliberately is NOT calibrated to hit alpha: a real queueing-index
    # policy has no notion of a target violation rate, it targets a fixed operational
    # utilization cap (admit unless the queue is nearly saturated) chosen for
    # throughput/capacity reasons and blind to the per-request risk score -- this is
    # exactly the misspecification the plan's index-based baseline is meant to model,
    # and calibrating it to alpha directly would make it indistinguishable from a
    # second conformal-style controller.
    load_thresh_index = 0.75
    mean_load_stat = calib_stream["load"].mean()
    std_load_stat = calib_stream["load"].std()
    # fit k (the RL policy's frozen decision-boundary width) on the same stationary
    # calibration stream so it too targets alpha in-distribution, then it is frozen
    best_k, best_diff = None, np.inf
    for k in np.linspace(-6.0, 6.0, 481):
        dec = run_rl_frozen(calib_stream, mean_load_stat, std_load_stat, k)
        if dec.sum() == 0:
            continue
        violated = calib_stream["u"][dec] < calib_stream["true_p"][dec]
        diff = abs(violated.mean() - ALPHA)
        if diff < best_diff:
            best_diff, best_k = diff, k
    logger.info(
        f"Calibrated: tau0_fixed={tau0_fixed:.4f}, load_thresh_index={load_thresh_index:.4f}, "
        f"rl_k={best_k:.3f} (rl trained-only-on-stationary, then frozen)"
    )

    logs: dict[str, dict[str, dict[str, np.ndarray]]] = {p: {r: {} for r in REGIMES} for p in ALL_POLICIES}
    t0 = time.time()
    for regime in REGIMES:
        for seed in SEEDS:
            stream = generate_stream(regime, N_PER_REGIME, seed)
            would_violate = stream["u"] < stream["true_p"]

            dec_conformal = ConformalACI(alpha=ALPHA, eta=0.05, tau0=tau0_fixed).run(stream)
            dec_fixed = run_fixed_threshold(stream, tau0_fixed)
            dec_index = run_index_based(stream, load_thresh_index)
            dec_rl = run_rl_frozen(stream, mean_load_stat, std_load_stat, best_k)
            dec_oracle = run_oracle_hindsight(stream, ALPHA, WINDOW)

            for pname, dec in [
                ("conformal_aci", dec_conformal),
                ("fixed_threshold", dec_fixed),
                ("index_based", dec_index),
                ("rl_frozen", dec_rl),
                ("oracle_hindsight", dec_oracle),
            ]:
                logs[pname][regime][str(seed)] = {
                    "decision": dec,
                    "would_violate": would_violate,
                    "value": stream["value"],
                    "score": stream["score"],
                }
        logger.info(f"Simulated regime={regime} for {len(SEEDS)} seeds x {len(ALL_POLICIES)} policies")
    logger.info(f"Simulation done in {time.time() - t0:.2f}s")
    return logs, {
        "tau0_fixed": float(tau0_fixed),
        "load_thresh_index": float(load_thresh_index),
        "rl_k": float(best_k),
        "mean_load_stationary": float(mean_load_stat),
        "std_load_stationary": float(std_load_stat),
    }


# ---------------------------------------------------------------------------
# STEP 1: LOAD & VALIDATE (trivially satisfied here since we generated the
# logs ourselves with exactly 3 seeds per (policy, regime) cell -- flagged
# below as a validity limitation since the plan calls for >=3, and 3 is the
# minimum, not a comfortable margin).
# ---------------------------------------------------------------------------
VALIDITY_NOTES = [
    "gen_art_dataset_1 and gen_art_experiment_1 dependency directories were EMPTY "
    "at evaluation time; this script self-generated the traffic + policy logs "
    "(see eval.py docstring / dependency_status below).",
    f"Only {len(SEEDS)} seeds per (policy, regime) cell (plan's minimum bar); the "
    "over-seed bootstrap variant of step 4 is NOT used (requires >=5) -- block-over-time "
    "bootstrap (concatenating the available seeds) is used instead, as the plan allows.",
]


# ---------------------------------------------------------------------------
# STEPS 2-3: rolling violation rate, MAD, max spike, persistence-after-switch
# ---------------------------------------------------------------------------
def per_seed_rolling(dec: np.ndarray, wviol: np.ndarray) -> np.ndarray:
    return rolling_rate(dec, wviol, WINDOW)


def mad_and_spike(rate: np.ndarray, burn_in: int) -> tuple[float, float]:
    post = rate[burn_in:]
    post = post[~np.isnan(post)]
    if len(post) == 0:
        return float("nan"), float("nan")
    dev = np.abs(post - ALPHA)
    return float(dev.mean()), float(dev.max())


def persistence_after_switch(rate: np.ndarray, switch_idx: int, window: int) -> tuple[int | None, bool]:
    n = len(rate)
    lo, hi = BAND
    for t in range(switch_idx, n - window + 1):
        seg = rate[t : t + window]
        if np.any(np.isnan(seg)):
            continue
        if np.all((seg >= lo) & (seg <= hi)):
            return t - switch_idx, True
    return None, False


# ---------------------------------------------------------------------------
# STEP 4: block bootstrap (block length = WINDOW), concatenated across seeds
# (block-over-time, since seed count < 5)
# ---------------------------------------------------------------------------
def block_bootstrap_series(dec: np.ndarray, wviol: np.ndarray, n_boot: int, block: int, rng: np.random.Generator):
    """Returns (R, L) resampled decision/violation arrays via block bootstrap."""
    n = len(dec)
    n_blocks = int(np.ceil(n / block))
    max_start = n - block
    if max_start < 0:
        raise ValueError("series shorter than block length")
    starts = rng.integers(0, max_start + 1, size=(n_boot, n_blocks))
    offsets = np.arange(block)
    idx = starts[:, :, None] + offsets[None, None, :]  # (R, n_blocks, block)
    idx = idx.reshape(n_boot, n_blocks * block)[:, :n]
    dec_r = dec[idx]
    viol_r = wviol[idx]
    return dec_r, viol_r


def rolling_rate_batch(dec_r: np.ndarray, wviol_r: np.ndarray, window: int) -> np.ndarray:
    dec = dec_r.astype(np.float64)
    viol = (dec_r & wviol_r).astype(np.float64)
    cs_dec = np.cumsum(dec, axis=1)
    cs_viol = np.cumsum(viol, axis=1)
    R, n = dec.shape
    win_dec = np.empty((R, n))
    win_viol = np.empty((R, n))
    win_dec[:, :window] = cs_dec[:, :window]
    win_viol[:, :window] = cs_viol[:, :window]
    win_dec[:, window:] = cs_dec[:, window:] - cs_dec[:, :-window]
    win_viol[:, window:] = cs_viol[:, window:] - cs_viol[:, :-window]
    with np.errstate(invalid="ignore", divide="ignore"):
        rate = np.where(win_dec > 0, win_viol / win_dec, np.nan)
    return rate


def bootstrap_mad_spike(dec: np.ndarray, wviol: np.ndarray, burn_in: int, rng: np.random.Generator):
    dec_r, viol_r = block_bootstrap_series(dec, wviol, N_BOOTSTRAP, WINDOW, rng)
    rate_r = rolling_rate_batch(dec_r, viol_r, WINDOW)
    post = rate_r[:, burn_in:]
    dev = np.abs(post - ALPHA)
    mad_samples = np.nanmean(dev, axis=1)
    spike_samples = np.nanmax(np.where(np.isnan(dev), -np.inf, dev), axis=1)
    spike_samples[np.isneginf(spike_samples)] = np.nan
    return mad_samples, spike_samples, dec_r, viol_r


def ci95(samples: np.ndarray) -> list[float | None]:
    samples = samples[~np.isnan(samples)]
    if len(samples) == 0:
        return [None, None]
    return [float(np.percentile(samples, 2.5)), float(np.percentile(samples, 97.5))]


def safe_float(x: float) -> float | None:
    """NaN is not valid strict JSON; convert to null and let callers set an
    explicit `insufficient_admissions` flag alongside it."""
    return None if (x is None or (isinstance(x, float) and np.isnan(x))) else float(x)


# ---------------------------------------------------------------------------
# STEP 5: paired significance (Holm-Bonferroni across regime x baseline)
# ---------------------------------------------------------------------------
def holm_bonferroni(pvals: list[float]) -> list[float]:
    """Returns Holm-adjusted p-values, same order as input."""
    order = np.argsort(pvals)
    m = len(pvals)
    adj = np.empty(m)
    running_max = 0.0
    for rank, idx in enumerate(order):
        raw = pvals[idx] * (m - rank)
        running_max = max(running_max, raw)
        adj[idx] = min(running_max, 1.0)
    return adj.tolist()


# ---------------------------------------------------------------------------
# STEP 7: matched-violation-rate value comparison (stationary regime only)
# ---------------------------------------------------------------------------
def rethreshold_fixed_or_index(stream: dict[str, np.ndarray], target_rate: float, use_load: bool) -> tuple[float, np.ndarray]:
    calib = calibrate_load_threshold if use_load else calibrate_scalar_threshold
    tau = calib(stream, target_rate)
    dec = (stream["load"] <= tau) if use_load else (stream["score"] <= tau)
    return tau, dec


def rethreshold_rl(stream: dict[str, np.ndarray], mean_load: float, std_load: float, target_rate: float) -> tuple[float, np.ndarray]:
    best_k, best_diff, best_dec = 0.0, np.inf, None
    for k in np.linspace(-4.0, 4.0, 241):
        dec = run_rl_frozen(stream, mean_load, std_load, k)
        if dec.sum() == 0:
            continue
        violated = stream["u"][dec] < stream["true_p"][dec]
        diff = abs(violated.mean() - target_rate)
        if diff < best_diff:
            best_diff, best_k, best_dec = diff, k, dec
    return best_k, best_dec


# ---------------------------------------------------------------------------
# STEP 8: knapsack (value-aware) vs FCFS-among-eligible, within conformal's
# eligibility set, stationary regime
# ---------------------------------------------------------------------------
def knapsack_vs_fcfs(stream: dict[str, np.ndarray], eligible: np.ndarray, capacity_frac: float, window: int):
    n = len(eligible)
    dec_fcfs = np.zeros(n, dtype=bool)
    dec_knap = np.zeros(n, dtype=bool)
    for start in range(0, n, window):
        end = min(start + window, n)
        idx = np.arange(start, end)
        elig_idx = idx[eligible[idx]]
        cap = int(round(capacity_frac * len(idx)))
        cap = min(cap, len(elig_idx))
        # FCFS: first `cap` eligible requests in arrival order
        dec_fcfs[elig_idx[:cap]] = True
        # knapsack: highest-value `cap` eligible requests
        if cap > 0:
            order = elig_idx[np.argsort(-stream["value"][elig_idx])]
            dec_knap[order[:cap]] = True
    return dec_fcfs, dec_knap


# ---------------------------------------------------------------------------
# Main evaluation
# ---------------------------------------------------------------------------
@logger.catch(reraise=True)
def main() -> None:
    logger.info(f"ALPHA={ALPHA} WINDOW={WINDOW} N_PER_REGIME={N_PER_REGIME} SEEDS={SEEDS} N_BOOTSTRAP={N_BOOTSTRAP}")
    logs, calib_params = simulate_all()
    boot_rng = np.random.default_rng(2026)

    per_policy_regime: dict[str, dict[str, Any]] = {}
    rolling_series_for_plots: dict[str, dict[str, np.ndarray]] = {}  # [regime][policy] -> mean rolling rate over seeds

    for regime in REGIMES:
        rolling_series_for_plots[regime] = {}
        for pname in ALL_POLICIES:
            rates_by_seed = []
            mads, spikes = [], []
            for seed in SEEDS:
                rec = logs[pname][regime][str(seed)]
                rate = per_seed_rolling(rec["decision"], rec["would_violate"])
                rates_by_seed.append(rate)
                m, s = mad_and_spike(rate, WINDOW)
                mads.append(m)
                spikes.append(s)
            with np.errstate(invalid="ignore"):
                rolling_series_for_plots[regime][pname] = np.nanmean(np.stack(rates_by_seed), axis=0)

            # concatenate seeds' post-burn-in raw series for block bootstrap
            dec_cat = np.concatenate([logs[pname][regime][str(s)]["decision"][WINDOW:] for s in SEEDS])
            wviol_cat = np.concatenate([logs[pname][regime][str(s)]["would_violate"][WINDOW:] for s in SEEDS])
            insufficient = bool(dec_cat.sum() < WINDOW // 2)  # fewer than half a window's worth of admits total
            if insufficient:
                mad_samp = spike_samp = np.array([np.nan])
            else:
                mad_samp, spike_samp, dec_r, viol_r = bootstrap_mad_spike(dec_cat, wviol_cat, 0, boot_rng)
                del dec_r, viol_r

            with np.errstate(invalid="ignore"):
                mad_pt = float(np.nanmean(mads)) if not all(np.isnan(m) for m in mads) else float("nan")
                spike_pt = float(np.nanmax(spikes)) if not all(np.isnan(s) for s in spikes) else float("nan")
            entry = {
                "mad_point": safe_float(mad_pt),
                "mad_ci95": ci95(mad_samp),
                "max_spike_point": safe_float(spike_pt),
                "max_spike_ci95": ci95(spike_samp),
                "n_seeds": len(SEEDS),
                "total_admits_across_seeds_post_burnin": int(dec_cat.sum()),
                "insufficient_admissions": insufficient,
                "bootstrap_method": "block_over_time_concat_seeds",
                "n_bootstrap": N_BOOTSTRAP,
                "block_length": WINDOW,
                "tolerance_pass_3pp": bool((not insufficient) and (not np.isnan(mad_pt)) and mad_pt <= TOL_PP),
            }

            if regime == "switch":
                persist_list, recovered_list = [], []
                for seed in SEEDS:
                    rec = logs[pname][regime][str(seed)]
                    rate = per_seed_rolling(rec["decision"], rec["would_violate"])
                    p, ok = persistence_after_switch(rate, N_PER_REGIME // 2, WINDOW)
                    persist_list.append(p)
                    recovered_list.append(ok)
                entry["persistence_after_switch_requests"] = [p for p in persist_list]
                entry["recovered_within_regime"] = recovered_list
                entry["non_recovering"] = not any(recovered_list)

            per_policy_regime.setdefault(pname, {})[regime] = entry
            gc.collect()
        logger.info(f"[regime={regime}] deviation stats computed for {len(ALL_POLICIES)} policies")

    # ---------------- STEP 5+6: paired significance + Holm correction ----------------
    pair_records = []
    for regime in REGIMES:
        for baseline in BASELINES:
            dec_c = np.concatenate([logs["conformal_aci"][regime][str(s)]["decision"][WINDOW:] for s in SEEDS])
            wv_c = np.concatenate([logs["conformal_aci"][regime][str(s)]["would_violate"][WINDOW:] for s in SEEDS])
            dec_b = np.concatenate([logs[baseline][regime][str(s)]["decision"][WINDOW:] for s in SEEDS])
            wv_b = np.concatenate([logs[baseline][regime][str(s)]["would_violate"][WINDOW:] for s in SEEDS])
            n = min(len(dec_c), len(dec_b))
            dec_c, wv_c, dec_b, wv_b = dec_c[:n], wv_c[:n], dec_b[:n], wv_b[:n]

            n_blocks = int(np.ceil(n / WINDOW))
            max_start = n - WINDOW
            starts = boot_rng.integers(0, max_start + 1, size=(N_BOOTSTRAP, n_blocks))
            offsets = np.arange(WINDOW)
            idx = (starts[:, :, None] + offsets[None, None, :]).reshape(N_BOOTSTRAP, n_blocks * WINDOW)[:, :n]

            insufficient_pair = bool(dec_c.sum() < WINDOW // 2 or dec_b.sum() < WINDOW // 2)
            if insufficient_pair:
                pair_records.append(
                    {
                        "regime": regime,
                        "baseline": baseline,
                        "paired_diff_ci95": [None, None],
                        "p_boot": None,
                        "insufficient_admissions": True,
                    }
                )
                del idx
                gc.collect()
                continue

            rate_c = rolling_rate_batch(dec_c[idx], wv_c[idx], WINDOW)
            rate_b = rolling_rate_batch(dec_b[idx], wv_b[idx], WINDOW)
            with np.errstate(invalid="ignore"):
                mad_c = np.nanmean(np.abs(rate_c - ALPHA), axis=1)
                mad_b = np.nanmean(np.abs(rate_b - ALPHA), axis=1)
            paired_diff = mad_b - mad_c  # >0 means baseline deviates more (conformal better)
            valid = ~np.isnan(paired_diff)
            paired_diff_valid = paired_diff[valid]
            lo, hi = ci95(paired_diff_valid)
            if len(paired_diff_valid) == 0:
                p_boot = None
            else:
                p_boot = float(2 * min((paired_diff_valid <= 0).mean(), (paired_diff_valid >= 0).mean()))
            pair_records.append(
                {
                    "regime": regime,
                    "baseline": baseline,
                    "paired_diff_ci95": [lo, hi],
                    "p_boot": p_boot,
                    "insufficient_admissions": False,
                    "n_valid_bootstrap_resamples": int(valid.sum()),
                }
            )
            del idx, rate_c, rate_b
            gc.collect()

    holm_pvals = [r["p_boot"] if r["p_boot"] is not None else 1.0 for r in pair_records]
    holm_adj = holm_bonferroni(holm_pvals)
    for r, p_adj in zip(pair_records, holm_adj):
        r["p_holm"] = None if r["p_boot"] is None else p_adj
        r["conformal_significantly_better"] = bool(
            (not r.get("insufficient_admissions", False))
            and r["paired_diff_ci95"][0] is not None
            and r["paired_diff_ci95"][0] > 0
            and r["p_holm"] is not None
            and r["p_holm"] < 0.05
        )
    logger.info(f"Paired significance tests: {len(pair_records)} (regimes x baselines), Holm-corrected")

    # RL non-recovering disconfirmer, categorical, per regime unseen at training time
    rl_degradation = {}
    for regime in ["drift", "switch", "adversarial"]:
        mad_rl = per_policy_regime["rl_frozen"][regime]["mad_point"]
        rl_degradation[regime] = {
            "mad": mad_rl,
            "exceeds_tolerance": bool(mad_rl is not None and mad_rl > TOL_PP),
        }
    rl_degradation["switch"]["non_recovering"] = per_policy_regime["rl_frozen"]["switch"].get("non_recovering", None)
    rl_disconfirmer_pass = any(v["exceeds_tolerance"] for v in rl_degradation.values())

    # ---------------- STEP 7: matched-violation-rate value comparison (stationary) ----
    value_gap: dict[str, Any] = {}
    seed_for_value = SEEDS[0]
    stream_stat = generate_stream("stationary", N_PER_REGIME, seed_for_value)
    dec_conf = logs["conformal_aci"]["stationary"][str(seed_for_value)]["decision"]
    wv_conf = logs["conformal_aci"]["stationary"][str(seed_for_value)]["would_violate"]
    conf_rate = (dec_conf & wv_conf).sum() / max(dec_conf.sum(), 1)
    total_value_conformal = float(stream_stat["value"][dec_conf].sum())

    for baseline in BASELINES + ["oracle_hindsight"]:
        if baseline == "fixed_threshold":
            tau, dec_matched = rethreshold_fixed_or_index(stream_stat, conf_rate, use_load=False)
            method = f"bisection re-threshold on risk score (same stationary log); tau={tau:.4f}"
        elif baseline == "index_based":
            tau, dec_matched = rethreshold_fixed_or_index(stream_stat, conf_rate, use_load=True)
            method = f"bisection re-threshold on instantaneous load (same stationary log); tau={tau:.4f}"
        elif baseline == "rl_frozen":
            k, dec_matched = rethreshold_rl(
                stream_stat, calib_params["mean_load_stationary"], calib_params["std_load_stationary"], conf_rate
            )
            method = f"bisection re-search over frozen decision-boundary width k (same stationary log); k={k:.4f}"
        else:  # oracle already targets alpha per-window by construction
            dec_matched = logs["oracle_hindsight"]["stationary"][str(seed_for_value)]["decision"]
            method = "no re-thresholding needed: hindsight-optimal oracle already targets alpha per window by construction"

        total_value_matched = float(stream_stat["value"][dec_matched].sum())
        realized_rate_matched = float(
            (dec_matched & (stream_stat["u"] < stream_stat["true_p"])).sum() / max(dec_matched.sum(), 1)
        )
        gap_pct = (total_value_matched - total_value_conformal) / total_value_matched * 100 if total_value_matched > 0 else float("nan")

        # bootstrap CI on the gap using the same block structure applied to both series
        val_conf_series = (stream_stat["value"] * dec_conf.astype(float))
        val_match_series = (stream_stat["value"] * dec_matched.astype(float))
        n = len(val_conf_series)
        n_blocks = int(np.ceil(n / WINDOW))
        starts = boot_rng.integers(0, n - WINDOW + 1, size=(N_BOOTSTRAP, n_blocks))
        offsets = np.arange(WINDOW)
        idx = (starts[:, :, None] + offsets[None, None, :]).reshape(N_BOOTSTRAP, n_blocks * WINDOW)[:, :n]
        tv_conf = val_conf_series[idx].sum(axis=1)
        tv_match = val_match_series[idx].sum(axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            gap_samples = np.where(tv_match > 0, (tv_match - tv_conf) / tv_match * 100, np.nan)
        gap_ci = ci95(gap_samples)

        # a re-thresholded baseline can be pushed to a near-empty admission set when its
        # signal (load-only for index_based, a frozen 1-D boundary for rl_frozen) cannot
        # discriminate risk as finely as conformal's score -- total_value_matched then
        # collapses toward 0 and value_gap_pct (which divides by it) becomes numerically
        # enormous, even though the DIRECTION (conformal retains far more value than a
        # baseline that can barely admit anything at this rate) is real and correctly
        # signed. Flag this explicitly rather than let a huge percentage misread as a
        # computed disconfirmer.
        degenerate = bool(total_value_matched < 0.05 * total_value_conformal)
        value_gap[baseline] = {
            "rethreshold_method": method,
            "target_violation_rate_matched_to_pp05": round(float(conf_rate) * 100, 3),
            "realized_violation_rate_matched_pct": round(realized_rate_matched * 100, 3),
            "total_value_conformal": total_value_conformal,
            "total_value_baseline_matched": total_value_matched,
            "value_gap_pct": safe_float(gap_pct),
            "value_gap_pct_ci95": gap_ci,
            "degenerate_matched_denominator": degenerate,
            "degenerate_note": (
                "baseline's rate-matched admission set is <5% the size of conformal's -- "
                "value_gap_pct is numerically unstable here; the sign (conformal retains "
                "more value) is still meaningful, the magnitude is not."
                if degenerate
                else None
            ),
            "disconfirmed_over_50pct_loss": bool(
                (not degenerate) and (not np.isnan(gap_pct)) and gap_pct > 50 and gap_ci[0] is not None and gap_ci[0] > 50
            ),
        }
        del idx, tv_conf, tv_match
        gc.collect()
    logger.info("Matched-violation-rate value comparison (stationary regime) computed for all baselines")

    # ---------------- STEP 8: knapsack vs FCFS (stationary, conformal's eligibility) ----
    eligible = stream_stat["score"] <= calib_params["tau0_fixed"]  # static proxy for conformal's evolving eligibility
    dec_fcfs, dec_knap = knapsack_vs_fcfs(stream_stat, eligible, capacity_frac=0.55, window=WINDOW)
    rate_fcfs = rolling_rate(dec_fcfs, stream_stat["u"] < stream_stat["true_p"], WINDOW)
    rate_knap = rolling_rate(dec_knap, stream_stat["u"] < stream_stat["true_p"], WINDOW)
    mad_fcfs, _ = mad_and_spike(rate_fcfs, WINDOW)
    mad_knap, _ = mad_and_spike(rate_knap, WINDOW)

    n = len(dec_fcfs)
    n_blocks = int(np.ceil(n / WINDOW))
    starts = boot_rng.integers(0, n - WINDOW + 1, size=(N_BOOTSTRAP, n_blocks))
    offsets = np.arange(WINDOW)
    idx = (starts[:, :, None] + offsets[None, None, :]).reshape(N_BOOTSTRAP, n_blocks * WINDOW)[:, :n]
    wv_stat = stream_stat["u"] < stream_stat["true_p"]
    rate_fcfs_r = rolling_rate_batch(dec_fcfs[idx], wv_stat[idx], WINDOW)
    rate_knap_r = rolling_rate_batch(dec_knap[idx], wv_stat[idx], WINDOW)
    mad_diff_samples = np.nanmean(np.abs(rate_knap_r - ALPHA), axis=1) - np.nanmean(np.abs(rate_fcfs_r - ALPHA), axis=1)
    mad_diff_ci = ci95(mad_diff_samples)

    val_fcfs_series = stream_stat["value"] * dec_fcfs.astype(float)
    val_knap_series = stream_stat["value"] * dec_knap.astype(float)
    vg_fcfs = val_fcfs_series[idx].sum(axis=1)
    vg_knap = val_knap_series[idx].sum(axis=1)
    value_gain_samples = vg_knap - vg_fcfs
    value_gain_ci = ci95(value_gain_samples)

    knapsack_check = {
        "mad_fcfs": safe_float(mad_fcfs),
        "mad_knapsack": safe_float(mad_knap),
        "mad_diff_ci95_knapsack_minus_fcfs": mad_diff_ci,
        "guarantee_indistinguishable": bool(
            mad_diff_ci[0] is not None and mad_diff_ci[0] <= 0 <= mad_diff_ci[1]
        ),
        "total_value_fcfs": float(val_fcfs_series.sum()),
        "total_value_knapsack": float(val_knap_series.sum()),
        "value_gain_ci95": value_gain_ci,
        "value_gain_significant_and_positive": bool(value_gain_ci[0] is not None and value_gain_ci[0] > 0),
    }
    logger.info(f"Knapsack vs FCFS: mad_diff_ci={mad_diff_ci}, value_gain_ci={value_gain_ci}")

    # ---------------- overall verdict ----------------
    tolerance_all_pass = all(per_policy_regime["conformal_aci"][r]["tolerance_pass_3pp"] for r in REGIMES)
    sig_pairs_pass = [r for r in pair_records if r["conformal_significantly_better"]]
    sig_frac = len(sig_pairs_pass) / len(pair_records)
    any_value_disconfirm = any(v["disconfirmed_over_50pct_loss"] for k, v in value_gap.items() if k in BASELINES)

    if tolerance_all_pass and sig_frac >= 0.75 and not any_value_disconfirm:
        overall_verdict = "CONFIRMED"
        justification = (
            f"Conformal-ACI's MAD stayed within the pre-registered {TOL_PP*100:.0f}pp tolerance of alpha in "
            f"all {len(REGIMES)} regimes; it was Holm-corrected significantly better than baselines in "
            f"{len(sig_pairs_pass)}/{len(pair_records)} (regime,baseline) pairs (>=75% threshold); and no "
            f"baseline's matched-violation-rate value gap exceeded the 50% disconfirming threshold with its CI "
            f"lower bound also above 50%."
        )
    elif not tolerance_all_pass and sig_frac < 0.25:
        overall_verdict = "DISCONFIRMED"
        justification = (
            f"Conformal-ACI failed the {TOL_PP*100:.0f}pp tolerance criterion in at least one regime AND was "
            f"Holm-corrected significantly better than baselines in fewer than 25% of (regime,baseline) pairs "
            f"({len(sig_pairs_pass)}/{len(pair_records)}); the core tracking claim in success_criteria is not "
            f"supported by this evaluation."
        )
    elif any_value_disconfirm:
        overall_verdict = "DISCONFIRMED"
        disconf_names = [k for k, v in value_gap.items() if k in BASELINES and v["disconfirmed_over_50pct_loss"]]
        justification = (
            f"The matched-violation-rate value comparison shows conformal-ACI losing more than 50% of "
            f"value relative to at least one rate-matched baseline ({disconf_names}), with the bootstrap CI "
            f"lower bound also exceeding 50% -- this triggers the plan's explicit safety-purchased-at-prohibitive-cost "
            f"disconfirming criterion, overriding an otherwise favorable tracking result."
        )
    else:
        overall_verdict = "PARTIALLY_CONFIRMED"
        justification = (
            f"Tolerance pass across all regimes: {tolerance_all_pass}. Holm-corrected significantly-better fraction: "
            f"{sig_frac:.2f} of {len(pair_records)} (regime,baseline) pairs. No baseline value comparison crossed the "
            f"50% disconfirming threshold. RL baseline showed the expected non-recovering degradation on at least one "
            f"unseen regime: {rl_disconfirmer_pass}. The result is directionally consistent with the hypothesis but "
            f"does not clear every pre-registered bar simultaneously (see per-regime/per-baseline breakdown for which "
            f"sub-criteria passed vs failed)."
        )

    # ---------------- assemble output ----------------
    metrics_agg = {
        "alpha": ALPHA,
        "window_requests": WINDOW,
        "n_per_regime": N_PER_REGIME,
        "n_seeds": len(SEEDS),
        "n_bootstrap": N_BOOTSTRAP,
        "tolerance_pp": TOL_PP,
        "conformal_mad_mean_across_regimes": float(
            np.mean([v for r in REGIMES if (v := per_policy_regime["conformal_aci"][r]["mad_point"]) is not None])
        ),
        "conformal_tolerance_all_regimes_pass": float(tolerance_all_pass),
        "significant_pairs_fraction": float(sig_frac),
        "rl_disconfirmer_pass": float(rl_disconfirmer_pass),
        "knapsack_guarantee_indistinguishable": float(knapsack_check["guarantee_indistinguishable"]),
        "knapsack_value_gain_significant": float(knapsack_check["value_gain_significant_and_positive"]),
    }
    for baseline, v in value_gap.items():
        if baseline in BASELINES and v["value_gap_pct"] is not None:
            metrics_agg[f"value_gap_pct_vs_{baseline}"] = float(v["value_gap_pct"])

    output = {
        "metadata": {
            "evaluation_name": "conformal_admission_control_regime_shift_verdict",
            "dependency_status": {
                "gen_art_dataset_1": "empty_at_execution_time",
                "gen_art_experiment_1": "empty_at_execution_time",
                "resolution": (
                    "self-generated a from-scratch multi-regime traffic dataset and re-implemented all "
                    "5 admission policies (conformal_aci, fixed_threshold, index_based, rl_frozen, "
                    "oracle_hindsight) inside eval.py to produce genuine logs for the pipeline described "
                    "in the artifact plan; see eval.py module docstring for full rationale."
                ),
            },
            "validity_notes": VALIDITY_NOTES,
            "calibration_params": calib_params,
            "policies": ALL_POLICIES,
            "baselines_for_significance_test": BASELINES,
            "regimes": REGIMES,
            "overall_verdict": overall_verdict,
            "overall_verdict_justification": justification,
            "per_policy_regime_deviation_stats": per_policy_regime,
            "paired_significance_tests_holm_corrected": pair_records,
            "rl_non_recovering_disconfirmer": rl_degradation,
            "matched_violation_rate_value_comparison_stationary": value_gap,
            "phase3_knapsack_vs_fcfs_check": knapsack_check,
        },
        "metrics_agg": metrics_agg,
        "datasets": [
            {
                "dataset": "self_generated_multi_regime_admission_control_logs",
                "examples": [
                    {
                        "input": f"policy={pname}, regime={regime}",
                        "output": json.dumps(
                            {
                                "mad_point": per_policy_regime[pname][regime]["mad_point"],
                                "mad_ci95": per_policy_regime[pname][regime]["mad_ci95"],
                                "max_spike_point": per_policy_regime[pname][regime]["max_spike_point"],
                                "max_spike_ci95": per_policy_regime[pname][regime]["max_spike_ci95"],
                                "tolerance_pass_3pp": per_policy_regime[pname][regime]["tolerance_pass_3pp"],
                            }
                        ),
                        "metadata_policy": pname,
                        "metadata_regime": regime,
                        # -1 sentinel (schema requires a number, not null) means insufficient_admissions=True
                        # for this (policy, regime) cell -- see the per_policy_regime_deviation_stats block for
                        # the authoritative flag.
                        "eval_mad": (per_policy_regime[pname][regime]["mad_point"] if per_policy_regime[pname][regime]["mad_point"] is not None else -1.0),
                        "eval_max_spike": (per_policy_regime[pname][regime]["max_spike_point"] if per_policy_regime[pname][regime]["max_spike_point"] is not None else -1.0),
                    }
                    for pname in ALL_POLICIES
                    for regime in REGIMES
                ],
            }
        ],
    }

    out_path = RESULTS_DIR / "eval_out.json"
    out_path.write_text(json.dumps(output, indent=2, default=lambda o: float(o) if isinstance(o, np.floating) else o))
    logger.info(f"Wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB); overall_verdict={overall_verdict}")

    write_summary_table(per_policy_regime, value_gap)
    write_plots(rolling_series_for_plots, per_policy_regime)


def _fmt(x: float | None) -> str:
    return "NA" if x is None else f"{x:.5f}"


def write_summary_table(per_policy_regime: dict[str, Any], value_gap: dict[str, Any]) -> None:
    lines = ["policy,regime,mad,mad_ci_lo,mad_ci_hi,max_spike,max_spike_ci_lo,max_spike_ci_hi,tolerance_pass,value_gap_pct_vs_conformal"]
    for pname in ALL_POLICIES:
        for regime in REGIMES:
            e = per_policy_regime[pname][regime]
            vg = value_gap.get(pname, {}).get("value_gap_pct", "") if regime == "stationary" else ""
            lines.append(
                f"{pname},{regime},{_fmt(e['mad_point'])},{_fmt(e['mad_ci95'][0])},{_fmt(e['mad_ci95'][1])},"
                f"{_fmt(e['max_spike_point'])},{_fmt(e['max_spike_ci95'][0])},{_fmt(e['max_spike_ci95'][1])},"
                f"{e['tolerance_pass_3pp']},{vg}"
            )
    csv_path = RESULTS_DIR / "summary_table.csv"
    csv_path.write_text("\n".join(lines))
    logger.info(f"Wrote {csv_path}")


def write_plots(rolling_series_for_plots: dict[str, dict[str, np.ndarray]], per_policy_regime: dict[str, Any]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = {
        "conformal_aci": "tab:blue",
        "fixed_threshold": "tab:orange",
        "index_based": "tab:green",
        "rl_frozen": "tab:red",
        "oracle_hindsight": "tab:gray",
    }
    for regime in REGIMES:
        fig, ax = plt.subplots(figsize=(10, 4.5))
        ax.axhspan(BAND[0], BAND[1], color="lightgray", alpha=0.5, label=f"+/-{TOL_PP*100:.0f}pp tolerance band")
        ax.axhline(ALPHA, color="black", linestyle="--", linewidth=1, label=f"alpha={ALPHA}")
        for pname in ALL_POLICIES:
            series = rolling_series_for_plots[regime][pname]
            ax.plot(series, label=pname, color=colors[pname], linewidth=1.2, alpha=0.9)
        ax.axvline(WINDOW, color="k", linestyle=":", linewidth=0.8, label="burn-in end")
        if regime == "switch":
            ax.axvline(N_PER_REGIME // 2, color="purple", linestyle="-.", linewidth=1, label="regime switch point")
        ax.set_xlabel("request index")
        ax.set_ylabel("rolling violation rate (window=%d requests)" % WINDOW)
        ax.set_title(f"Rolling SLO-violation rate vs alpha -- regime={regime}")
        ax.legend(loc="upper right", fontsize=8, ncol=2)
        ax.set_ylim(-0.02, 1.0)
        fig.tight_layout()
        for ext in ("png", "pdf"):
            fig.savefig(FIG_DIR / f"rolling_violation_rate_{regime}.{ext}", dpi=150)
        plt.close(fig)

    # dedicated recovery-trajectory figure for the switch regime
    fig, ax = plt.subplots(figsize=(10, 4.5))
    switch_idx = N_PER_REGIME // 2
    window_plot = slice(max(0, switch_idx - 100), min(N_PER_REGIME, switch_idx + 1200))
    ax.axhspan(BAND[0], BAND[1], color="lightgray", alpha=0.5, label=f"+/-{TOL_PP*100:.0f}pp tolerance band")
    ax.axhline(ALPHA, color="black", linestyle="--", linewidth=1, label=f"alpha={ALPHA}")
    ax.axvline(switch_idx, color="purple", linestyle="-.", linewidth=1, label="regime switch point")
    for pname in ALL_POLICIES:
        series = rolling_series_for_plots["switch"][pname]
        ax.plot(np.arange(N_PER_REGIME)[window_plot], series[window_plot], label=pname, color=colors[pname], linewidth=1.3)
    ax.set_xlabel("request index")
    ax.set_ylabel("rolling violation rate")
    ax.set_title("Recovery trajectory after regime switch")
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"recovery_trajectory_switch.{ext}", dpi=150)
    plt.close(fig)
    logger.info(f"Wrote {len(REGIMES) + 1} figure(s) x2 formats to {FIG_DIR}")


if __name__ == "__main__":
    main()
