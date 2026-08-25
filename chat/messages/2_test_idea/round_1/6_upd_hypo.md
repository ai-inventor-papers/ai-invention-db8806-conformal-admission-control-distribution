# upd_hypo — test_idea

> Phase: `invention_loop` · round 1 · `upd_hypo`
> Run: `iter1_88afd6206a08` — Conformal Admission Control for Overloaded Request Queues
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-08-25 18:38:12 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/upd_hypo/upd_hypo
```

### [2] SYSTEM-USER prompt · 2026-08-25 18:38:20 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviser (Step 3.6: UPD_HYPO in the invention loop)

You received the current hypothesis, all artifacts, and the paper draft.
Revise the hypothesis based on what the evidence supports.

Honest revision → focused research. Inflated confidence → wasted iteration.
</your_role>
</ai_inventor_context>

You are revising a research hypothesis based on empirical evidence gathered
during an iterative invention loop. Your role is internal reflection — honest
assessment of what the evidence supports.

SCOPE: Your ONLY output is the revised hypothesis text. You do NOT run code,
produce artifacts, fix bugs, or otherwise act on the evidence yourself — the
next iteration of the invention loop will spawn fresh artifacts based on your
revised hypothesis. Reflect on the evidence and rewrite the hypothesis;
nothing else.

PRINCIPLES:
- Ground every revision in specific artifacts and results
- Treat negative and null results as valuable contributions. If the original
  approach failed, the null result IS often the contribution — frame it as
  such (e.g. "X does not improve Y under conditions Z"). Only pivot to a
  different positive claim when the evidence actually supports one; never
  fabricate a positive narrative to mask a failed approach.
- Increase specificity as evidence accumulates
- Don't inflate confidence without strong evidence
- Preserve the core AII prompt unless evidence clearly contradicts it
- Revise hypothesis text only — never attempt to address feedback by running
  code, proposing fixes, or producing artifacts; the next loop iteration
  handles all artifact generation

<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: 'Conformal Admission Control: Distribution-Free SLO Budgets for Overloaded Queues'
hypothesis: |-
  An admission control policy built on ONLINE CONFORMAL RISK CONTROL — not queueing theory, not reinforcement learning — can hold a hard, distribution-free, finite-sample guarantee on the long-run rate of SLO violations (e.g., 'no more than alpha fraction of admitted requests exceed their P99 latency target') while maximizing throughput/value, under traffic and service-time distributions that are unknown, non-stationary, and possibly adversarial — with NO assumption of exchangeability, no fitted queueing model (no M/M/1, no Markov-modulated arrivals), and no trained neural policy.

  Concretely: at admission time, a (cheap, possibly miscalibrated) scoring function s(x) produces a real-valued 'risk score' for each incoming request x — e.g., a fast heuristic or tiny regressor estimate of the probability that, if admitted right now, this request would blow its latency SLO given current queue depth, predicted service time, and recent system state. The system does NOT trust s(x)'s calibration. Instead it maintains a single scalar threshold lambda_t, updated after every observed outcome via the Adaptive Conformal Inference (ACI) gradient step: lambda_{t+1} = lambda_t + eta * (alpha - 1[actual outcome for the request admitted/denied at time t was an SLO violation]), i.e. lambda_t rises when recent admissions are violating the SLO more than the target rate alpha and falls when they are violating it less — admit iff s(x) <= lambda_t. Because this is a pure feedback-controlled quantile-tracking rule (not a fitted distributional model), it inherits the Gibbs & Candes (2021) guarantee that the EMPIRICAL SLO-violation rate over any long window converges to alpha REGARDLESS of the true, unknown, non-stationary arrival/service process — a guarantee that no queueing-theoretic policy (which assumes a distributional model) or RL policy (which has no finite-sample distribution-free guarantee at all, only asymptotic or empirical performance) can offer. Request VALUE heterogeneity is incorporated not by biasing the guarantee (which stays SLO-focused and class-agnostic) but by using value as the tie-break / ordering signal WITHIN the admitted budget each control interval: when the conformal budget for this interval allows admitting K more requests, admit the K highest-value eligible requests (s(x) <= lambda_t) rather than first-come-first-served, turning the risk-controlled budget into a value-maximizing knapsack subject to a provable violation-rate ceiling.
motivation: |-
  The two dominant admission-control paradigms both have a specific, verifiable weakness. Queueing-theoretic / index-based policies (e.g., the classical marginal-productivity / Whittle-index admission control of Nino-Mora 2002, Mathematical Programming, arXiv:2304.01946, verified by full-text fetch) give elegant near-optimality results but REQUIRE a distributional model — birth-death dynamics, known or estimated transition kernels — and their guarantees are about EXPECTED long-run reward under that model, not a finite-sample, model-free bound on the actual realized SLO-violation rate under whatever traffic really shows up. Deep-RL and learned-threshold controllers (e.g., TopFull, ACM SIGCOMM 2024, verified by full-text fetch: a real, strong, per-API RL rate controller beating DAGOR and Breakwater on SLO compliance and P99 latency) adapt empirically but offer NO formal, finite-sample guarantee on the violation rate at all — their safety is entirely empirical, which is exactly why bad exploration or distribution shift causing an outage is a real deployment fear.

  There is a third paradigm — online/adaptive conformal prediction and, more specifically, Conformal Risk Control (Angelopoulos et al., ICLR 2024 / arXiv:2208.02814, verified by full-text fetch: controls the expected value of any bounded monotone loss at a target level via a threshold updated online, with a finite-sample distribution-free guarantee) and Adaptive Conformal Inference under distribution shift (Gibbs & Candes, NeurIPS 2021 / arXiv:2106.00170, verified by full-text fetch: a single-parameter online gradient update on the threshold that provably achieves the target coverage/violation frequency over long-run windows 'irrespective of the true data generating process', i.e. with NO exchangeability assumption, explicitly designed for distribution shift) — that has been developed almost entirely for PREDICTION-SET / abstention problems (e.g., which examples a classifier should abstain on) and has NOT, to the evidence found in this pass (targeted search combining 'conformal prediction' with 'admission control' / 'queue' / 'SLO' returned no matching prior work — a negative result that should be re-verified with a dedicated literature search before the paper draft, since absence of search hits is suggestive, not conclusive, of a genuine gap), been applied to REQUEST ADMISSION CONTROL for an overloaded system.

  This matters because the guarantee type is qualitatively different from, not just quantitatively better than, the existing paradigms: an operator can be told 'over any sufficiently long window, no more than alpha fraction of admitted requests will violate their SLO, provably, no matter what the traffic does' — a statement that neither a tuned RED/CoDel threshold, nor an index policy relying on a fitted queueing model, nor an RL policy trusted only empirically, can make. That is a genuinely different kind of admission-control policy, not a variant of index-based or RL-based control, and it is directly implementable and testable (the ACI update is a few lines of arithmetic per admission decision).
assumptions:
- >-
  A real-valued risk score s(x) — even if badly calibrated, even if it is just current-queue-depth or a crude predicted-service-time
  heuristic — is available cheaply at admission time and is at least weakly informative (monotonically associated with true
  SLO-violation probability), since the conformal guarantee controls the VIOLATION RATE via the threshold regardless of s(x)'s
  calibration quality, but a completely uninformative s(x) would still hit the target rate while admitting requests essentially
  at random, wasting the value-maximization benefit even though the safety guarantee holds.
- >-
  The true outcome (whether an admitted request actually violated its SLO) becomes observable within a bounded delay after
  the admission decision, so the ACI feedback loop (lambda_{t+1} depends on the realized outcome of request t) can be updated
  on a timescale fast relative to how quickly the traffic/service-time distribution shifts — if outcomes are observed only
  after a long delay (e.g., minutes), the threshold lags and the empirical guarantee applies to a longer effective window
  than the nominal one.
- >-
  The per-decision loss can be encoded as a single bounded scalar (e.g., 1 if the admitted request's realized latency exceeded
  its SLO target, 0 otherwise) — i.e., the object being controlled is genuinely reducible to a binary or bounded-monotone
  violation indicator rather than requiring joint control of multiple, potentially conflicting risk objectives simultaneously
  (multi-objective conformal risk control exists but adds complexity this hypothesis's Phase 1 deliberately avoids).
- >-
  Admitting or rejecting one request does not retroactively change whether ALREADY-admitted requests violate their SLO in
  a way that breaks the i.i.d.-ish per-decision feedback assumption underlying the ACI update — in a real queue this is only
  approximately true (admitting one more request does increase delay for others already in the queue), so the guarantee should
  be understood/tested as applying per-decision given the system's realized trajectory, not as a claim that admission decisions
  are causally independent of each other.
- >-
  Request 'value' (used only for the knapsack tie-break among conformal-eligible requests, not for the safety guarantee itself)
  is available or estimable at admission time; if unavailable, the policy degrades to FCFS among eligible requests while the
  SLO-violation-rate guarantee is unaffected.
investigation_approach: |-
  Phase 0 — Mechanism check on synthetic non-stationary traffic (fastest, highest-signal test first): Build a discrete-event simulator with several traffic regimes explicitly designed to be adversarial to a distributional-model assumption — a stationary Poisson baseline, a sudden 10x burst, a slow sinusoidal drift in load, a regime SWITCH with no warning, and a genuinely adversarial worst-case sequence constructed to try to break the threshold tracker. For each regime, run the ACI-based conformal admission controller (threshold updated per the Gibbs & Candes gradient rule) and measure the REALIZED empirical SLO-violation rate in rolling windows against the target alpha. This directly tests the headline claim (distribution-free violation-rate control) in the setting most likely to break it.

  Phase 1 — Baselines and value-maximization comparison: Implement strong baselines — (a) a fixed/offline-tuned threshold, (b) an index-based admission policy per the classical Nino-Mora-style construction assuming a (possibly mis-specified) queueing model, (c) a deep-RL admission controller (small PPO/DQN agent, comparable in spirit to TopFull's approach) trained on the stationary regime and then evaluated on all regimes including unseen ones, and (d) an offline-optimal oracle. Compare total accepted value AT MATCHED REALIZED SLO-violation rate across all traffic regimes — the key comparison is not 'who gets highest throughput in the regime they were tuned for' but 'who keeps their promised violation rate when the regime changes without warning', which is exactly where distributional/RL assumptions are expected to fail and the conformal guarantee is expected to hold by construction.

  Phase 2 — Sensitivity to score-function quality: Sweep the informativeness of s(x) from near-random (uninformative heuristic) to well-calibrated (an oracle-adjacent predictor), to empirically characterize the value-maximization degradation as a function of score quality while confirming the safety guarantee (target violation rate) holds across the entire sweep — this directly probes assumption 1 above.

  Phase 3 — Multi-class / value-aware knapsack layer: Implement and evaluate the value-maximizing tie-break layer (admit highest-value eligible requests within the per-interval conformal budget) versus FCFS-among-eligible, quantifying the value gain from value-awareness while re-confirming it does not affect the violation-rate guarantee (it should not, since value is only used to choose AMONG already-eligible requests, never to relax eligibility).

  Phase 4 (stretch) — Real-trace replay: Replay a public request trace with genuine non-stationarity/bursts (e.g., Azure Functions invocation trace or Alibaba cluster trace) through the simulator to check the synthetic-regime findings transfer to realistic autocorrelation and burst structure.
success_criteria: |-
  CONFIRMING evidence: (1) Across ALL tested traffic regimes (including the sudden-burst, drift, and regime-switch scenarios explicitly designed to break distributional assumptions), the realized rolling-window SLO-violation rate of the conformal admission controller tracks the target alpha within a small, pre-registered tolerance (e.g., within +/-3 percentage points after a bounded burn-in window) — while the fixed-threshold and queueing-index baselines show LARGER, regime-dependent deviations from alpha (e.g., spiking to 2x+ the target violation rate during the regime switch), and the RL baseline trained on the stationary regime shows measurable, non-recovering violation-rate degradation on the unseen-at-training-time regimes. (2) At matched realized violation rate, the conformal controller's accepted total value is competitive with (not necessarily beating, but not collapsing relative to) the index-based and RL baselines in the STATIONARY regime where those baselines have their best-case advantage, showing the safety guarantee is not purchased at a prohibitive throughput cost. (3) The value-aware knapsack layer (Phase 3) increases total accepted value relative to FCFS-among-eligible by a statistically significant margin (bootstrap CI excluding 0) while the violation-rate guarantee is statistically indistinguishable between the two variants.

  DISCONFIRMING evidence: (1) The realized violation rate deviates substantially and persistently from alpha in ANY tested regime (i.e., the theoretical distribution-free guarantee fails to manifest empirically at the tested update rate eta and outcome-observation delay), which would indicate either a bug in the ACI implementation or that the observation-delay/dependency assumptions (assumption 2 and 4 above) are violated badly enough in a real queue to break the guarantee in practice — this is the single most important thing to check first since it would invalidate the headline claim. (2) The value-maximization cost of the distribution-free guarantee is so large (e.g., >50% lower accepted value than the index/RL baselines even in the stationary regime at matched violation rate) that the guarantee is not practically worth adopting. (3) A focused literature re-search (beyond this pass's search) surfaces prior work that already applies online/adaptive conformal risk control to queue admission control, which would require repositioning the contribution as an application/extension rather than a new combination.

  PARTIAL confirmation: If the violation-rate guarantee holds robustly but only with a materially larger burn-in window or coarser tolerance than hoped, or holds well only for regimes without abrupt regime switches, this is still a valuable, precisely-characterized result about where distribution-free admission control earns its complexity relative to model-based alternatives.
related_works:
- >-
  Angelopoulos, A. N., Bates, S., et al. (2024) 'Conformal Risk Control' — ICLR 2024 / arXiv:2208.02814. VERIFIED BY FULL-TEXT
  FETCH: develops a threshold-selection procedure that controls the expected value of any bounded monotone loss at a target
  level alpha with a finite-sample, distribution-free guarantee, and an online/sequential variant that does not require exchangeability
  and adapts under distribution shift. This is the core mechanism this hypothesis repurposes for admission-decision thresholding
  rather than prediction-set construction; the paper itself does not address queueing, admission control, or systems/latency
  SLOs.
- >-
  Gibbs, I. & Candes, E. (2021) 'Adaptive Conformal Inference Under Distribution Shift' — NeurIPS 2021 / arXiv:2106.00170.
  VERIFIED BY FULL-TEXT FETCH (abstract): the single-parameter online gradient update this hypothesis's lambda_t recursion
  is built on, provably achieving the target coverage/violation frequency over long-run windows 'irrespective of the true
  data generating process' (no exchangeability assumption), explicitly targeting distribution shift. Applied in the original
  paper to prediction-interval coverage for forecasting-style problems, not to systems admission control.
- >-
  Nino-Mora, J. (2002) 'Dynamic allocation indices for restless projects and queueing admission control: a polyhedral approach'
  — Mathematical Programming 93, 361-413 (arXiv:2304.01946). VERIFIED BY FULL-TEXT FETCH (in a prior pass of this same investigation):
  derives marginal-productivity/Whittle-type indices for queueing admission control, but under an assumed known distributional
  (birth-death) model, with guarantees about expected long-run reward under that model — not a finite-sample, model-free bound
  on the realized violation rate under an unknown or adversarial arrival process, which is the qualitatively different guarantee
  this hypothesis targets.
- >-
  Park, J. et al. (2024) 'TopFull: An Adaptive Top-Down Overload Control for SLO-Oriented Microservices' — ACM SIGCOMM 2024
  (full PDF fetched in a prior pass: ina.kaist.ac.kr/assets/bibliography/Topfull.pdf). A real, strong, deep-RL-based per-API
  admission/rate controller reported to beat DAGOR and Breakwater on SLO compliance and P99 latency; confirmed to have no
  formal finite-sample violation-rate guarantee — its safety is empirical/learned, which is precisely the property this hypothesis's
  conformal approach targets as a point of qualitative difference, not merely a claim of superior average performance.
- >-
  Targeted search combining 'conformal prediction' / 'conformal risk control' with 'admission control', 'queue', and 'SLO'
  (this pass) returned no directly matching prior work applying online conformal risk control specifically to request admission
  control for overloaded queueing systems — noted here as a negative search result, which is suggestive of a genuine gap but
  should be treated as provisional and re-checked with a dedicated, broader literature search (including systems venues like
  SIGCOMM/OSDI/NSDI and the 'conformal prediction for systems' cross-over literature specifically) before the paper draft
  relies on it as a confirmed novelty claim.
inspiration: |-
  CONCEPTUAL (Level 1): The core transplant is reframing 'what threshold should I admit at?' from a MODEL-BASED question (assume a distribution, compute the optimal policy under it, as in queueing theory and RL) into a PURE FEEDBACK-CONTROL question over a single scalar (raise the bar when recent violations run hot, lower it when they run cold) that provably tracks a target rate with no distributional assumption at all — the same mental shift that separates classical statistical inference (assume a model) from conformal prediction (wrap any model, guarantee holds regardless of whether the model or the world's true distribution is right).

  PROCEDURAL (Level 2): The online conformal calibration loop — observe realized outcome, compute the indicator loss, take a bounded gradient step on the threshold, use the updated threshold for the next decision — is imported wholesale from adaptive conformal inference's prediction-interval-coverage workflow and repointed at a binary admit/reject decision with an SLO-violation loss instead of an interval-coverage loss.

  METHODOLOGICAL (Level 3): Two specific tools are imported directly and combined: (1) the Conformal Risk Control threshold-selection procedure and its finite-sample guarantee for bounded monotone losses (Angelopoulos et al. 2024), and (2) the Gibbs & Candes (2021) single-parameter online gradient update that extends this to non-exchangeable, distribution-shifting data — both imported without modification to the core update rule, with the systems-specific contribution being (a) the choice of loss (SLO violation given admission), (b) the score function design for a queueing context (queue-depth/predicted-service-time-based risk score), and (c) the value-aware knapsack layer built on top of the conformal eligibility set, which has no direct analogue in the source conformal-prediction literature.
terms:
- term: Admission control
  definition: >-
    The policy decision of whether to accept or reject an incoming request into a queue/service system, typically invoked
    when the system is at risk of overload.
- term: Conformal risk control
  definition: >-
    A method (Angelopoulos et al. 2024) for choosing a decision threshold that provably controls the expected value of a bounded,
    monotone loss function at a target level, with a finite-sample, distribution-free guarantee.
- term: Adaptive Conformal Inference (ACI)
  definition: >-
    An online procedure (Gibbs & Candes 2021) that updates a single threshold parameter via a bounded gradient step after
    each observed outcome, provably achieving a target long-run coverage/violation frequency without assuming the data are
    exchangeable or drawn from any fixed distribution.
- term: SLO (Service Level Objective) violation
  definition: >-
    The event that an admitted request's realized latency (or other measured quality-of-service metric) exceeds its target
    threshold; the bounded loss this hypothesis's conformal controller is designed to keep at a target rate alpha.
- term: Distribution-free guarantee
  definition: >-
    A statistical guarantee that holds for ANY underlying data-generating process (no assumption of a specific distribution
    family, e.g. Poisson arrivals or Markov-modulated service times), in contrast to queueing-theoretic guarantees that hold
    only under an assumed distributional model.
- term: Risk score s(x)
  definition: >-
    A cheap, possibly miscalibrated, real-valued function of a request's features and current system state (e.g., queue depth,
    predicted service time) used only to RANK requests by estimated SLO-violation risk; the conformal threshold, not the score's
    own calibration, is what provides the formal guarantee.
- term: Value-aware knapsack tie-break
  definition: >-
    Within the set of requests eligible for admission under the current conformal threshold, admitting the highest-value requests
    first (subject to capacity) rather than first-come-first-served, to maximize accepted value without altering the underlying
    violation-rate guarantee.
summary: >-
  This hypothesis proposes ADMISSION CONTROL VIA ONLINE CONFORMAL RISK CONTROL: instead of a queueing-theoretic index policy
  (which assumes a distributional model) or a deep-RL controller (which has no formal safety guarantee), maintain a single
  admission threshold updated by the Gibbs & Candes (2021) adaptive conformal-inference gradient rule so that the realized
  rate of SLO violations among admitted requests provably tracks a target level alpha over any long window, REGARDLESS of
  the true, unknown, non-stationary traffic and service-time process — with request value used only as a tie-break/knapsack
  layer among already-eligible requests, not affecting the safety guarantee. This is a genuinely different paradigm from bandit/index-based
  or RL-based admission control (verified via full-text-fetched prior work on both Nino-Mora-style index admission control
  and TopFull-style RL admission control, neither of which offers a finite-sample distribution-free violation-rate guarantee),
  and a targeted search found no prior work applying online conformal risk control specifically to queue admission control
  — a provisional novelty signal to be reconfirmed with deeper search. It is directly testable via discrete-event simulation
  designed specifically to probe robustness under sudden bursts, drift, and unannounced regime switches, comparing realized
  violation rate and accepted value against index-based, RL, and offline-optimal baselines.
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

--- Item 1 ---
id: art_fAlkDy9YEd-N
type: dataset
title: Real Azure Traffic Traces for Admission Control
summary: >-
  Standardized, schema-validated dataset (exp_sel_data_out.json format) for evaluating conformal admission-control policies
  under overloaded request queues. Built from the real Azure Functions 2019 invocation-per-minute and execution-duration-percentile
  trace (Shahrad et al., USENIX ATC 2020). Contains 210,000 request-level examples across 5 traffic regimes (stationary, burst,
  drift, regime_switch, adversarial); 4 regimes (168,000 examples) are derived from real trace windows selected for matching
  statistical signatures (low-CV for stationary, >=10x spike ratio for burst, sustained monotonic ramp for drift, hard-cut
  concatenation of two distinct real function windows for regime_switch), and only the adversarial regime (20,000 examples,
  ~9.5% of rows) is synthetically constructed and explicitly flagged via metadata_is_synthetic/metadata_provenance. Each example's
  `input` is a JSON string of admission-time-only features (arrival_time, risk_score, slo_target, regime_label, function_id,
  is_synthetic) and `output` is the binary SLO-violation label (1 iff the request's realized service_time exceeded its function's
  documented p99-derived slo_target), computed post-hoc from information excluded from `input` to avoid label leakage. The
  risk_score is a deliberately imperfect, documented heuristic computed from admission-time-only signals (coarse per-function
  service-time estimate plus queue-depth/arrival-rate proxy), matching the hypothesis's weakly-informative-but-miscalibrated-signal
  assumption. Per-example metadata_* fields carry the fold assignment, task type, class count, regime label, function id,
  request id, synthetic flag, provenance string, realized service_time, and slo_target, plus the ordered feature-name list,
  so downstream experiment code does not need to re-derive regime boundaries or the SLO/risk-score formulas. The full dataset
  is split into 4 part files (full_data_out/full_data_out_1.json..4.json, ~52,500 examples / ~50MB each) to stay under the
  100MB per-file limit; concatenate each part's `datasets[0].examples` list to reconstruct the complete 210,000-row dataset.
  mini_data_out.json and preview_data_out.json each hold 3 representative examples for quick inspection. Overall SLO-violation
  rate is 9.06%, varying meaningfully by regime (stationary 3.95%, burst 0.24%, drift 15.53%, regime_switch 3.09%, adversarial
  38.25%), giving a downstream admission-control policy genuine regime-dependent signal to exploit. All construction logic
  (source trace, per-regime selection criteria, SLO/risk-score formulas, synthetic-vs-real provenance) is documented in this
  summary and in data.py's docstring/comments, and the output passed exp_sel_data_out.json schema validation with zero errors
  and zero warnings.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 2 ---
id: art_oRyejQXIp14c
type: evaluation
title: Verdict on Conformal Admission Control
summary: >-
  This artifact (eval.py) produces the pre-registered statistical verdict on whether a conformal (ACI-based) admission controller
  tracks a target SLO-violation rate alpha=0.10 better than four baselines (a frozen fixed-score threshold, a misspecified
  queueing-index policy, a frozen policy trained only on stationary traffic, and a hindsight-optimal oracle) across five traffic
  regimes (stationary, burst, drift, regime-switch, adversarial). IMPORTANT DEPENDENCY NOTE: the required upstream dependencies
  (gen_art_dataset_1 and gen_art_experiment_1) were EMPTY directories at execution time -- no traffic dataset or experiment
  logs existed to evaluate. Rather than fabricate a verdict from nothing, eval.py self-generates a from-scratch, reproducible
  multi-regime traffic simulator and re-implements all 5 admission policies internally, following the same (policy, regime,
  seed) log contract the experiment plan describes, so the full evaluation pipeline runs on genuine simulated data. This is
  recorded verbatim in eval_out.json's metadata.dependency_status field so downstream paper-writing does not mistake this
  for an evaluation of an independently produced experiment. The pipeline computes, per (policy, regime): rolling violation
  rate over a 200-request window, mean absolute deviation (MAD) and max transient spike from alpha post-burn-in, and (for
  the regime-switch scenario) persistence-after-switch recovery time. It runs a moving-block bootstrap (2000 resamples, block
  length 200, concatenated across the 3 available seeds -- documented as block-over-time since seed count is below the 5 needed
  for over-seed bootstrap) to get 95% CIs on MAD and max-spike, then a paired significance test (conformal vs each baseline,
  per regime, same resample indices applied to both series) with Holm-Bonferroni correction across all 15 (regime, baseline)
  pairs. It separately checks the absolute 3-percentage-point tolerance criterion per regime, and flags whether the frozen
  RL baseline shows non-recovering degradation on regimes unseen at training time. For the stationary regime it re-thresholds
  each baseline to match conformal's realized violation rate and computes value_gap_pct with a bootstrap CI, flagging DISCONFIRMED
  only if the loss exceeds 50% with the CI lower bound also above 50% (a degenerate-denominator flag guards against a baseline
  whose rate-matched admission set collapses to near-zero size, which can otherwise blow up the percentage numerically without
  changing its sign). It also compares a value-aware knapsack admission variant against FCFS-among-eligible within conformal's
  eligibility set, checking the safety guarantee is statistically indistinguishable while the value gain is significant and
  positive. Outputs: eval_out.json (schema-validated against exp_eval_sol_out, contains per-policy-regime stats, paired significance
  tests, RL disconfirmer, matched-value comparison, knapsack check, and a top-level overall_verdict of CONFIRMED/PARTIALLY_CONFIRMED/DISCONFIRMED
  with plain-text justification -- current run: CONFIRMED, since conformal stayed within the 3pp tolerance in all 5 regimes,
  was Holm-corrected significantly better than baselines in 15/15 regime-baseline pairs, and no baseline's matched-value comparison
  crossed the 50% disconfirming threshold), a regime x policy summary_table.csv, and matplotlib PNG/PDF time-series figures
  (rolling violation rate vs alpha with a shaded tolerance band, one per regime, plus a dedicated regime-switch recovery-trajectory
  figure). Downstream paper-writing should prominently cite the dependency_status limitation alongside the verdict.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 2 artifacts were created THIS iteration.

id: art_fAlkDy9YEd-N
type: dataset
title: Real Azure Traffic Traces for Admission Control
summary: >-
  Standardized, schema-validated dataset (exp_sel_data_out.json format) for evaluating conformal admission-control policies
  under overloaded request queues. Built from the real Azure Functions 2019 invocation-per-minute and execution-duration-percentile
  trace (Shahrad et al., USENIX ATC 2020). Contains 210,000 request-level examples across 5 traffic regimes (stationary, burst,
  drift, regime_switch, adversarial); 4 regimes (168,000 examples) are derived from real trace windows selected for matching
  statistical signatures (low-CV for stationary, >=10x spike ratio for burst, sustained monotonic ramp for drift, hard-cut
  concatenation of two distinct real function windows for regime_switch), and only the adversarial regime (20,000 examples,
  ~9.5% of rows) is synthetically constructed and explicitly flagged via metadata_is_synthetic/metadata_provenance. Each example's
  `input` is a JSON string of admission-time-only features (arrival_time, risk_score, slo_target, regime_label, function_id,
  is_synthetic) and `output` is the binary SLO-violation label (1 iff the request's realized service_time exceeded its function's
  documented p99-derived slo_target), computed post-hoc from information excluded from `input` to avoid label leakage. The
  risk_score is a deliberately imperfect, documented heuristic computed from admission-time-only signals (coarse per-function
  service-time estimate plus queue-depth/arrival-rate proxy), matching the hypothesis's weakly-informative-but-miscalibrated-signal
  assumption. Per-example metadata_* fields carry the fold assignment, task type, class count, regime label, function id,
  request id, synthetic flag, provenance string, realized service_time, and slo_target, plus the ordered feature-name list,
  so downstream experiment code does not need to re-derive regime boundaries or the SLO/risk-score formulas. The full dataset
  is split into 4 part files (full_data_out/full_data_out_1.json..4.json, ~52,500 examples / ~50MB each) to stay under the
  100MB per-file limit; concatenate each part's `datasets[0].examples` list to reconstruct the complete 210,000-row dataset.
  mini_data_out.json and preview_data_out.json each hold 3 representative examples for quick inspection. Overall SLO-violation
  rate is 9.06%, varying meaningfully by regime (stationary 3.95%, burst 0.24%, drift 15.53%, regime_switch 3.09%, adversarial
  38.25%), giving a downstream admission-control policy genuine regime-dependent signal to exploit. All construction logic
  (source trace, per-regime selection criteria, SLO/risk-score formulas, synthetic-vs-real provenance) is documented in this
  summary and in data.py's docstring/comments, and the output passed exp_sel_data_out.json schema validation with zero errors
  and zero warnings.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

id: art_oRyejQXIp14c
type: evaluation
title: Verdict on Conformal Admission Control
summary: >-
  This artifact (eval.py) produces the pre-registered statistical verdict on whether a conformal (ACI-based) admission controller
  tracks a target SLO-violation rate alpha=0.10 better than four baselines (a frozen fixed-score threshold, a misspecified
  queueing-index policy, a frozen policy trained only on stationary traffic, and a hindsight-optimal oracle) across five traffic
  regimes (stationary, burst, drift, regime-switch, adversarial). IMPORTANT DEPENDENCY NOTE: the required upstream dependencies
  (gen_art_dataset_1 and gen_art_experiment_1) were EMPTY directories at execution time -- no traffic dataset or experiment
  logs existed to evaluate. Rather than fabricate a verdict from nothing, eval.py self-generates a from-scratch, reproducible
  multi-regime traffic simulator and re-implements all 5 admission policies internally, following the same (policy, regime,
  seed) log contract the experiment plan describes, so the full evaluation pipeline runs on genuine simulated data. This is
  recorded verbatim in eval_out.json's metadata.dependency_status field so downstream paper-writing does not mistake this
  for an evaluation of an independently produced experiment. The pipeline computes, per (policy, regime): rolling violation
  rate over a 200-request window, mean absolute deviation (MAD) and max transient spike from alpha post-burn-in, and (for
  the regime-switch scenario) persistence-after-switch recovery time. It runs a moving-block bootstrap (2000 resamples, block
  length 200, concatenated across the 3 available seeds -- documented as block-over-time since seed count is below the 5 needed
  for over-seed bootstrap) to get 95% CIs on MAD and max-spike, then a paired significance test (conformal vs each baseline,
  per regime, same resample indices applied to both series) with Holm-Bonferroni correction across all 15 (regime, baseline)
  pairs. It separately checks the absolute 3-percentage-point tolerance criterion per regime, and flags whether the frozen
  RL baseline shows non-recovering degradation on regimes unseen at training time. For the stationary regime it re-thresholds
  each baseline to match conformal's realized violation rate and computes value_gap_pct with a bootstrap CI, flagging DISCONFIRMED
  only if the loss exceeds 50% with the CI lower bound also above 50% (a degenerate-denominator flag guards against a baseline
  whose rate-matched admission set collapses to near-zero size, which can otherwise blow up the percentage numerically without
  changing its sign). It also compares a value-aware knapsack admission variant against FCFS-among-eligible within conformal's
  eligibility set, checking the safety guarantee is statistically indistinguishable while the value gain is significant and
  positive. Outputs: eval_out.json (schema-validated against exp_eval_sol_out, contains per-policy-regime stats, paired significance
  tests, RL disconfirmer, matched-value comparison, knapsack check, and a top-level overall_verdict of CONFIRMED/PARTIALLY_CONFIRMED/DISCONFIRMED
  with plain-text justification -- current run: CONFIRMED, since conformal stayed within the 3pp tolerance in all 5 regimes,
  was Holm-corrected significantly better than baselines in 15/15 regime-baseline pairs, and no baseline's matched-value comparison
  crossed the 50% disconfirming threshold), a regime x policy summary_table.csv, and matplotlib PNG/PDF time-series figures
  (rolling violation rate vs alpha with a shaded tolerance band, one per regime, plus a dedicated regime-switch recovery-trajectory
  figure). Downstream paper-writing should prominently cite the dependency_status limitation alongside the verdict.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

Overloaded request-serving systems -- a serverless function platform, a database connection pool, an API gateway in front of a microservice fleet -- must decide, for every incoming request, whether to admit it now or reject it before it consumes resources it cannot repay. The decision is an admission-control problem: choose a subset of arriving requests to serve so that the fraction of admitted requests that miss a latency service-level objective (SLO), such as a P99 response-time target, stays at or below an operator-chosen rate alpha, while admitting as much useful work as possible.

This problem matters at the scale modern platforms operate at. A function-as-a-service provider processes millions of invocations across thousands of distinct functions with wildly different, non-stationary load patterns; an operator who cannot bound the SLO-violation rate either over-provisions capacity to survive worst-case bursts, wasting most of it most of the time, or under-provisions and risks a violation cascade that a single bad five minutes of traffic can trigger.

The problem is hard because the traffic and service-time processes that determine whether a given admission decision will violate an SLO are not known in advance, are rarely stationary, and can change abruptly -- a deployment rolls out, a viral event drives a sudden spike, a co-located tenant's workload shifts the effective service rate. Any policy whose safety argument rests on a fitted model of that process is only as safe as the model's fit to the traffic that actually arrives, and the traffic that breaks the fit is exactly the traffic an operator most needs protection from.

The two paradigms in use today accept this fragility as the price of a formal argument, or drop the formal argument entirely. Queueing-theoretic and index-based controllers, including the classical Whittle-index construction for restless-bandit admission control [9] and its birth-death-model extension to queueing admission [3], derive elegant near-optimal policies -- but their optimality guarantee is a statement about expected long-run reward under an assumed distributional model of the arrival and service process, not a finite-sample bound on the violation rate actually realized when that model is wrong. Learned controllers such as TopFull [4], a reinforcement-learning admission and rate controller for SLO-oriented microservices reported to beat DAGOR- and Breakwater-style overload control on P99 latency, adapt empirically to whatever traffic a training run exposes them to -- but carry no finite-sample safety guarantee at all, so a distribution shift the policy did not see during training is a real, unbounded deployment risk rather than a bounded, quantified one.

This paper proposes and empirically tests a third paradigm, adapted from a distinct branch of statistics that has, to our knowledge, not previously been applied to admission control: online conformal risk control. Conformal Risk Control [1] and its online, non-exchangeable extension, Adaptive Conformal Inference (ACI) [2], choose a decision threshold by a feedback rule -- raise it when a monitored loss has recently run above target, lower it when it has run below -- that provably tracks a target loss rate over any long window, for any underlying data-generating process, with no distributional assumption and no requirement that the data be exchangeable. We repoint this threshold-tracking rule at the admission decision itself: a single scalar threshold, updated after every observed outcome, decides whether to admit a request whose cheap, possibly poorly calibrated risk score falls below it, so that the empirical SLO-violation rate among admitted requests tracks the target alpha regardless of how the traffic behaves. Because request value is used only to rank requests already judged eligible by this threshold -- a knapsack layer on top of, not a substitute for, the safety rule -- the resulting policy pursues throughput without weakening the guarantee it is built to hold.

[FIGURE:fig1]

We test this policy in a discrete-event simulator built on five traffic regimes -- a stationary baseline, a sudden burst, a slow drift, an unannounced regime switch, and a synthetically constructed adversarial sequence -- against four baselines: a frozen fixed-score threshold, a misspecified queueing-index policy, a reinforcement-learning controller frozen after training on the stationary regime only, and a hindsight-optimal oracle. Across all five regimes the conformal controller's realized violation rate stays within a pre-registered tolerance of the target alpha, while three of the four baselines break that tolerance the moment the regime is no longer stationary. At a violation rate matched to the conformal controller's own realized rate, the conformal policy's accepted value is statistically indistinguishable from the fixed-threshold and reinforcement-learning baselines even in the stationary regime where those baselines have their best-case advantage, so the distribution-free guarantee is not purchased at a large throughput cost. A value-aware layer built on top of the conformal eligibility set increases accepted value over first-come-first-served admission by a statistically significant margin while leaving the violation-rate guarantee unaffected.

## Summary of Contributions

- We introduce conformal admission control, an admission policy that repoints the Adaptive Conformal Inference threshold-tracking update onto the admit/reject decision for an SLO-violation loss, giving a finite-sample, distribution-free guarantee on the realized violation rate with no distributional model of the arrival or service process (Section 3).
- We evaluate the policy in a five-regime discrete-event simulator against a fixed threshold, an index-based queueing policy, a frozen reinforcement-learning controller, and a hindsight-optimal oracle, and show the conformal controller is the only non-oracle policy that stays within a pre-registered tolerance of the target violation rate in every regime (Section 5).
- We show that this safety margin is not bought at a large cost in accepted value: at matched realized violation rate in the stationary regime, the conformal policy's accepted value is statistically indistinguishable from the fixed-threshold and reinforcement-learning baselines (Section 5.3).
- We introduce and evaluate a value-aware admission layer that admits the highest-value eligible requests within the conformal budget rather than first-come-first-served, and show it raises accepted value with no measurable change to the violation-rate guarantee (Section 5.4).

# Related Work

**Conformal risk control and adaptive conformal inference.** Conformal prediction methods construct set-valued or thresholded predictions with a finite-sample, distribution-free coverage guarantee under the sole assumption that calibration and test data are exchangeable [6]. Conformal Risk Control [1] generalizes this to control the expected value of any bounded, monotone loss -- not only miscoverage -- at a target level, via a threshold chosen by inverting the empirical loss curve; it also gives an online variant for sequential, non-exchangeable data. Distribution-Free, Risk-Controlling Prediction Sets [7] independently develops a closely related threshold-selection framework with the same finite-sample guarantee for monotone losses, applied to prediction-set-valued outputs such as image segmentation and classification-with-rejection. Adaptive Conformal Inference (ACI) [2] removes the exchangeability assumption entirely: a single online gradient step on the threshold, using only the realized indicator of the current loss, provably drives the long-run average loss to the target rate irrespective of the true, possibly adversarial, data-generating process. Achieving Risk Control in Online Learning Settings [8] extends this line further with alternative online update rules for the threshold-tracking problem. All four papers develop and analyze this machinery for prediction-set construction or interval-coverage problems in forecasting and classification; none addresses systems admission control, queueing, or latency SLOs, and a targeted search of the conformal prediction literature crossed with admission-control and queueing terms surfaced no prior application of this machinery to request admission.

**Queueing-theoretic and index-based admission control.** The classical treatment of admission control as an optimal-stopping or restless-bandit problem dates to Whittle's index policy for restless bandits [9], later specialized to queueing admission control via a polyhedral, marginal-productivity index construction [3] that gives near-optimal expected long-run reward under an assumed birth-death arrival and service model. This family of results is a genuine engineering advance where the assumed model is a good fit, but its guarantee is conditional on that fit: it says nothing, finite-sample, about the realized violation rate when the true process departs from the assumed one, which is precisely the setting non-stationary production traffic creates.

**Learned and heuristic overload control.** Deep-reinforcement-learning and empirically tuned overload controllers, exemplified by TopFull [4] -- a per-API rate controller reported to outperform threshold-based systems such as DAGOR and Breakwater on SLO compliance and tail latency -- adapt their admission policy from observed system state without assuming a queueing model. Their safety is empirical: nothing in the training or deployment procedure bounds the violation rate a distribution-shifted test regime will realize, which is the property this paper's baselines are designed to probe directly by freezing a trained controller and exposing it to regimes it never saw during training.

**Real traffic traces.** The traffic regimes evaluated in this paper are built from the Azure Functions 2019 invocation and execution-duration trace [5], a widely used public characterization of a production serverless workload's non-stationary, bursty invocation pattern and per-function duration distribution.

# Preliminaries: Conformal Risk Control and Adaptive Conformal Inference

Conformal Risk Control [1] addresses the following problem: given a bounded, monotone loss function of a decision threshold, choose the threshold so that the expected loss is at most a target level alpha, with a finite-sample guarantee that holds regardless of the underlying data distribution, provided calibration and test examples are exchangeable. Adaptive Conformal Inference [2] removes the exchangeability requirement by replacing the batch threshold choice with an online update: after observing the loss incurred by the current threshold's decision, the threshold moves by a step proportional to the gap between the realized loss and the target rate alpha, in the direction that pushes the running average loss back toward alpha. Gibbs and Candes [2] show that this single-parameter update achieves the target long-run average loss rate over any window, for any sequence of losses -- including one generated adversarially -- because the update is a bounded, self-correcting feedback rule rather than an estimate of a fixed underlying distribution: if the realized loss rate over a recent window has run above alpha, the threshold tightens; if it has run below alpha, the threshold relaxes; and this correction has no dependence on any assumption about how future losses will be generated.

# Method: Conformal Admission Control

## Threshold-Tracking Admission Rule

We treat each arriving request x_t as carrying a cheap, real-valued risk score s(x_t), computed from information available at admission time only -- current queue depth, a coarse per-endpoint service-time estimate, and recent arrival-rate history -- that need not be well calibrated; the conformal guarantee below does not depend on s(x_t) being an accurate probability, only on it being a monotonic ranking signal correlated with true violation risk. The controller maintains a single scalar threshold lambda_t and admits request t if and only if s(x_t) is at most lambda_t. After the outcome of every admitted request becomes observable -- a bounded-delay indicator y_t in {0, 1} for whether its realized latency exceeded its SLO target -- the threshold updates by the Adaptive Conformal Inference gradient step

lambda_{t+1} = lambda_t + eta * (alpha - y_t),

where eta is a fixed step size and alpha is the target violation rate. When a recently admitted request violates its SLO (y_t = 1), the threshold tightens by eta * (1 - alpha); when it does not (y_t = 0), the threshold relaxes by eta * alpha. Because this update makes no reference to any assumed distribution over arrivals or service times -- it depends only on the realized outcome of the current decision -- the long-run average of y_t over any sufficiently long window converges to alpha regardless of whether the arrival process is stationary, drifting, or adversarially constructed, which is the property the experiments in Section 5 test directly rather than assume.

## Value-Aware Admission Layer

Within a fixed control interval, the conformal rule above defines an eligibility set: the requests with s(x) at or below lambda_t. When more requests are eligible than the system has capacity to serve in that interval, the safety guarantee is agnostic to which eligible requests are chosen -- it is a statement about the violation rate among whichever requests get admitted, not about which ones those are. We exploit this slack by ranking eligible requests within each interval by a request-level value signal (for example, a priority tier or billing weight) and admitting the highest-value requests first, up to capacity, rather than admitting in first-come-first-served (FCFS) order. This reduces to a bounded knapsack problem over the eligible set with capacity as the constraint; the eligibility set itself, and hence the violation-rate guarantee, is unchanged by which ranking is used inside it.

# Experimental Setup

## Traffic Regimes and Data

We built a discrete-event simulator on five traffic regimes designed to stress-test the distribution-free claim rather than to flatter it: a stationary regime with low load variance, a sudden burst regime with a large spike relative to baseline, a slow monotonic drift regime, an unannounced regime-switch scenario that concatenates two structurally different windows with no warning signal, and a synthetically constructed adversarial regime built specifically to try to break the threshold tracker. Four of the five regimes are grounded in a 210,000-request dataset built from the Azure Functions 2019 invocation and duration trace [5]: stationary, burst, drift, and regime-switch windows were selected from the real trace by matching statistical signatures (low coefficient of variation for stationary, a ten-times-or-larger spike ratio for burst, a sustained monotonic ramp for drift, and a hard concatenation of two distinct real function windows for regime-switch); the adversarial regime (roughly 9.5% of the dataset) is explicitly flagged as synthetic rather than trace-derived [ARTIFACT:art_fAlkDy9YEd-N]. Each request in this dataset carries admission-time-only features (arrival time, a deliberately imperfect risk-score heuristic, an SLO target, and a regime label) and a post-hoc binary SLO-violation label computed from the request's realized service time relative to its function's documented P99-derived target, with an overall violation rate of 9.06% that varies substantially by regime -- from 0.24% in the burst regime to 38.25% in the adversarial regime -- giving the admission policies genuine, regime-dependent signal to exploit or be confused by.

The controllers reported in Section 5 were evaluated in a self-contained instance of this same five-regime simulator design, run directly by the evaluation pipeline; the upstream dataset-construction and experiment-logging artifacts described above were empty at the time the evaluation ran, so the pipeline reconstructed a from-scratch multi-regime traffic generator and re-implemented all five admission policies internally rather than fabricate results from missing logs [ARTIFACT:art_oRyejQXIp14c]. Each (policy, regime) cell was run with 3 independent seeds of 3,000 requests each; a 95% confidence interval on every reported statistic was obtained by a moving-block bootstrap (block length 200, 2,000 resamples) over the concatenated seeds, since three seeds falls below the five needed for the plan's alternative over-seed bootstrap. We flag this substitution of a self-generated simulator for the originally planned trace-replay evaluation explicitly as a limitation in the Discussion, since the reported numbers characterize the policies' behavior under the same regime design as the trace-derived dataset rather than under the trace-derived dataset's exact realized values.

## Baselines and Metrics

We compare the conformal controller (target alpha = 0.10) against four baselines evaluated on the identical regime sequences: a fixed threshold calibrated once on the stationary regime and never updated; an index-based policy that admits below a fixed instantaneous-load threshold, representing a queueing-theoretic policy misspecified against the four non-stationary regimes it was not tuned for; a reinforcement-learning controller frozen after training only on the stationary regime, representing a learned policy exposed to unseen distribution shift at test time; and a hindsight-optimal oracle that re-thresholds each window to hit the target rate exactly, representing an upper bound unavailable to any online policy. For every (policy, regime) cell we report the rolling violation rate over a 200-request window, its mean absolute deviation (MAD) from alpha post burn-in, and the maximum transient spike above alpha; for the regime-switch scenario we additionally report whether the violation rate recovers to within tolerance after the switch. We pre-registered a tolerance of 3 percentage points (0.03) on MAD as the pass/fail criterion for the headline distribution-free claim, and used a paired, Holm-Bonferroni-corrected bootstrap significance test (conformal vs. each baseline, per regime) across all 15 (regime, baseline) comparisons.

# Results

## The Conformal Controller Tracks the Target Rate Across All Five Regimes

[FIGURE:fig2]

Table 1 and Figure 2 report the post-burn-in MAD from the target alpha = 0.10 for every (policy, regime) cell. The conformal controller stays within the pre-registered 3-percentage-point tolerance in all five regimes, with a MAD ranging from 0.0141 (burst) to 0.0194 (regime-switch) and a mean MAD of 0.0167 across regimes -- the only non-oracle policy to do so. The fixed threshold passes in the stationary and burst regimes (MAD 0.0250 and 0.0271) but fails once the regime departs from what it was calibrated on: MAD rises to 0.0332 in drift, 0.0426 in regime-switch, and 0.0331 in the adversarial regime, exceeding the 3-percentage-point tolerance in three of five regimes, and the regime-switch scenario shows non-recovering degradation -- none of its three seeds returns within tolerance before the regime ends. The index-based policy, representing a queueing-theoretic model misspecified against non-stationary load, fails the tolerance in every regime, with MAD an order of magnitude above the conformal controller's (0.1029 stationary, 0.1099 drift, 0.1291 regime-switch) and a maximum transient spike of 0.70 -- a violation rate seven times the target -- during the regime switch. The reinforcement-learning controller, frozen after training on the stationary regime, passes only in the regime it was trained on (MAD 0.0234) and fails in all four unseen regimes (0.0338 burst, 0.0420 drift, 0.0559 regime-switch, 0.0350 adversarial), confirming that its empirical adaptation does not transfer to distribution shift it was not exposed to during training. The hindsight-optimal oracle passes in all five regimes by construction, as expected of a policy with access to future information unavailable online.

| Regime | Conformal | Fixed threshold | Index-based | RL (frozen) | Oracle |
|---|---|---|---|---|---|
| Stationary | 0.0182 (pass) | 0.0250 (pass) | 0.1029 (fail) | 0.0234 (pass) | 0.0213 (pass) |
| Burst | 0.0141 (pass) | 0.0271 (pass) | 0.0823 (fail) | 0.0338 (fail) | 0.0195 (pass) |
| Drift | 0.0169 (pass) | 0.0332 (fail) | 0.1099 (fail) | 0.0420 (fail) | 0.0211 (pass) |
| Regime-switch | 0.0194 (pass) | 0.0426 (fail) | 0.1291 (fail) | 0.0559 (fail) | 0.0190 (pass) |
| Adversarial | 0.0150 (pass) | 0.0331 (fail) | 0.0759 (fail) | 0.0350 (fail) | 0.0195 (pass) |

*Table 1: Post-burn-in mean absolute deviation (MAD) from the target violation rate alpha = 0.10, per policy and regime, against the pre-registered 0.03 tolerance. n = 3 seeds x 3,000 requests per cell.*

A Holm-Bonferroni-corrected, paired bootstrap significance test comparing the conformal controller against the three non-oracle baselines across all 15 (regime, baseline) pairs finds the conformal controller significantly closer to alpha in 13 of 15 pairs (86.7%). The two exceptions are both in the stationary regime -- against the fixed threshold (p_holm = 0.098) and against the frozen RL controller (p_holm = 0.098) -- exactly the regime each of those two baselines was calibrated or trained on, and where they would be expected to perform closest to their best case. Against the index-based policy, the conformal controller is significantly better in every regime including stationary (p_holm < 0.001), since the index policy's fixed-load threshold is not itself protective of a per-request latency SLO even under stationary load.

## Distribution Shift Does Not Recover on Its Own

The regime-switch scenario isolates what happens when traffic changes with no warning signal the policy can use to anticipate it. The conformal controller's MAD in this regime (0.0194) is close to its mean across all other regimes, and its transient spike (0.0951, i.e., a realized rate of 0.195 at the single worst 200-request window) stays within the pre-registered tolerance band. The fixed threshold, by contrast, is flagged as non-recovering: across all three seeds, its rolling violation rate never returns to within tolerance before the regime-switch window ends, meaning the switch's effect on this policy's realized safety is not a transient the policy corrects, but a persistent shift. The frozen RL controller's post-switch MAD (0.0559) also exceeds tolerance, though one of its three seeds does recover within the regime's remaining requests (after 279 requests), indicating partial but incomplete adaptation. The index-based policy's post-switch behavior is the most severe: its maximum transient spike of 0.70 corresponds to a realized violation rate seven times the target immediately after the switch, and only one of its three seeds recovers within the regime.

## The Safety Guarantee Is Not Purchased at a Large Value Cost

[FIGURE:fig3]

A distribution-free guarantee is of limited practical use if it can only be bought by discarding most of the useful work a system could otherwise accept. To test this, we re-thresholded each baseline on the stationary regime -- the regime where each has its best-case advantage -- to match the conformal controller's own realized violation rate, then compared total accepted value. Figure 3 shows the resulting value gap. Against the fixed threshold, the conformal controller accepts 2.97% less total value, with a bootstrap 95% confidence interval of [-7.09%, 12.25%] that includes zero, so the two policies are not statistically distinguishable in accepted value at matched safety. Against the frozen RL controller, the conformal controller accepts 6.73% less value, again with a confidence interval ([-17.24%, 2.38%]) that includes zero. Against the hindsight-optimal oracle, the conformal controller accepts 7.91% less value ([-0.99%, 15.94%]), consistent with the oracle's structural advantage of re-thresholding with foreknowledge of the window's outcomes rather than tracking them online. None of these three comparisons crosses the pre-registered disconfirming threshold of a 50% value loss. The index-based policy is excluded from this comparison for a different reason: re-thresholding it to match the conformal controller's realized violation rate collapses its admission set to near zero -- it admits almost no requests at that rate -- so a percentage value gap against it is numerically degenerate rather than informative; the qualitative conclusion, that the conformal controller retains far more accepted value at the same safety level, still holds, but the magnitude does not meaningfully quantify a trade-off.

## The Value-Aware Admission Layer Adds Value Without Weakening Safety

[FIGURE:fig4]

We compared the value-aware admission rule against first-come-first-served (FCFS) admission within the same conformal eligibility set. The two variants' MAD from alpha are statistically indistinguishable: 0.0301 for FCFS versus 0.0316 for the value-aware variant, with a bootstrap 95% confidence interval on the difference ([-0.0023, 0.0058]) that includes zero, confirming that reordering admissions among already-eligible requests does not measurably affect the safety guarantee. Total accepted value, however, rises significantly: 1,862.99 for the value-aware variant versus 1,816.16 for FCFS, a 2.58% relative gain whose bootstrap 95% confidence interval on the absolute difference ([19.03, 86.55]) excludes zero.

# Discussion

The central empirical finding -- that a single scalar threshold, updated by nothing more than a bounded feedback step on the most recently observed outcome, tracks a target SLO-violation rate within a few percentage points across a stationary baseline, a sudden burst, a slow drift, an unannounced regime switch, and an adversarially constructed sequence -- is consistent with the theoretical claim behind Adaptive Conformal Inference [2]: the guarantee holds because the update corrects toward the target regardless of what generated the last outcome, not because it has modeled or anticipated what will generate the next one. The two baselines that fail this test both fail for the reason their design predicts: the fixed threshold is a snapshot of one regime's calibration frozen against every later regime, and the frozen RL controller is an empirical fit to the training regime with no correction mechanism once test-time traffic departs from it. The index-based policy's uniform failure, including in the stationary regime, indicates that a fixed load threshold is a poor proxy for a per-request latency SLO even absent any distribution shift, underscoring that the qualitative difference this paper argues for -- a threshold rule that reacts to the realized loss it is trying to control, rather than to a proxy for it -- matters independently of non-stationarity.

The two non-significant comparisons underlying Table 1 are informative rather than a weakness to explain away: both occur in the stationary regime, against the two baselines calibrated or trained on exactly that regime, which is the single condition under which a model-based or learned policy should be expected to compete with a distribution-free one. That the conformal controller is statistically indistinguishable from, rather than worse than, these baselines in their own best-case regime -- while remaining significantly better everywhere the regime shifts -- is the intended shape of the result: the guarantee costs little where the alternative already works, and it holds where the alternative does not.

**Limitations.** The evaluation reported in Section 5 was produced by a self-generated instance of the five-regime simulator design rather than a direct replay of the Azure-trace-derived dataset described in Section 4.1, because the dataset- and experiment-logging artifacts this evaluation was planned to consume were empty at the time it ran; the qualitative regime structure -- stationary, burst, drift, switch, and adversarial -- and target violation rate match the planned design, but the specific realized traffic and service-time values differ from the trace-derived dataset's own 210,000 logged requests. A direct replay of the conformal controller against that dataset, rather than a re-implementation of the regime generator, is needed to confirm the numbers reported here transfer unchanged to the originally collected trace. Second, every reported confidence interval is built from only three seeds per (policy, regime) cell via a block-over-time bootstrap rather than the five-seed over-seed bootstrap the evaluation plan preferred; wider seed coverage would tighten every interval reported in Table 1 and could plausibly turn one or both of the two non-significant stationary-regime comparisons significant, or leave them non-significant with a narrower interval -- the current data cannot distinguish between these. Third, the reinforcement-learning baseline is a single frozen policy trained once on the stationary regime; a continually retrained or online-fine-tuned RL controller might narrow the gap this paper reports without closing the qualitative distinction, since even a retrained learned policy would still lack a finite-sample guarantee on its retrained state. Finally, the outcome-observation delay in the simulator is effectively immediate, matching the assumption behind the ACI update; a production deployment where SLO violations are confirmed only after a longer delay would need the update rate eta re-tuned against that delay, and the guarantee would then apply to a correspondingly longer effective window than the nominal one.

# Conclusion

This paper shows that an admission-control policy built entirely from an online conformal-inference threshold update -- with no queueing model, no trained neural policy, and no exchangeability assumption -- holds a realized SLO-violation rate within 3 percentage points of a 10% target across five traffic regimes engineered to break distributional assumptions, including a sudden burst, a slow drift, and an unannounced regime switch, where a frozen fixed threshold, a misspecified queueing-index policy, and a frozen reinforcement-learning controller each measurably fail. This safety property is not bought at a large cost in accepted value: at matched realized violation rate in the regime where model-based and learned baselines have their best-case advantage, the conformal controller's accepted value is statistically indistinguishable from theirs. A value-aware admission layer built on top of the conformal eligibility set recovers a further, statistically significant gain in accepted value with no measurable change to the safety guarantee.

Future work includes: replaying the conformal controller directly against the trace-derived Azure Functions dataset built for this study rather than a re-implemented regime generator, to confirm transfer to the original logged requests; extending the single-scalar threshold to a small number of per-endpoint or per-tenant thresholds under a joint violation-rate budget; and characterizing the update rate eta's sensitivity to a bounded outcome-observation delay, which production systems where SLO confirmation lags the admission decision would require.

# References

[1] Angelopoulos, A. N., Bates, S., Fisch, A., Lei, L., & Schuster, T. (2022). Conformal Risk Control. *International Conference on Learning Representations*. arXiv:2208.02814.

[2] Gibbs, I., & Candes, E. (2021). Adaptive Conformal Inference Under Distribution Shift. *Neural Information Processing Systems*. arXiv:2106.00170.

[3] Nino-Mora, J. (2002). Dynamic Allocation Indices for Restless Projects and Queueing Admission Control: A Polyhedral Approach. *Mathematical Programming*, 93, 361-413.

[4] Park, J., Park, J., Jung, Y., Lim, H., Yeo, H., & Han, D. (2024). TopFull: An Adaptive Top-Down Overload Control for SLO-Oriented Microservices. *Proceedings of the ACM SIGCOMM 2024 Conference*.

[5] Shahrad, M., Fonseca, R., Goiri, I., Chaudhry, G., Batum, P., Cooke, J., Laureano, E., Tresness, C., Russinovich, M., & Bianchini, R. (2020). Serverless in the Wild: Characterizing and Optimizing the Serverless Workload at a Large Cloud Provider. *USENIX Annual Technical Conference*, 205-218.

[6] Angelopoulos, A. N., & Bates, S. (2021). A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification. arXiv:2107.07511.

[7] Bates, S., Angelopoulos, A. N., Lei, L., Malik, J., & Jordan, M. I. (2021). Distribution-Free, Risk-Controlling Prediction Sets. *Journal of the ACM*, 68, 43:1-43:34.

[8] Feldman, S., Ringel, L., Bates, S., & Romano, Y. (2022). Achieving Risk Control in Online Learning Settings. *Transactions on Machine Learning Research*.

[9] Whittle, P. (1988). Restless Bandits: Activity Allocation in a Changing World. *Journal of Applied Probability*, 25, 287-298.
</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (evidence) The reported results were not produced against the real, trace-derived dataset the paper spends a full subsection (4.1) and a full artifact (art_fAlkDy9YEd-N) describing. Because that dataset and the experiment-logging artifact were empty at evaluation time, eval.py self-generated its own multi-regime traffic simulator and re-implemented all five policies (including the conformal controller under test) from scratch. The paper discloses this in a limitations paragraph, but the framing throughout the Introduction, Experimental Setup, and Results ('four of the five regimes are grounded in a 210,000-request dataset...') reads, until that disclosure, as though the reported Table 1 numbers come from that dataset. They do not.
  Action: Either (a) re-run the full evaluation against the actual trace-derived dataset and report those numbers as the headline result, moving the current self-generated numbers to an appendix as a robustness check, or (b) if that is not feasible in this iteration, restructure the paper so the self-generated nature of the evaluation is stated in the abstract and at the top of Section 5, not only in the Limitations paragraph near the end -- a reader should not need to reach the Discussion to learn that the headline table is not evaluated on the dataset the paper spent a subsection constructing.
- [MAJOR] (rigor) The eval.py artifact that produces the paper's results implements both the policies under test (including the proposed conformal controller) and the traffic/label generator used to score them, in the same self-contained script, with no independently produced ground truth. This creates a structural risk that the evaluator's assumptions about what 'a violation' or 'a regime' looks like are baked identically into both the data-generating process and the policies being compared, which could inflate or bias the reported gaps in ways an externally sourced trace would not.
  Action: Have an independent script (or, at minimum, a script written before and frozen against the policy implementations) generate the traffic and ground-truth labels, and only then run the five policies against that frozen dataset, so the comparison is not self-referential. Report a hash or fixed seed manifest so a third party could reproduce the exact traffic sequence independently of the evaluation code.
- [MAJOR] (methodology) The paper states the ACI convergence property only by natural-language paraphrase and citation ('Gibbs and Candes [2] show that this single-parameter update achieves the target long-run average loss rate...'), with no theorem statement, no explicit assumptions (e.g., loss boundedness in [0,1], fixed vs. adaptive step size, the exact non-asymptotic bound), and no proof sketch connecting the admission-control setting's specific loss (a delayed binary SLO-violation indicator) to the assumptions under which the cited result actually holds.
  Action: Add a short formal subsection in Section 3 stating the guarantee as an explicit theorem (with citation) in the paper's own notation for lambda_t, y_t, alpha, and eta, including the finite-sample bound on |average(y_t) - alpha| over a window of length T as a function of eta and the loss range, and explicitly verify that the admission-control setting (bounded-delay binary outcome) satisfies the theorem's preconditions.
- [MINOR] (evidence) Statistical power is limited: only 3 independent seeds per (policy, regime) cell, below the 5 the evaluation plan itself identifies as the threshold for its preferred over-seed bootstrap, forcing a fallback to a block-over-time bootstrap. The paper's own Limitations section notes this could plausibly flip one or both of the two non-significant stationary-regime comparisons.
  Action: Increase to at least 5 seeds per cell (as the evaluation plan originally specified) to use the intended over-seed bootstrap and tighten the confidence intervals on the two borderline stationary-regime comparisons.
- [MINOR] (clarity) The risk score s(x_t) is described only qualitatively ('current queue depth, a coarse per-endpoint service-time estimate, and recent arrival-rate history') with no formula, update cadence, or computational cost analysis, despite the paper's practical claim that it is 'cheap' -- a reader cannot judge how cheap, or reproduce it, from the text given.
  Action: Give the exact functional form (or pseudocode) used to compute s(x_t) in the artifact, its computational complexity per request, and how it is updated online, either in the Method section or an appendix.
- [MINOR] (clarity) The step size eta is never given a numeric value anywhere in the paper, nor is any sensitivity analysis over it provided, even though the Discussion explicitly identifies eta as the parameter that would need re-tuning under delayed outcome observation -- a reader cannot assess how sensitive the headline results are to this choice.
  Action: Report the eta value(s) used in Section 5 and add a small sensitivity sweep (e.g., 3-5 values) showing how MAD-from-target and transient spike size trade off against eta, at least for the regime-switch and adversarial regimes where responsiveness matters most.
- [MINOR] (novelty) Related work stops citing the online/adaptive conformal literature at 2022 (Gibbs & Candes; Feldman et al.). Given the field's activity since then on strongly-adaptive and multi-window online conformal tracking, the paper cannot currently claim it has selected the strongest available threshold-tracking rule to repoint at admission control, only that it used a specific well-known one.
  Action: Add a paragraph acknowledging post-2022 online conformal tracking variants and either justify the plain ACI update as the appropriate baseline choice for this first application, or note the newer variants as a natural extension (this can be folded into the existing Future Work paragraph).
- [MINOR] (scope) The introduction motivates the problem at the scale of 'a function-as-a-service provider processes millions of invocations across thousands of distinct functions,' but the method and evaluation operate a single scalar threshold shared across all traffic, and multi-endpoint/multi-tenant thresholding under a joint budget is explicitly deferred to future work. The gap between the motivating scale and the evaluated scope is large and not flagged until the very end of the paper.
  Action: Either narrow the introduction's motivating scenario to match the single-threshold scope actually evaluated, or move the multi-endpoint caveat earlier (e.g., into the Introduction or Method) so the reader is not left assuming per-function guarantees that the paper does not test.
</reviewer_feedback>



<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the field's landscape, prior work, crowded lanes, and the novelty bar — consult it while revising so the updated hypothesis stays genuinely novel and well-positioned.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-25 18:38:20 UTC

```
Find a better admission control policy for overloaded request queues.
```

### [4] TOOL CALL — Write · 2026-08-25 18:38:48 UTC

```
File: /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json

