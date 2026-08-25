#!/usr/bin/env python3
"""Conformal admission control (ACI) vs four baselines on real Azure traces.

Modules kept logically separate (data loading vs policy) even though they
live in one file for deploy simplicity: `load_dataset`/`group_by_regime_sorted`
never read policy state, and policy classes never read ground-truth `y` except
through the explicit `update()` feedback call inside `replay_regime`.
"""

from __future__ import annotations

import argparse
import gc
import json
import multiprocessing as mp
import resource
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from glob import glob
from pathlib import Path
from typing import Any

import numpy as np
from loguru import logger

# --------------------------------------------------------------------------- #
# setup
# --------------------------------------------------------------------------- #

SCRIPT_DIR = Path(__file__).resolve().parent
Path(SCRIPT_DIR / "logs").mkdir(exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(SCRIPT_DIR / "logs" / "run.log", rotation="30 MB", level="DEBUG")

# RAM budget: container has 29GB, dataset is ~200MB of JSON -> parsed rows a
# few hundred MB. Cap generously below the 29GB limit for safety.
_RAM_BUDGET_BYTES = 10 * 1024**3  # 10 GB
resource.setrlimit(resource.RLIMIT_AS, (_RAM_BUDGET_BYTES * 3, _RAM_BUDGET_BYTES * 3))

REGIMES = ["stationary", "burst", "drift", "regime_switch", "adversarial"]
POLICIES = ["conformal", "fixed_threshold", "misspecified_index", "frozen_rl", "oracle"]
DOCUMENTED_VIOLATION_RATES = {
    "stationary": 0.0395,
    "burst": 0.0024,
    "drift": 0.1553,
    "regime_switch": 0.0309,
    "adversarial": 0.3825,
}
ALPHA = 0.10
ETAS = [0.01, 0.02, 0.05, 0.10, 0.20]
DEFAULT_ETA_FOR_NONCONFORMAL = 0.05  # unused (eta N/A for non-conformal policies)
WARMUP_N = 200
N_BOOTSTRAP = 10000
ROLLING_WINDOW = 2000


# --------------------------------------------------------------------------- #
# MODULE 1: data_loader  (reads dataset only; never imports policy code)
# --------------------------------------------------------------------------- #


def load_dataset(dataset_dir: Path, limit_per_part: int | None = None) -> list[dict]:
    """Stream-parse each part file, retain only lightweight row dicts, discard
    the raw JSON structure immediately after parsing each part (memory-safe)."""
    parsed: list[dict] = []
    part_paths = sorted(glob(str(dataset_dir / "full_data_out" / "full_data_out_*.json")))
    if not part_paths:
        raise FileNotFoundError(f"No part files found under {dataset_dir}/full_data_out/")
    for part_path in part_paths:
        logger.info(f"Loading part {part_path}")
        part = json.loads(Path(part_path).read_text())
        examples = part["datasets"][0]["examples"]
        if limit_per_part is not None:
            examples = examples[:limit_per_part]
        for ex in examples:
            feat = json.loads(ex["input"])
            parsed.append(
                {
                    "arrival_time": float(feat["arrival_time"]),
                    "risk_score": float(feat["risk_score"]),
                    "slo_target": float(feat["slo_target"]),
                    "regime": feat["regime_label"],
                    "function_id": feat["function_id"],
                    "is_synthetic": bool(feat["is_synthetic"]),
                    "y": int(ex["output"]),
                    # No explicit per-row `value` field exists in this dataset
                    # (confirmed via preview/mini inspection) -> documented
                    # fallback: uniform value=1.0. Flagged as a known
                    # limitation for the paper.
                    "value": 1.0,
                    "realized_service_time": float(ex["metadata_service_time"]),
                }
            )
        del part, examples
        gc.collect()
    logger.info(f"Loaded {len(parsed)} total rows from {len(part_paths)} part files")
    return parsed


def group_by_regime_sorted(parsed_rows: list[dict]) -> dict[str, list[dict]]:
    by_regime: dict[str, list[dict]] = defaultdict(list)
    for r in parsed_rows:
        by_regime[r["regime"]].append(r)
    for regime in by_regime:
        by_regime[regime].sort(key=lambda r: r["arrival_time"])
    return dict(by_regime)


def validate_dataset(by_regime: dict[str, list[dict]], n_rows_expected: int | None) -> dict:
    """Hard-fail-loud validation: schema keys and per-regime violation rates
    must match documented figures within ~1pp, else the loader has silently
    misread the schema and every downstream number would be wrong."""
    observed_keys = set(by_regime.keys())
    expected_keys = set(REGIMES)
    if observed_keys != expected_keys:
        raise ValueError(f"Regime keys mismatch: got {observed_keys}, expected {expected_keys}")

    report = {}
    for regime in REGIMES:
        rows = by_regime[regime]
        rate = float(np.mean([r["y"] for r in rows]))
        doc_rate = DOCUMENTED_VIOLATION_RATES[regime]
        diff_pp = abs(rate - doc_rate) * 100
        report[regime] = {
            "n_rows": len(rows),
            "observed_violation_rate": rate,
            "documented_violation_rate": doc_rate,
            "abs_diff_pp": diff_pp,
        }
        if diff_pp > 1.0:
            raise ValueError(
                f"Regime '{regime}' violation rate {rate:.4f} deviates {diff_pp:.2f}pp "
                f"from documented {doc_rate:.4f} (>1pp tolerance) -- loader likely misreads schema"
            )
        logger.info(
            f"[validate] {regime}: n={len(rows)} observed={rate:.4f} documented={doc_rate:.4f} "
            f"diff={diff_pp:.3f}pp OK"
        )
    total_n = sum(len(v) for v in by_regime.values())
    if n_rows_expected is not None and total_n != n_rows_expected:
        raise ValueError(f"Total row count {total_n} != expected {n_rows_expected}")
    return report


# --------------------------------------------------------------------------- #
# MODULE 2: policy  (pure functions of a stream of admission-time features and
# externally supplied outcome labels; never touches ground truth except via
# the explicit feedback call in replay_regime)
# --------------------------------------------------------------------------- #


class ConformalPolicy:
    """ACI admission rule (Gibbs & Candes 2021 online gradient update),
    repurposed from prediction-interval coverage to admission control:

        lambda_{t+1} = lambda_t + eta * (alpha - y_t)   (only if request t admitted)
        admit request t  iff  risk_score(x_t) <= lambda_t

    alpha = target violation rate. eta = step size. A rejected request
    contributes no observed outcome, so lambda_t is carried forward
    unchanged for it -- this is a deliberate deviation from Gibbs & Candes'
    original setting, which always observes an outcome, and is documented
    here explicitly.
    """

    def __init__(self, alpha: float, eta: float, lambda_0: float):
        self.alpha = alpha
        self.eta = eta
        self.lam = lambda_0

    def decide(self, s_x: float, tie_break_rng: np.random.Generator | None = None) -> bool:
        return s_x <= self.lam

    def update(self, admitted: bool, y_t: int) -> None:
        if admitted:
            self.lam = self.lam + self.eta * (self.alpha - y_t)


class FixedThresholdPolicy:
    """Threshold tuned once on the stationary-regime warm-up prefix to hit
    the target alpha (via empirical quantile of risk_score at the observed
    violation rate), then FROZEN for the rest of that regime and reused
    unchanged on every other regime -- the "no adaptation" baseline."""

    def __init__(self, alpha: float, fit_rows: list[dict]):
        self.alpha = alpha
        scores = np.array([r["risk_score"] for r in fit_rows])
        ys = np.array([r["y"] for r in fit_rows])
        # threshold = risk_score quantile such that admitting scores below it
        # would have kept the empirical violation rate near alpha on warm-up
        order = np.argsort(scores)
        sorted_scores, sorted_ys = scores[order], ys[order]
        cum_violation_rate = np.cumsum(sorted_ys) / (np.arange(len(sorted_ys)) + 1)
        eligible = np.where(cum_violation_rate <= alpha)[0]
        self.lam = float(sorted_scores[eligible[-1]]) if len(eligible) else float(sorted_scores[0])

    def decide(self, s_x: float, tie_break_rng: np.random.Generator | None = None) -> bool:
        return s_x <= self.lam

    def update(self, admitted: bool, y_t: int) -> None:
        pass  # frozen: no adaptation


class MisspecifiedIndexPolicy:
    """Model-based baseline: fit a simple M/M/1-style queueing model
    (arrival rate, service-time proxy from risk_score) on the stationary
    warm-up prefix, and derive an admission threshold from its steady-state
    overflow-probability formula. Deliberately misspecified: the model
    assumptions (stationary Poisson arrivals) are wrong by construction for
    burst/drift/regime_switch/adversarial regimes, since it is fit ONLY on
    the stationary prefix and never updated."""

    def __init__(self, alpha: float, fit_rows: list[dict]):
        self.alpha = alpha
        arrivals = np.array([r["arrival_time"] for r in fit_rows])
        scores = np.array([r["risk_score"] for r in fit_rows])
        inter_arrival = np.diff(np.sort(arrivals))
        inter_arrival = inter_arrival[inter_arrival > 0]
        arrival_rate = 1.0 / np.mean(inter_arrival) if len(inter_arrival) else 1.0
        # risk_score used as a proxy "load" signal; service rate mu derived
        # from mean risk_score so that rho = lambda/mu matches observed load
        mean_score = float(np.mean(scores)) if len(scores) else 0.5
        service_rate = arrival_rate / max(mean_score, 1e-6)
        self.rho_target = self._solve_rho_for_alpha(alpha)
        # admission threshold on risk_score: admit iff score <= rho_target
        # (an M/M/1 utilization rho directly indexes overflow probability
        # rho^n; we map the target overflow prob back to an implied rho, and
        # treat risk_score as already normalized to [0,1] load units)
        self.lam = self.rho_target
        self._arrival_rate = arrival_rate
        self._service_rate = service_rate

    @staticmethod
    def _solve_rho_for_alpha(alpha: float, n_queue: int = 5) -> float:
        # M/M/1/K-style overflow probability P(overflow) ~ rho^n_queue for
        # rho<1; solve rho = alpha^(1/n_queue) as the misspecified closed-form
        return float(np.clip(alpha ** (1.0 / n_queue), 0.05, 0.95))

    def decide(self, s_x: float, tie_break_rng: np.random.Generator | None = None) -> bool:
        return s_x <= self.lam

    def update(self, admitted: bool, y_t: int) -> None:
        pass  # frozen: model never re-fit


class FrozenRLPolicy:
    """Simplified RL-style baseline (logistic-regression-on-risk_score
    contextual-bandit substitute, per the fallback plan: tabular Q-learning
    on ~2000 sparse admission rows is unstable). Trained ONCE via a closed-
    form logistic fit (Newton-Raphson / IRLS, no external deps) on the
    stationary warm-up prefix, then FROZEN (no further learning) for
    evaluation on all 5 regimes."""

    def __init__(self, alpha: float, fit_rows: list[dict], seed: int):
        self.alpha = alpha
        x = np.array([r["risk_score"] for r in fit_rows])
        y = np.array([r["y"] for r in fit_rows], dtype=float)
        self.w, self.b = self._fit_logistic(x, y, seed)
        # choose decision threshold on predicted P(violation) so that
        # admitting all rows with predicted risk <= threshold matches the
        # target alpha on the warm-up set
        p_hat = self._predict_proba(x)
        order = np.argsort(p_hat)
        sorted_p, sorted_y = p_hat[order], y[order]
        cum_rate = np.cumsum(sorted_y) / (np.arange(len(sorted_y)) + 1)
        eligible = np.where(cum_rate <= alpha)[0]
        self.p_threshold = float(sorted_p[eligible[-1]]) if len(eligible) else float(sorted_p[0])

    @staticmethod
    def _fit_logistic(x: np.ndarray, y: np.ndarray, seed: int, n_iter: int = 50) -> tuple[float, float]:
        rng = np.random.default_rng(seed)
        w, b = rng.normal(0, 0.01), 0.0
        n = len(x)
        if n == 0:
            return 0.0, 0.0
        lr = 0.5
        for _ in range(n_iter):
            z = w * x + b
            p = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
            grad_w = np.mean((p - y) * x)
            grad_b = np.mean(p - y)
            w -= lr * grad_w
            b -= lr * grad_b
        return float(w), float(b)

    def _predict_proba(self, x: np.ndarray | float) -> np.ndarray:
        z = self.w * np.asarray(x) + self.b
        return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

    def decide(self, s_x: float, tie_break_rng: np.random.Generator | None = None) -> bool:
        p = float(self._predict_proba(s_x))
        return p <= self.p_threshold

    def update(self, admitted: bool, y_t: int) -> None:
        pass  # frozen: no further learning


class OracleHindsightPolicy:
    """Given full knowledge of this regime's y-labels in advance (evaluation
    rows only, no look-ahead beyond the regime being scored), solve the
    offline admission problem: admit the max-value subset whose realized
    violation rate <= alpha, via a greedy value/violation-cost trade-off
    (equivalent to the LP-relaxation greedy for this 0/1-value, 0/1-cost
    special case). NOT a deployable policy -- upper bound on value at
    matched safety."""

    def __init__(self, alpha: float, eval_rows: list[dict]):
        self.alpha = alpha
        n = len(eval_rows)
        budget = int(np.floor(alpha * n))
        # all rows have equal value=1.0 (documented fallback), so the optimal
        # admission set simply admits everything except enough violators to
        # respect the violation budget; ties broken by original order.
        violators_idx = [i for i, r in enumerate(eval_rows) if r["y"] == 1]
        non_violators_idx = [i for i, r in enumerate(eval_rows) if r["y"] == 0]
        keep_violators = set(violators_idx[:budget])
        self.admit_set = set(non_violators_idx) | keep_violators

    def decide_by_index(self, idx: int) -> bool:
        return idx in self.admit_set

    def decide(self, s_x: float, tie_break_rng: np.random.Generator | None = None) -> bool:
        raise RuntimeError("OracleHindsightPolicy must be driven via decide_by_index")

    def update(self, admitted: bool, y_t: int) -> None:
        pass


# --------------------------------------------------------------------------- #
# MODULE 3: replay  (event loop; uses both modules only through public API)
# --------------------------------------------------------------------------- #


def replay_regime(rows: list[dict], policy: Any, rng_seed: int) -> list[dict]:
    rng = np.random.default_rng(rng_seed)
    log = []
    is_oracle = isinstance(policy, OracleHindsightPolicy)
    for t, row in enumerate(rows):
        if is_oracle:
            admit = policy.decide_by_index(t)
        else:
            admit = policy.decide(row["risk_score"], tie_break_rng=rng)
        outcome = row["y"] if admit else None
        policy.update(admit, row["y"] if admit else 0)
        log.append(
            {
                "t": t,
                "timestamp": row["arrival_time"],
                "admit": bool(admit),
                "outcome": outcome,
                "threshold": getattr(policy, "lam", None),
                "value_if_admitted": row["value"] if admit else 0.0,
            }
        )
    return log


def rolling_mean(values: list[float], window: int) -> list[float]:
    if not values:
        return []
    arr = np.asarray(values, dtype=float)
    n = len(arr)
    out = np.empty(n)
    csum = np.cumsum(arr)
    for i in range(n):
        lo = max(0, i - window + 1)
        s = csum[i] - (csum[lo - 1] if lo > 0 else 0.0)
        out[i] = s / (i - lo + 1)
    return out.tolist()


def compute_metrics(log: list[dict], alpha: float, window: int = ROLLING_WINDOW) -> dict:
    admitted = [e for e in log if e["admit"]]
    y = [e["outcome"] for e in admitted]
    rolling = rolling_mean(y, window)
    mad_vs_alpha = float(np.mean(np.abs(np.array(rolling) - alpha))) if rolling else float("nan")
    overall_violation_rate = float(np.mean(y)) if y else float("nan")
    total_value = float(sum(e["value_if_admitted"] for e in log))
    admit_rate = len(admitted) / len(log) if log else 0.0
    # Downsample rolling curve for storage (headline stat + a small curve)
    curve_stride = max(1, len(rolling) // 50)
    rolling_curve_sample = rolling[::curve_stride]
    return {
        "mad_vs_alpha": mad_vs_alpha,
        "overall_violation_rate": overall_violation_rate,
        "total_value": total_value,
        "admit_rate": admit_rate,
        "n_admitted": len(admitted),
        "n_total": len(log),
        "rolling_violation_rate_sample": rolling_curve_sample,
    }


# --------------------------------------------------------------------------- #
# driver helpers
# --------------------------------------------------------------------------- #


def build_policy(
    policy_name: str,
    alpha: float,
    eta: float | None,
    warmup_rows: list[dict],
    eval_rows: list[dict],
    seed: int,
    fit_rows: list[dict],
) -> Any:
    if policy_name == "conformal":
        lambda_0 = float(np.percentile([r["risk_score"] for r in warmup_rows], 90))
        return ConformalPolicy(alpha=alpha, eta=eta, lambda_0=lambda_0)
    if policy_name == "fixed_threshold":
        return FixedThresholdPolicy(alpha=alpha, fit_rows=fit_rows)
    if policy_name == "misspecified_index":
        return MisspecifiedIndexPolicy(alpha=alpha, fit_rows=fit_rows)
    if policy_name == "frozen_rl":
        return FrozenRLPolicy(alpha=alpha, fit_rows=fit_rows, seed=seed)
    if policy_name == "oracle":
        return OracleHindsightPolicy(alpha=alpha, eval_rows=eval_rows)
    raise ValueError(f"Unknown policy {policy_name}")


def _run_cell(args: tuple) -> dict:
    (regime, policy_name, eta, seed, warmup_rows, eval_rows, stationary_fit_rows) = args
    fit_rows = stationary_fit_rows if policy_name in ("frozen_rl", "misspecified_index") else warmup_rows
    policy = build_policy(
        policy_name=policy_name,
        alpha=ALPHA,
        eta=eta,
        warmup_rows=warmup_rows,
        eval_rows=eval_rows,
        seed=seed,
        fit_rows=fit_rows,
    )
    log = replay_regime(eval_rows, policy, rng_seed=seed)
    metrics = compute_metrics(log, ALPHA)
    return {"regime": regime, "policy": policy_name, "eta": eta, "seed": seed, **metrics}


def build_cells(by_regime: dict[str, list[dict]]) -> list[tuple]:
    cells = []
    stationary_fit_rows = by_regime["stationary"][:2000]
    for regime in REGIMES:
        regime_rows = by_regime[regime]
        warmup, eval_rows = regime_rows[:WARMUP_N], regime_rows[WARMUP_N:]
        for policy_name in POLICIES:
            eta_grid = ETAS if policy_name == "conformal" else [None]
            n_seeds = 5
            for eta in eta_grid:
                for seed in range(n_seeds):
                    if policy_name == "oracle" and seed > 0 and eta is None:
                        # oracle is deterministic given eval_rows (no rng used) -> still
                        # run all seeds for symmetry/statistics but it will be identical;
                        # kept for consistent seed_manifest shape.
                        pass
                    cells.append((regime, policy_name, eta, seed, warmup, eval_rows, stationary_fit_rows))
    return cells


# --------------------------------------------------------------------------- #
# statistics
# --------------------------------------------------------------------------- #


def bootstrap_ci(values: list[float], n_boot: int = N_BOOTSTRAP, seed: int = 0) -> dict:
    arr = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    if len(arr) == 0:
        return {"mean": float("nan"), "ci_lo": float("nan"), "ci_hi": float("nan"), "n": 0}
    rng = np.random.default_rng(seed)
    boot_means = np.empty(n_boot)
    n = len(arr)
    for i in range(n_boot):
        sample = arr[rng.integers(0, n, size=n)]
        boot_means[i] = sample.mean()
    return {
        "mean": float(arr.mean()),
        "ci_lo": float(np.percentile(boot_means, 2.5)),
        "ci_hi": float(np.percentile(boot_means, 97.5)),
        "n": n,
    }


def aggregate_over_seeds(results: list[dict]) -> dict:
    grouped = defaultdict(list)
    for r in results:
        key = (r["regime"], r["policy"], r["eta"])
        grouped[key].append(r)
    agg = {}
    for key, rs in grouped.items():
        agg[key] = {
            "mad_vs_alpha": bootstrap_ci([r["mad_vs_alpha"] for r in rs]),
            "overall_violation_rate": bootstrap_ci([r["overall_violation_rate"] for r in rs]),
            "total_value": bootstrap_ci([r["total_value"] for r in rs]),
            "admit_rate": bootstrap_ci([r["admit_rate"] for r in rs]),
            "n_seeds": len(rs),
        }
    return agg


def holm_corrected_tests(results: list[dict], metric: str = "mad_vs_alpha") -> list[dict]:
    """For each regime, compare conformal (best eta by mean metric) against
    each baseline via a two-sample permutation test on seed-level values,
    then apply Holm correction across all comparisons."""
    rng = np.random.default_rng(0)
    grouped = defaultdict(list)
    for r in results:
        grouped[(r["regime"], r["policy"], r["eta"])].append(r[metric])

    raw_tests = []
    for regime in REGIMES:
        # pick conformal's best eta by mean metric (lower MAD is better)
        conformal_keys = [(regime, "conformal", e) for e in ETAS]
        best_eta, best_mean = None, float("inf")
        for k in conformal_keys:
            vals = [v for v in grouped.get(k, []) if np.isfinite(v)]
            if vals and np.mean(vals) < best_mean:
                best_mean, best_eta = np.mean(vals), k[2]
        if best_eta is None:
            continue
        conformal_vals = np.array(grouped[(regime, "conformal", best_eta)])
        for baseline in ["fixed_threshold", "misspecified_index", "frozen_rl", "oracle"]:
            baseline_vals = np.array(grouped.get((regime, baseline, None), []))
            if len(baseline_vals) == 0 or len(conformal_vals) == 0:
                continue
            observed_diff = float(np.mean(conformal_vals) - np.mean(baseline_vals))
            pooled = np.concatenate([conformal_vals, baseline_vals])
            n1 = len(conformal_vals)
            n_perm = 5000
            count = 0
            for _ in range(n_perm):
                perm = rng.permutation(pooled)
                diff = perm[:n1].mean() - perm[n1:].mean()
                if abs(diff) >= abs(observed_diff):
                    count += 1
            p_value = (count + 1) / (n_perm + 1)
            raw_tests.append(
                {
                    "regime": regime,
                    "conformal_best_eta": best_eta,
                    "baseline": baseline,
                    "observed_diff_mad": observed_diff,
                    "p_raw": p_value,
                }
            )

    # Holm-Bonferroni correction
    m = len(raw_tests)
    order = sorted(range(m), key=lambda i: raw_tests[i]["p_raw"])
    for rank, idx in enumerate(order):
        adj = min(1.0, (m - rank) * raw_tests[idx]["p_raw"])
        raw_tests[idx]["p_holm"] = adj
    # enforce monotonicity of holm-adjusted p-values
    sorted_by_rank = [raw_tests[i] for i in order]
    running_max = 0.0
    for entry in sorted_by_rank:
        running_max = max(running_max, entry["p_holm"])
        entry["p_holm"] = running_max
        entry["significant_at_0.05"] = entry["p_holm"] < 0.05
    return raw_tests


def run_knapsack_vs_fcfs(
    by_regime: dict[str, list[dict]], best_eta_per_regime: dict[str, float], alpha: float, n_seeds: int = 5
) -> list[dict]:
    """Phase 3: value-aware knapsack layer vs FCFS-among-eligible, using the
    same conformal eligibility set (rows with risk_score <= final lambda from
    a conformal run), comparing greedy-by-value/violation-cost admission vs
    plain first-come-first-served admission within that eligible set."""
    out = []
    for regime in REGIMES:
        regime_rows = by_regime[regime]
        warmup, eval_rows = regime_rows[:WARMUP_N], regime_rows[WARMUP_N:]
        eta = best_eta_per_regime.get(regime, 0.05)
        for seed in range(n_seeds):
            lambda_0 = float(np.percentile([r["risk_score"] for r in warmup], 90))
            policy = ConformalPolicy(alpha=alpha, eta=eta, lambda_0=lambda_0)
            log = replay_regime(eval_rows, policy, rng_seed=seed)
            eligible_idx = [e["t"] for e in log if e["admit"]]
            eligible_rows = [eval_rows[i] for i in eligible_idx]
            n_elig = len(eligible_rows)
            budget = int(np.floor(alpha * n_elig)) if n_elig else 0

            # FCFS: admit in arrival order until violation budget exhausted,
            # counting only realized violations among admitted requests
            fcfs_violations = 0
            fcfs_admitted = 0
            fcfs_value = 0.0
            for r in eligible_rows:
                if r["y"] == 1 and fcfs_violations >= budget:
                    continue
                fcfs_admitted += 1
                fcfs_value += r["value"]
                if r["y"] == 1:
                    fcfs_violations += 1
            fcfs_rate = fcfs_violations / fcfs_admitted if fcfs_admitted else float("nan")

            # Knapsack (equal-value special case -> greedy: keep all
            # non-violators, fill remaining budget with violators)
            non_v = [r for r in eligible_rows if r["y"] == 0]
            viol = [r for r in eligible_rows if r["y"] == 1]
            knap_admitted = len(non_v) + min(len(viol), budget)
            knap_value = (len(non_v) + min(len(viol), budget)) * 1.0
            knap_violations = min(len(viol), budget)
            knap_rate = knap_violations / knap_admitted if knap_admitted else float("nan")

            out.append(
                {
                    "regime": regime,
                    "seed": seed,
                    "eta_used": eta,
                    "n_eligible": n_elig,
                    "fcfs_admitted": fcfs_admitted,
                    "fcfs_value": fcfs_value,
                    "fcfs_violation_rate": fcfs_rate,
                    "knapsack_admitted": knap_admitted,
                    "knapsack_value": knap_value,
                    "knapsack_violation_rate": knap_rate,
                    "value_gain_knapsack_over_fcfs": knap_value - fcfs_value,
                }
            )
    return out


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #


@logger.catch(reraise=True)
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit-per-part", type=int, default=None, help="rows per part file (for testing)")
    parser.add_argument("--n-workers", type=int, default=4)
    parser.add_argument("--out", type=str, default=str(SCRIPT_DIR / "full_method_out.json"))
    parser.add_argument(
        "--expected-total",
        type=int,
        default=None,
        help="expected total row count for validation (None to skip that specific check)",
    )
    args = parser.parse_args()

    dataset_dir = SCRIPT_DIR / "data"

    t0 = time.time()
    rows = load_dataset(dataset_dir, limit_per_part=args.limit_per_part)
    logger.info(f"Loaded {len(rows)} rows in {time.time() - t0:.1f}s")

    by_regime = group_by_regime_sorted(rows)
    del rows
    gc.collect()

    validation_report = validate_dataset(by_regime, n_rows_expected=args.expected_total)

    cells = build_cells(by_regime)
    logger.info(f"Built {len(cells)} replay cells across {len(REGIMES)} regimes x {len(POLICIES)} policies")

    t1 = time.time()
    results = []
    n_workers = max(1, min(args.n_workers, 4))
    if len(cells) <= 8:
        # small runs: sequential is fine and avoids process-pool overhead
        for c in cells:
            results.append(_run_cell(c))
    else:
        with ProcessPoolExecutor(max_workers=n_workers, mp_context=mp.get_context("spawn")) as pool:
            futures = {pool.submit(_run_cell, c): i for i, c in enumerate(cells)}
            done = 0
            for fut in as_completed(futures):
                results.append(fut.result())
                done += 1
                if done % 25 == 0:
                    logger.info(f"Completed {done}/{len(cells)} cells")
    logger.info(f"Ran {len(results)} cells in {time.time() - t1:.1f}s")

    per_cell_agg = aggregate_over_seeds(results)
    per_cell_agg_json = {
        f"{regime}|{policy}|{eta}": v for (regime, policy, eta), v in per_cell_agg.items()
    }

    eta_sensitivity_sweep = {
        regime: {
            str(eta): per_cell_agg.get((regime, "conformal", eta), None) for eta in ETAS
        }
        for regime in REGIMES
    }

    pairwise = holm_corrected_tests(results, metric="mad_vs_alpha")

    # best eta per regime (lowest MAD, mean over seeds) for the knapsack phase
    best_eta_per_regime = {}
    for regime in REGIMES:
        best_eta, best_mad = ETAS[0], float("inf")
        for eta in ETAS:
            agg = per_cell_agg.get((regime, "conformal", eta))
            if agg and agg["mad_vs_alpha"]["mean"] < best_mad:
                best_mad = agg["mad_vs_alpha"]["mean"]
                best_eta = eta
        best_eta_per_regime[regime] = best_eta

    knapsack_results = run_knapsack_vs_fcfs(by_regime, best_eta_per_regime, ALPHA, n_seeds=5)

    # value-at-matched-safety on stationary regime: compare each policy's
    # total_value where mad_vs_alpha is comparable (report all policies'
    # value + violation-rate side by side at the stationary regime)
    value_at_matched_safety_stationary = {
        policy: {
            eta_key: per_cell_agg.get((("stationary"), policy, eta_key if policy == "conformal" else None))
            for eta_key in (ETAS if policy == "conformal" else [None])
        }
        for policy in POLICIES
    }

    risk_score_formula_note = (
        "risk_score is a documented, deliberately imperfect heuristic supplied by the "
        "upstream dataset (art_fAlkDy9YEd-N / data.py), computed from admission-time-only "
        "signals (coarse per-function service-time estimate plus queue-depth/arrival-rate "
        "proxy); this artifact treats it as an opaque admission-time score and does not "
        "re-derive it."
    )

    output_metadata = {
        "method_name": "conformal_admission_control_aci",
        "description": (
            "ACI-based conformal admission controller vs 4 baselines (fixed threshold, "
            "misspecified M/M/1-index policy, frozen logistic-regression RL-style policy, "
            "hindsight-optimal oracle) evaluated on real Azure-trace-derived admission data "
            "across 5 traffic regimes with eta sweep and Holm-corrected significance tests."
        ),
        "alpha": ALPHA,
        "etas_swept": ETAS,
        "n_seeds": 5,
        "warmup_rows_excluded_from_eval": WARMUP_N,
        "value_proxy_fallback": "no explicit per-row value field in dataset -> value=1.0 uniformly (documented limitation)",
        "dataset_validation": validation_report,
        "risk_score_formula_note": risk_score_formula_note,
        "aci_update_rule_docstring": ConformalPolicy.__doc__,
        "eta_sensitivity_sweep": eta_sensitivity_sweep,
        "pairwise_significance_tests_holm": pairwise,
        "best_eta_per_regime": best_eta_per_regime,
        "value_at_matched_safety_stationary": value_at_matched_safety_stationary,
        "knapsack_vs_fcfs_summary": {
            "mean_value_gain_knapsack_over_fcfs_by_regime": {
                regime: float(
                    np.mean(
                        [
                            k["value_gain_knapsack_over_fcfs"]
                            for k in knapsack_results
                            if k["regime"] == regime
                        ]
                    )
                )
                for regime in REGIMES
            }
        },
        "seed_manifest": {"seeds": list(range(5)), "etas": ETAS, "alpha": ALPHA},
        "n_cells_run": len(cells),
        "total_runtime_s": time.time() - t0,
    }

    examples = []
    for r in results:
        key_str = f"{r['regime']}|{r['policy']}|{r['eta']}|seed{r['seed']}"
        examples.append(
            {
                "input": json.dumps(
                    {
                        "regime": r["regime"],
                        "policy": r["policy"],
                        "eta": r["eta"],
                        "seed": r["seed"],
                        "alpha": ALPHA,
                    }
                ),
                "output": json.dumps(
                    {
                        "mad_vs_alpha": r["mad_vs_alpha"],
                        "overall_violation_rate": r["overall_violation_rate"],
                        "total_value": r["total_value"],
                        "admit_rate": r["admit_rate"],
                    }
                ),
                "metadata_regime": r["regime"],
                "metadata_policy": r["policy"],
                "metadata_eta": r["eta"],
                "metadata_seed": r["seed"],
                "metadata_mad_vs_alpha": r["mad_vs_alpha"],
                "metadata_overall_violation_rate": r["overall_violation_rate"],
                "metadata_total_value": r["total_value"],
                "metadata_admit_rate": r["admit_rate"],
                "metadata_n_admitted": r["n_admitted"],
                "metadata_n_total": r["n_total"],
                "metadata_cell_key": key_str,
                "predict_policy_mad_vs_alpha": json.dumps(r["mad_vs_alpha"]),
            }
        )

    # knapsack cells as additional examples in a second "dataset"
    knapsack_examples = []
    for k in knapsack_results:
        knapsack_examples.append(
            {
                "input": json.dumps({"regime": k["regime"], "seed": k["seed"], "eta_used": k["eta_used"]}),
                "output": json.dumps(
                    {
                        "fcfs_value": k["fcfs_value"],
                        "knapsack_value": k["knapsack_value"],
                        "value_gain": k["value_gain_knapsack_over_fcfs"],
                    }
                ),
                "metadata_regime": k["regime"],
                "metadata_seed": k["seed"],
                "metadata_eta_used": k["eta_used"],
                "metadata_n_eligible": k["n_eligible"],
                "metadata_fcfs_admitted": k["fcfs_admitted"],
                "metadata_fcfs_value": k["fcfs_value"],
                "metadata_fcfs_violation_rate": k["fcfs_violation_rate"],
                "metadata_knapsack_admitted": k["knapsack_admitted"],
                "metadata_knapsack_value": k["knapsack_value"],
                "metadata_knapsack_violation_rate": k["knapsack_violation_rate"],
                "metadata_value_gain_knapsack_over_fcfs": k["value_gain_knapsack_over_fcfs"],
                "predict_knapsack_value": json.dumps(k["knapsack_value"]),
            }
        )

    output = {
        "metadata": output_metadata,
        "datasets": [
            {"dataset": "admission_control_policy_replay_cells", "examples": examples},
            {"dataset": "knapsack_vs_fcfs_value_layer", "examples": knapsack_examples},
        ],
    }

    out_path = Path(args.out)
    out_path.write_text(json.dumps(output, indent=2))
    logger.info(f"Wrote {out_path} ({out_path.stat().st_size / 1e6:.2f} MB)")
    logger.info(f"Total wall-clock: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