{
  "title": "Conformal Admission Control for Overloaded Queues",
  "hypothesis": "An admission control policy built on ONLINE CONFORMAL RISK CONTROL -- not queueing theory, not reinforcement learning -- can hold a hard, distribution-free, finite-sample guarantee on the long-run rate of SLO violations (e.g., 'no more than alpha fraction of admitted requests exceed their P99 latency target') while maximizing throughput/value, under traffic and service-time distributions that are unknown, non-stationary, and possibly adversarial -- with NO assumption of exchangeability, no fitted queueing model, and no trained neural policy.\n\nConcretely: at admission time, a cheap, possibly miscalibrated risk score s(x) is computed by an explicit, documented, closed-form heuristic (queue depth + coarse per-endpoint service-time estimate; exact formula and O(1) per-request cost fixed in advance and reported, not just described qualitatively). The system does NOT trust s(x)'s calibration. It maintains a single scalar threshold lambda_t, updated after every observed outcome via the Adaptive Conformal Inference (ACI) gradient step lambda_{t+1} = lambda_t + eta * (alpha - y_t), with a FIXED, reported numeric eta (and a small pre-registered sensitivity sweep over eta, e.g. 3-5 values) rather than an unstated constant; admit iff s(x) <= lambda_t. Because this is a feedback-controlled quantile-tracking rule, it inherits the Gibbs & Candes (2021) finite-sample guarantee -- STATED IN THIS PAPER AS AN EXPLICIT THEOREM, in the paper's own notation (lambda_t, y_t in {0,1}, alpha, eta, window length T), including the non-asymptotic bound on |mean(y_t) - alpha| as a function of eta and the [0,1] loss range, with an explicit check that the admission-control setting's bounded-delay binary SLO-violation indicator satisfies the theorem's preconditions -- that the empirical SLO-violation rate over any long window converges to alpha REGARDLESS of the true, unknown, non-stationary process, a guarantee no queueing-theoretic or RL policy can offer. Request VALUE heterogeneity enters only as a tie-break/knapsack layer within the conformal-eligible set each control interval, never relaxing the safety rule.\n\nSCOPE, narrowed by iteration-1 evidence: the evaluated and claimed guarantee is for a SINGLE shared scalar threshold over one queue/endpoint class, not a per-function or per-tenant guarantee at the fleet scale the motivation invokes; multi-threshold extension under a joint budget remains future work and must be stated as such in the Introduction, not only at the end of the paper.\n\nEVIDENTIARY STATUS after iteration 1: the headline numbers (Table 1: conformal MAD 0.014-0.019 across 5 regimes, within the pre-registered 0.03 tolerance, vs. fixed-threshold/index-based/frozen-RL baselines failing in 3-4 of 5 regimes; value cost at matched safety statistically indistinguishable from baselines; value-aware layer +2.58% value with unchanged safety) were produced by eval.py's SELF-GENERATED multi-regime traffic simulator and SELF-REIMPLEMENTED policies, NOT against the real Azure-trace-derived 210,000-request dataset (art_fAlkDy9YEd-N) that was separately, successfully constructed but sat unconsumed because gen_art_experiment_1 never ran. This is a genuine gap, not a cosmetic one: the same script both generates ground truth and implements the policy under test, which is a structural risk of self-referential inflation the next iteration must close by (a) running an independently-authored experiment script against the frozen, already-built trace-derived dataset (art_fAlkDy9YEd-N) as the PRIMARY evaluation, with the self-generated simulator numbers demoted to a robustness-check appendix, and (b) increasing seed count to >=5 per (policy, regime) cell to use the over-seed bootstrap the plan originally specified, tightening the two currently non-significant stationary-regime comparisons (conformal vs. fixed-threshold p_holm=0.098; vs. frozen-RL p_holm=0.098).",
  "relation_type": "evolution",
  "relation_rationale": "Same conceptual frame (ACI-based admission control); narrowed to single-threshold scope, added formal theorem + eta/score specificity per reviewer.",
  "confidence_delta": "unchanged",
  "key_changes": [
    "Flagged as unresolved: the reported Table 1 results are from a self-generated simulator/self-reimplemented policies inside eval.py, not from the already-built real Azure-trace dataset (art_fAlkDy9YEd-N), which sat unused because the experiment artifact never ran -- next iteration must run an independent experiment against that frozen dataset as the primary result.",
    "Named the structural self-referential risk (same script generates data and implements the tested policy) and required an independently-authored data/label generator going forward.",
    "Required the ACI convergence claim be stated as an explicit theorem with notation and a non-asymptotic bound, not just paraphrase-and-cite, with preconditions explicitly checked against the bounded-delay binary-outcome setting.",
    "Required s(x) to be given as an explicit closed-form/pseudocode with per-request cost, and eta to be reported as a concrete numeric value with a small sensitivity sweep, rather than described only qualitatively.",
    "Narrowed scope: the guarantee as evaluated is for a single shared scalar threshold on one queue, and the Introduction must state this scope up front rather than motivating at fleet/multi-tenant scale and deferring the gap to the end.",
    "Required increasing seeds to >=5 per (policy, regime) cell to use the originally-planned over-seed bootstrap and tighten the two currently non-significant stationary-regime comparisons.",
    "Retained the core mechanism and headline claim unchanged, since the underlying result (where it was actually tested) held: conformal control was the only non-oracle policy within tolerance across all five regimes."
  ],
  "artifact_relations": []
}
```

### [5] TOOL RESULT — Write · 2026-08-25 18:38:48 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Conformal Admission Control for Overloaded Queues\",\n  \"hypothesis\": \"An admission control policy built on ONLINE CONFORMAL RISK CONTROL -- not queueing theory, not reinforcement learning -- can hold a hard, distribution-free, finite-sample guarantee on the long-run rate of SLO violations (e.g., 'no more than alpha fraction of admitted requests exceed their P99 latency target') while maximizing throughput/value, under traffic and service-time distributions that are unknown, non-stationary, and possibly adversarial -- with NO assumption of exchangeability, no fitted queueing model, and no trained neural policy.\\n\\nConcretely: at admission time, a cheap, possibly miscalibrated risk score s(x) is computed by an explicit, documented, closed-form heuristic (queue depth + coarse per-endpoint service-time estimate; exact formula and O(1) per-request cost fixed in advance and reported, not just described qualitatively). The system does NOT trust s(x)'s calibration. It maintains a single scalar threshold lambda_t, updated after every observed outcome via the Adaptive Conformal Inference (ACI) gradient step lambda_{t+1} = lambda_t + eta * (alpha - y_t), with a FIXED, reported numeric eta (and a small pre-registered sensitivity sweep over eta, e.g. 3-5 values) rather than an unstated constant; admit iff s(x) <= lambda_t. Because this is a feedback-controlled quantile-tracking rule, it inherits the Gibbs & Candes (2021) finite-sample guarantee -- STATED IN THIS PAPER AS AN EXPLICIT THEOREM, in the paper's own notation (lambda_t, y_t in {0,1}, alpha, eta, window length T), including the non-asymptotic bound on |mean(y_t) - alpha| as a function of eta and the [0,1] loss range, with an explicit check that the admission-control setting's bounded-delay binary SLO-violation indicator satisfies the theorem's preconditions -- that the empirical SLO-violation rate over any long window converges to alpha REGARDLESS of the true, unknown, non-stationary process, a guarantee no queueing-theoretic or RL policy can offer. Request VALUE heterogeneity enters only as a tie-break/knapsack layer within the conformal-eligible set each control interval, never relaxing the safety rule.\\n\\nSCOPE, narrowed by iteration-1 evidence: the evaluated and claimed guarantee is for a SINGLE shared scalar threshold over one queue/endpoint class, not a per-function or per-tenant guarantee at the fleet scale the motivation invokes; multi-threshold extension under a joint budget remains future work and must be stated as such in the Introduction, not only at the end of the paper.\\n\\nEVIDENTIARY STATUS after iteration 1: the headline numbers (Table 1: conformal MAD 0.014-0.019 across 5 regimes, within the pre-registered 0.03 tolerance, vs. fixed-threshold/index-based/frozen-RL baselines failing in 3-4 of 5 regimes; value cost at matched safety statistically indistinguishable from baselines; value-aware layer +2.58% value with unchanged safety) were produced by eval.py's SELF-GENERATED multi-regime traffic simulator and SELF-REIMPLEMENTED policies, NOT against the real Azure-trace-derived 210,000-request dataset (art_fAlkDy9YEd-N) that was separately, successfully constructed but sat unconsumed because gen_art_experiment_1 never ran. This is a genuine gap, not a cosmetic one: the same script both generates ground truth and implements the policy under test, which is a structural risk of self-referential inflation the next iteration must close by (a) running an independently-authored experiment script against the frozen, already-built trace-derived dataset (art_fAlkDy9YEd-N) as the PRIMARY evaluation, with the self-generated simulator numbers demoted to a robustness-check appendix, and (b) increasing seed count to >=5 per (policy, regime) cell to use the over-seed bootstrap the plan originally specified, tightening the two currently non-significant stationary-regime comparisons (conformal vs. fixed-threshold p_holm=0.098; vs. frozen-RL p_holm=0.098).\",\n  \"relation_type\": \"evolution\",\n  \"relation_rationale\": \"Same conceptual frame (ACI-based admission control); narrowed to single-threshold scope, added formal theorem + eta/score specificity per reviewer.\",\n  \"confidence_delta\": \"unchanged\",\n  \"key_changes\": [\n    \"Flagged as unresolved: the reported Table 1 results are from a self-generated simulator/self-reimplemented policies inside eval.py, not from the already-built real Azure-trace dataset (art_fAlkDy9YEd-N), which sat unused because the experiment artifact never ran -- next iteration must run an independent experiment against that frozen dataset as the primary result.\",\n    \"Named the structural self-referential risk (same script generates data and implements the tested policy) and required an independently-authored data/label generator going forward.\",\n    \"Required the ACI convergence claim be stated as an explicit theorem with notation and a non-asymptotic bound, not just paraphrase-and-cite, with preconditions explicitly checked against the bounded-delay binary-outcome setting.\",\n    \"Required s(x) to be given as an explicit closed-form/pseudocode with per-request cost, and eta to be reported as a concrete numeric value with a small sensitivity sweep, rather than described only qualitatively.\",\n    \"Narrowed scope: the guarantee as evaluated is for a single shared scalar threshold on one queue, and the Introduction must state this scope up front rather than motivating at fleet/multi-tenant scale and deferring the gap to the end.\",\n    \"Required increasing seeds to >=5 per (policy, regime) cell to use the originally-planned over-seed bootstrap and tighten the two currently non-significant stationary-regime comparisons.\",\n    \"Retained the core mechanism and headline claim unchanged, since the underlying result (where it was actually tested) held: conformal control was the only non-oracle policy within tolerance across all five regimes.\"\n  ],\n  \"artifact_relations\": []\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [6] ASSISTANT · 2026-08-25 18:38:50 UTC

```
Done — revised hypothesis written to `.terminal_claude_agent_struct_out.json`, keeping the core conformal-admission-control claim (evolution, not replacement) but narrowing scope to single-threshold, requiring the theorem statement, explicit s(x)/eta, and flagging that next iteration must evaluate against the already-built real trace dataset instead of the self-generated simulator.
```

### [7] SYSTEM-USER prompt · 2026-08-25 18:38:52 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `relation_rationale`: 'Same conceptual frame (ACI-based admission control); narrowed to single-threshold scope, added formal theorem + eta/score specificity per reviewer.' is too long (at most 120 characters, got 147)
Every required field must be present and every field type must match the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```

### [8] TOOL CALL — Edit · 2026-08-25 18:38:56 UTC

```
File: /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json
OLD:   "relation_rationale": "Same conceptual frame (ACI-based admission control); narrowed to single-threshold scope, added formal theorem + eta/score specificity per reviewer.",
NEW:   "relation_rationale": "Same ACI frame; narrowed to single threshold, added theorem + eta/score specificity per reviewer.",
```

### [9] TOOL RESULT — Edit · 2026-08-25 18:38:56 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json", "oldString": "  \"relation_rationale\": \"Same conceptual frame (ACI-based admission control); narrowed to single-threshold scope, added formal theorem + eta/score specificity per reviewer.\",", "newString": "  \"relation_rationale\": \"Same ACI frame; narrowed to single threshold, added theorem + eta/score specificity per reviewer.\",", "originalFile": "{\n  \"title\": \"Conformal Admission Control for Overloaded Queues\",\n  \"hypothesis\": \"An admission control policy built on ONLINE CONFORMAL RISK CONTROL -- not queueing theory, not reinforcement learning -- can hold a hard, distribution-free, finite-sample guarantee on the long-run rate of SLO violations (e.g., 'no more than alpha fraction of admitted requests exceed their P99 latency target') while maximizing throughput/value, under traffic and service-time distributions that are unknown, non-stationary, and possibly adversarial -- with NO assumption of exchangeability, no fitted queueing model, and no trained neural policy.\\n\\nConcretely: at admission time, a cheap, possibly miscalibrated risk score s(x) is computed by an explicit, documented, closed-form heuristic (queue depth + coarse per-endpoint service-time estimate; exact formula and O(1) per-request cost fixed in advance and reported, not just described qualitatively). The system does NOT trust s(x)'s calibration. It maintains a single scalar threshold lambda_t, updated after every observed outcome via the Adaptive Conformal Inference (ACI) gradient step lambda_{t+1} = lambda_t + eta * (alpha - y_t), with a FIXED, reported numeric eta (and a small pre-registered sensitivity sweep over eta, e.g. 3-5 values) rather than an unstated constant; admit iff s(x) <= lambda_t. Because this is a feedback-controlled quantile-tracking rule, it inherits the Gibbs & Candes (2021) finite-sample guarantee -- STATED IN THIS PAPER AS AN EXPLICIT THEOREM, in the paper's own notation (lambda_t, y_t in {0,1}, alpha, eta, window length T), including the non-asymptotic bound on |mean(y_t) - alpha| as a function of eta and the [0,1] loss range, with an explicit check that the admission-control setting's bounded-delay binary SLO-violation indicator satisfies the theorem's preconditions -- that the empirical SLO-violation rate over any long window converges to alpha REGARDLESS of the true, unknown, non-stationary process, a guarantee no queueing-theoretic or RL policy can offer. Request VALUE heterogeneity enters only as a tie-break/knapsack layer within the conformal-eligible set each control interval, never relaxing the safety rule.\\n\\nSCOPE, narrowed by iteration-1 evidence: the evaluated and claimed guarantee is for a SINGLE shared scalar threshold over one queue/endpoint class, not a per-function or per-tenant guarantee at the fleet scale the motivation invokes; multi-threshold extension under a joint budget remains future work and must be stated as such in the Introduction, not only at the end of the paper.\\n\\nEVIDENTIARY STATUS after iteration 1: the headline numbers (Table 1: conformal MAD 0.014-0.019 across 5 regimes, within the pre-registered 0.03 tolerance, vs. fixed-threshold/index-based/frozen-RL baselines failing in 3-4 of 5 regimes; value cost at matched safety statistically indistinguishable from baselines; value-aware layer +2.58% value with unchanged safety) were produced by eval.py's SELF-GENERATED multi-regime traffic simulator and SELF-REIMPLEMENTED policies, NOT against the real Azure-trace-derived 210,000-request dataset (art_fAlkDy9YEd-N) that was separately, successfully constructed but sat unconsumed because gen_art_experiment_1 never ran. This is a genuine gap, not a cosmetic one: the same script both generates ground truth and implements the policy under test, which is a structural risk of self-referential inflation the next iteration must close by (a) running an independently-authored experiment script against the frozen, already-built trace-derived dataset (art_fAlkDy9YEd-N) as the PRIMARY evaluation, with the self-generated simulator numbers demoted to a robustness-check appendix, and (b) increasing seed count to >=5 per (policy, regime) cell to use the over-seed bootstrap the plan originally specified, tightening the two currently non-significant stationary-regime comparisons (conformal vs. fixed-threshold p_holm=0.098; vs. frozen-RL p_holm=0.098).\",\n  \"relation_type\": \"evolution\",\n  \"relation_rationale\": \"Same conceptual frame (ACI-based admission control); narrowed to single-threshold scope, added formal theorem + eta/score specificity per reviewer.\",\n  \"confidence_delta\": \"unchanged\",\n  \"key_changes\": [\n    \"Flagged as unresolved: the reported Table 1 results are from a self-generated simulator/self-reimplemented policies inside eval.py, not from the already-built real Azure-trace dataset (art_fAlkDy9YEd-N), which sat unused because the experiment artifact never ran -- next iteration must run an independent experiment against that frozen dataset as the primary result.\",\n    \"Named the structural self-referential risk (same script generates data and implements the tested policy) and required an independently-authored data/label generator going forward.\",\n    \"Required the ACI convergence claim be stated as an explicit theorem with notation and a non-asymptotic bound, not just paraphrase-and-cite, with preconditions explicitly checked against the bounded-delay binary-outcome setting.\",\n    \"Required s(x) to be given as an explicit closed-form/pseudocode with per-request cost, and eta to be reported as a concrete numeric value with a small sensitivity sweep, rather than described only qualitatively.\",\n    \"Narrowed scope: the guarantee as evaluated is for a single shared scalar threshold on one queue, and the Introduction must state this scope up front rather than motivating at fleet/multi-tenant scale and deferring the gap to the end.\",\n    \"Required increasing seeds to >=5 per (policy, regime) cell to use the originally-planned over-seed bootstrap and tighten the two currently non-significant stationary-regime comparisons.\",\n    \"Retained the core mechanism and headline claim unchanged, since the underlying result (where it was actually tested) held: conformal control was the only non-oracle policy within tolerance across all five regimes.\"\n  ],\n  \"artifact_relations\": []\n}\n", "structuredPatch": [{"oldStart": 2, "oldLines": 7, "newStart": 2, "newLines": 7, "lines": ["   \"title\": \"Conformal Admission Control for Overloaded Queues\",", "   \"hypothesis\": \"An admission control policy built on ONLINE CONFORMAL RISK CONTROL -- not queueing theory, not reinforcement learning -- can hold a hard, distribution-free, finite-sample guarantee on the long-run rate of SLO violations (e.g., 'no more than alpha fraction of admitted requests exceed their P99 latency target') while maximizing throughput/value, under traffic and service-time distributions that are unknown, non-stationary, and possibly adversarial -- with NO assumption of exchangeability, no fitted queueing model, and no trained neural policy.\\n\\nConcretely: at admission time, a cheap, possibly miscalibrated risk score s(x) is computed by an explicit, documented, closed-form heuristic (queue depth + coarse per-endpoint service-time estimate; exact formula and O(1) per-request cost fixed in advance and reported, not just described qualitatively). The system does NOT trust s(x)'s calibration. It maintains a single scalar threshold lambda_t, updated after every observed outcome via the Adaptive Conformal Inference (ACI) gradient step lambda_{t+1} = lambda_t + eta * (alpha - y_t), with a FIXED, reported numeric eta (and a small pre-registered sensitivity sweep over eta, e.g. 3-5 values) rather than an unstated constant; admit iff s(x) <= lambda_t. Because this is a feedback-controlled quantile-tracking rule, it inherits the Gibbs & Candes (2021) finite-sample guarantee -- STATED IN THIS PAPER AS AN EXPLICIT THEOREM, in the paper's own notation (lambda_t, y_t in {0,1}, alpha, eta, window length T), including the non-asymptotic bound on |mean(y_t) - alpha| as a function of eta and the [0,1] loss range, with an explicit check that the admission-control setting's bounded-delay binary SLO-violation indicator satisfies the theorem's preconditions -- that the empirical SLO-violation rate over any long window converges to alpha REGARDLESS of the true, unknown, non-stationary process, a guarantee no queueing-theoretic or RL policy can offer. Request VALUE heterogeneity enters only as a tie-break/knapsack layer within the conformal-eligible set each control interval, never relaxing the safety rule.\\n\\nSCOPE, narrowed by iteration-1 evidence: the evaluated and claimed guarantee is for a SINGLE shared scalar threshold over one queue/endpoint class, not a per-function or per-tenant guarantee at the fleet scale the motivation invokes; multi-threshold extension under a joint budget remains future work and must be stated as such in the Introduction, not only at the end of the paper.\\n\\nEVIDENTIARY STATUS after iteration 1: the headline numbers (Table 1: conformal MAD 0.014-0.019 across 5 regimes, within the pre-registered 0.03 tolerance, vs. fixed-threshold/index-based/frozen-RL baselines failing in 3-4 of 5 regimes; value cost at matched safety statistically indistinguishable from baselines; value-aware layer +2.58% value with unchanged safety) were produced by eval.py's SELF-GENERATED multi-regime traffic simulator and SELF-REIMPLEMENTED policies, NOT against the real Azure-trace-derived 210,000-request dataset (art_fAlkDy9YEd-N) that was separately, successfully constructed but sat unconsumed because gen_art_experiment_1 never ran. This is a genuine gap, not a cosmetic one: the same script both generates ground truth and implements the policy under test, which is a structural risk of self-referential inflation the next iteration must close by (a) running an independently-authored experiment script against the frozen, already-built trace-derived dataset (art_fAlkDy9YEd-N) as the PRIMARY evaluation, with the self-generated simulator numbers demoted to a robustness-check appendix, and (b) increasing seed count to >=5 per (policy, regime) cell to use the over-seed bootstrap the plan originally specified, tightening the two currently non-significant stationary-regime comparisons (conformal vs. fixed-threshold p_holm=0.098; vs. frozen-RL p_holm=0.098).\",", "   \"relation_type\": \"evolution\",", "-  \"relation_rationale\": \"Same conceptual frame (ACI-based admission control); narrowed to single-threshold scope, added formal theorem + eta/score specificity per reviewer.\",", "+  \"relation_rationale\": \"Same ACI frame; narrowed to single threshold, added theorem + eta/score specificity per reviewer.\",", "   \"confidence_delta\": \"unchanged\",", "   \"key_changes\": [", "     \"Flagged as unresolved: the reported Table 1 results are from a self-generated simulator/self-reimplemented policies inside eval.py, not from the already-built real Azure-trace dataset (art_fAlkDy9YEd-N), which sat unused because the experiment artifact never ran -- next iteration must run an independent experiment against that frozen dataset as the primary result.\","]}], "userModified": false, "replaceAll": false}
```

### [10] ASSISTANT · 2026-08-25 18:38:56 UTC

```
Fixed — the rationale is now under 120 characters.
```
