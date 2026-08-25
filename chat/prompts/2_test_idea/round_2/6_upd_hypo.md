# upd_hypo — test_idea

> Phase: `invention_loop` · round 2 · `upd_hypo`
> Run: `iter1_88afd6206a08` — Conformal Admission Control for Overloaded Request Queues
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-25 19:23:37 UTC

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
title: Conformal Admission Control for Overloaded Queues
hypothesis: |-
  An admission control policy built on ONLINE CONFORMAL RISK CONTROL -- not queueing theory, not reinforcement learning -- can hold a hard, distribution-free, finite-sample guarantee on the long-run rate of SLO violations (e.g., 'no more than alpha fraction of admitted requests exceed their P99 latency target') while maximizing throughput/value, under traffic and service-time distributions that are unknown, non-stationary, and possibly adversarial -- with NO assumption of exchangeability, no fitted queueing model, and no trained neural policy.

  Concretely: at admission time, a cheap, possibly miscalibrated risk score s(x) is computed by an explicit, documented, closed-form heuristic (queue depth + coarse per-endpoint service-time estimate; exact formula and O(1) per-request cost fixed in advance and reported, not just described qualitatively). The system does NOT trust s(x)'s calibration. It maintains a single scalar threshold lambda_t, updated after every observed outcome via the Adaptive Conformal Inference (ACI) gradient step lambda_{t+1} = lambda_t + eta * (alpha - y_t), with a FIXED, reported numeric eta (and a small pre-registered sensitivity sweep over eta, e.g. 3-5 values) rather than an unstated constant; admit iff s(x) <= lambda_t. Because this is a feedback-controlled quantile-tracking rule, it inherits the Gibbs & Candes (2021) finite-sample guarantee -- STATED IN THIS PAPER AS AN EXPLICIT THEOREM, in the paper's own notation (lambda_t, y_t in {0,1}, alpha, eta, window length T), including the non-asymptotic bound on |mean(y_t) - alpha| as a function of eta and the [0,1] loss range, with an explicit check that the admission-control setting's bounded-delay binary SLO-violation indicator satisfies the theorem's preconditions -- that the empirical SLO-violation rate over any long window converges to alpha REGARDLESS of the true, unknown, non-stationary process, a guarantee no queueing-theoretic or RL policy can offer. Request VALUE heterogeneity enters only as a tie-break/knapsack layer within the conformal-eligible set each control interval, never relaxing the safety rule.

  SCOPE, narrowed by iteration-1 evidence: the evaluated and claimed guarantee is for a SINGLE shared scalar threshold over one queue/endpoint class, not a per-function or per-tenant guarantee at the fleet scale the motivation invokes; multi-threshold extension under a joint budget remains future work and must be stated as such in the Introduction, not only at the end of the paper.

  EVIDENTIARY STATUS after iteration 1: the headline numbers (Table 1: conformal MAD 0.014-0.019 across 5 regimes, within the pre-registered 0.03 tolerance, vs. fixed-threshold/index-based/frozen-RL baselines failing in 3-4 of 5 regimes; value cost at matched safety statistically indistinguishable from baselines; value-aware layer +2.58% value with unchanged safety) were produced by eval.py's SELF-GENERATED multi-regime traffic simulator and SELF-REIMPLEMENTED policies, NOT against the real Azure-trace-derived 210,000-request dataset (art_fAlkDy9YEd-N) that was separately, successfully constructed but sat unconsumed because gen_art_experiment_1 never ran. This is a genuine gap, not a cosmetic one: the same script both generates ground truth and implements the policy under test, which is a structural risk of self-referential inflation the next iteration must close by (a) running an independently-authored experiment script against the frozen, already-built trace-derived dataset (art_fAlkDy9YEd-N) as the PRIMARY evaluation, with the self-generated simulator numbers demoted to a robustness-check appendix, and (b) increasing seed count to >=5 per (policy, regime) cell to use the over-seed bootstrap the plan originally specified, tightening the two currently non-significant stationary-regime comparisons (conformal vs. fixed-threshold p_holm=0.098; vs. frozen-RL p_holm=0.098).
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
_relation_rationale: >-
  Same ACI frame; narrowed to single threshold, added theorem + eta/score specificity per reviewer.
_confidence_delta: unchanged
_key_changes:
- >-
  Flagged as unresolved: the reported Table 1 results are from a self-generated simulator/self-reimplemented policies inside
  eval.py, not from the already-built real Azure-trace dataset (art_fAlkDy9YEd-N), which sat unused because the experiment
  artifact never ran -- next iteration must run an independent experiment against that frozen dataset as the primary result.
- >-
  Named the structural self-referential risk (same script generates data and implements the tested policy) and required an
  independently-authored data/label generator going forward.
- >-
  Required the ACI convergence claim be stated as an explicit theorem with notation and a non-asymptotic bound, not just paraphrase-and-cite,
  with preconditions explicitly checked against the bounded-delay binary-outcome setting.
- >-
  Required s(x) to be given as an explicit closed-form/pseudocode with per-request cost, and eta to be reported as a concrete
  numeric value with a small sensitivity sweep, rather than described only qualitatively.
- >-
  Narrowed scope: the guarantee as evaluated is for a single shared scalar threshold on one queue, and the Introduction must
  state this scope up front rather than motivating at fleet/multi-tenant scale and deferring the gap to the end.
- >-
  Required increasing seeds to >=5 per (policy, regime) cell to use the originally-planned over-seed bootstrap and tighten
  the two currently non-significant stationary-regime comparisons.
- >-
  Retained the core mechanism and headline claim unchanged, since the underlying result (where it was actually tested) held:
  conformal control was the only non-oracle policy within tolerance across all five regimes.
relation_type: evolution
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

--- Item 3 ---
id: art_bHFxugXcpJMg
type: experiment
in_dependencies:
- id: art_fAlkDy9YEd-N
  label: dataset
title: Conformal Admission Control on Real Azure Traces
summary: >-
  Implements and runs the ACI (adaptive conformal inference) admission controller alongside four baselines -- a fixed threshold,
  a deliberately misspecified M/M/1-style queueing index policy, a frozen logistic-regression contextual-bandit-style RL substitute,
  and a hindsight-optimal oracle knapsack -- directly against the frozen, real Azure-Functions-2019-derived dataset (art_fAlkDy9YEd-N,
  210,000 request-level rows spanning 5 traffic regimes: stationary, burst, drift, regime_switch, adversarial). Data-loading
  code (data_loader-style functions: load_dataset, group_by_regime_sorted, validate_dataset) is kept strictly separate from
  policy code (ConformalPolicy, FixedThresholdPolicy, MisspecifiedIndexPolicy, FrozenRLPolicy, OracleHindsightPolicy), with
  policies touching ground-truth outcome labels only through an explicit update() feedback call inside the replay loop, closing
  the self-referential-evaluation gap flagged in the prior iteration. On load, per-regime violation rates are hard-validated
  against the documented figures (stationary 3.95%, burst 0.24%, drift 15.53%, regime_switch 3.09%, adversarial 38.25%) and
  matched to within 0.005 percentage points before any policy code runs. The conformal policy's step size eta is swept over
  5 pre-registered values (0.01, 0.02, 0.05, 0.10, 0.20), and every (policy, regime, eta) cell is replayed with 5 independent
  seeds (225 total replay cells), using the first 200 rows of each regime as an excluded warm-up prefix for threshold initialization
  / baseline fitting only. Metrics reported per cell: mean absolute deviation of the rolling admitted-request violation rate
  from the target alpha=0.10 (the headline safety-control statistic), overall violation rate, total value admitted (uniform
  value=1.0 fallback, since the dataset carries no explicit per-row value field -- documented explicitly as a known limitation
  rather than silently invented), and admission rate. A percentile-bootstrap layer (10,000 resamples) gives seed-level confidence
  intervals per cell, and a permutation-test-based Holm-corrected pairwise comparison (conformal at its best eta vs. each
  baseline, per regime) re-tests the near-significant stationary-regime comparisons flagged in the prior iteration now against
  the real trace with >=5 seeds. A third phase compares a value-aware knapsack admission layer against plain first-come-first-served
  admission within the same conformal eligibility set; because of the uniform value=1.0 fallback this comparison legitimately
  reduces to a tie (mathematically expected, and reported as such rather than hidden). All numbers -- including the eta-sensitivity
  plateaus that arise from risk_score values clustering by function_id in the underlying trace, and the pairwise significance
  verdicts, whichever way they land -- are reported exactly as computed, with no post-hoc filtering toward a more flattering
  result. Runs in ~35 seconds end-to-end on 4 CPUs (well inside budget), and the full 210,000-row grid, 225-cell replay results
  (plus 25 knapsack-vs-FCFS cells), Holm-corrected significance tests, eta sensitivity sweep, and dataset validation report
  are all written to full_method_out.json in the exp_gen_sol_out schema (datasets/examples with input/output/metadata_*/predict_*
  fields), which validates with zero schema errors, alongside mini and preview truncated variants for quick inspection.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 4 ---
id: art_k4NZEyG_q_yz
type: evaluation
in_dependencies:
- id: art_fAlkDy9YEd-N
  label: dataset
title: Real-Trace Verdict for Admission Control
summary: >-
  Computes the pre-registered statistical verdict for conformal admission control on REAL Azure Functions trace data (art_fAlkDy9YEd-N,
  210,000 rows, 5 regimes: stationary/burst/drift/regime_switch/adversarial), promoted as the primary headline result for
  this iteration. gen_art_experiment_1 was EMPTY at execution time (no method_out.json), so per the plan's own validity check
  this technically triggers a HALT; the resolution taken (documented in eval.py's docstring and metadata.dependency_status)
  is to implement the 5 admission policies (conformal_aci, fixed_threshold, index_based, rl_frozen, oracle_hindsight) directly
  in eval.py and run them against the real, independently-produced trace data rather than a self-generated simulator -- strictly
  closer to the plan's intent than iteration 1, which had to self-generate both the dataset and the policy logs. Pre-registered
  validity checks (row count = 210,000, per-regime base violation rates cross-checked against the dataset's own documented
  figures) all PASS. For each (policy, regime) cell, computes admitted-request rolling-window violation rate (W=500), post-burn-in
  MAD from alpha=0.10 with the 3pp tolerance PASS/FAIL flag, and max transient spike. Because the real trace has no native
  seed/replicate dimension, 5 seeds are constructed as i.i.d. bootstrap resamples of each regime's rows (documented substitute
  for genuine replicates), enabling a genuine over-seed bootstrap (B=10,000, whole-seed resampling) for 95% CIs and Holm-Bonferroni-corrected
  paired significance tests (conformal vs each baseline, 15 regime x baseline pairs). The two previously-tied stationary-regime
  comparisons from iteration 1 (conformal vs fixed_threshold, conformal vs frozen-RL, both p_holm=0.098) are explicitly re-tested;
  neither resolves to significant at alpha=0.05 with the real trace (p_holm=1.0 both), which is itself informative -- documented
  as such rather than obscured. Matched-violation-rate value comparison and value-aware-knapsack-vs-FCFS checks are reproduced
  using a documented deterministic value proxy (dataset has no native value field: value = (1/slo_target) * (0.25 + 0.75*risk_score),
  blending per-function SLO tightness with per-request risk_score for genuine request-level variation) and a load proxy (inverse
  trailing-50-request mean inter-arrival time) for load-driven baselines; the knapsack check runs on regime_switch rather
  than stationary because stationary is dominated by a single function_id (constant slo_target) which makes the value proxy
  degenerate there. A new eta-sensitivity table/plot (MAD and max-spike vs eta over grid [0.01,0.02,0.05,0.10,0.20]) is computed
  for stationary, regime_switch, and adversarial. Iteration 1's self-generated eval_out.json (art_oRyejQXIp14c) is loaded
  purely as a labeled secondary comparison tagged self_generated_robustness_check (60% cell-level tolerance-verdict agreement
  with the new primary numbers), never blended into primary metrics. Overall verdict: PARTIALLY_CONFIRMED -- an important
  real-data finding documented in validity_notes is that per-regime base violation rates vary hugely (0.24% to 38.25%) around
  the single global alpha=0.10 target, so even the non-causal hindsight oracle fails the 3pp tolerance test in low-base-rate
  regimes (stationary/burst/regime_switch) by mathematical construction, not policy failure; conformal_aci still passes tolerance
  in drift and is materially closer to alpha than all frozen baselines in adversarial. Outputs: eval.py (fully self-contained,
  real-data-driven), eval_out.json (schema-validated against exp_eval_sol_out, includes per-policy-regime deviation stats,
  paired significance tests, matched-value and knapsack checks, eta sensitivity, and the secondary comparison), full/mini/preview
  variants, and 6 figure pairs (PNG+PDF) under figures/ showing rolling violation-rate trajectories per regime plus eta sensitivity.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 2 artifacts were created THIS iteration.

id: art_bHFxugXcpJMg
type: experiment
in_dependencies:
- id: art_fAlkDy9YEd-N
  label: dataset
title: Conformal Admission Control on Real Azure Traces
summary: >-
  Implements and runs the ACI (adaptive conformal inference) admission controller alongside four baselines -- a fixed threshold,
  a deliberately misspecified M/M/1-style queueing index policy, a frozen logistic-regression contextual-bandit-style RL substitute,
  and a hindsight-optimal oracle knapsack -- directly against the frozen, real Azure-Functions-2019-derived dataset (art_fAlkDy9YEd-N,
  210,000 request-level rows spanning 5 traffic regimes: stationary, burst, drift, regime_switch, adversarial). Data-loading
  code (data_loader-style functions: load_dataset, group_by_regime_sorted, validate_dataset) is kept strictly separate from
  policy code (ConformalPolicy, FixedThresholdPolicy, MisspecifiedIndexPolicy, FrozenRLPolicy, OracleHindsightPolicy), with
  policies touching ground-truth outcome labels only through an explicit update() feedback call inside the replay loop, closing
  the self-referential-evaluation gap flagged in the prior iteration. On load, per-regime violation rates are hard-validated
  against the documented figures (stationary 3.95%, burst 0.24%, drift 15.53%, regime_switch 3.09%, adversarial 38.25%) and
  matched to within 0.005 percentage points before any policy code runs. The conformal policy's step size eta is swept over
  5 pre-registered values (0.01, 0.02, 0.05, 0.10, 0.20), and every (policy, regime, eta) cell is replayed with 5 independent
  seeds (225 total replay cells), using the first 200 rows of each regime as an excluded warm-up prefix for threshold initialization
  / baseline fitting only. Metrics reported per cell: mean absolute deviation of the rolling admitted-request violation rate
  from the target alpha=0.10 (the headline safety-control statistic), overall violation rate, total value admitted (uniform
  value=1.0 fallback, since the dataset carries no explicit per-row value field -- documented explicitly as a known limitation
  rather than silently invented), and admission rate. A percentile-bootstrap layer (10,000 resamples) gives seed-level confidence
  intervals per cell, and a permutation-test-based Holm-corrected pairwise comparison (conformal at its best eta vs. each
  baseline, per regime) re-tests the near-significant stationary-regime comparisons flagged in the prior iteration now against
  the real trace with >=5 seeds. A third phase compares a value-aware knapsack admission layer against plain first-come-first-served
  admission within the same conformal eligibility set; because of the uniform value=1.0 fallback this comparison legitimately
  reduces to a tie (mathematically expected, and reported as such rather than hidden). All numbers -- including the eta-sensitivity
  plateaus that arise from risk_score values clustering by function_id in the underlying trace, and the pairwise significance
  verdicts, whichever way they land -- are reported exactly as computed, with no post-hoc filtering toward a more flattering
  result. Runs in ~35 seconds end-to-end on 4 CPUs (well inside budget), and the full 210,000-row grid, 225-cell replay results
  (plus 25 knapsack-vs-FCFS cells), Holm-corrected significance tests, eta sensitivity sweep, and dataset validation report
  are all written to full_method_out.json in the exp_gen_sol_out schema (datasets/examples with input/output/metadata_*/predict_*
  fields), which validates with zero schema errors, alongside mini and preview truncated variants for quick inspection.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_k4NZEyG_q_yz
type: evaluation
in_dependencies:
- id: art_fAlkDy9YEd-N
  label: dataset
title: Real-Trace Verdict for Admission Control
summary: >-
  Computes the pre-registered statistical verdict for conformal admission control on REAL Azure Functions trace data (art_fAlkDy9YEd-N,
  210,000 rows, 5 regimes: stationary/burst/drift/regime_switch/adversarial), promoted as the primary headline result for
  this iteration. gen_art_experiment_1 was EMPTY at execution time (no method_out.json), so per the plan's own validity check
  this technically triggers a HALT; the resolution taken (documented in eval.py's docstring and metadata.dependency_status)
  is to implement the 5 admission policies (conformal_aci, fixed_threshold, index_based, rl_frozen, oracle_hindsight) directly
  in eval.py and run them against the real, independently-produced trace data rather than a self-generated simulator -- strictly
  closer to the plan's intent than iteration 1, which had to self-generate both the dataset and the policy logs. Pre-registered
  validity checks (row count = 210,000, per-regime base violation rates cross-checked against the dataset's own documented
  figures) all PASS. For each (policy, regime) cell, computes admitted-request rolling-window violation rate (W=500), post-burn-in
  MAD from alpha=0.10 with the 3pp tolerance PASS/FAIL flag, and max transient spike. Because the real trace has no native
  seed/replicate dimension, 5 seeds are constructed as i.i.d. bootstrap resamples of each regime's rows (documented substitute
  for genuine replicates), enabling a genuine over-seed bootstrap (B=10,000, whole-seed resampling) for 95% CIs and Holm-Bonferroni-corrected
  paired significance tests (conformal vs each baseline, 15 regime x baseline pairs). The two previously-tied stationary-regime
  comparisons from iteration 1 (conformal vs fixed_threshold, conformal vs frozen-RL, both p_holm=0.098) are explicitly re-tested;
  neither resolves to significant at alpha=0.05 with the real trace (p_holm=1.0 both), which is itself informative -- documented
  as such rather than obscured. Matched-violation-rate value comparison and value-aware-knapsack-vs-FCFS checks are reproduced
  using a documented deterministic value proxy (dataset has no native value field: value = (1/slo_target) * (0.25 + 0.75*risk_score),
  blending per-function SLO tightness with per-request risk_score for genuine request-level variation) and a load proxy (inverse
  trailing-50-request mean inter-arrival time) for load-driven baselines; the knapsack check runs on regime_switch rather
  than stationary because stationary is dominated by a single function_id (constant slo_target) which makes the value proxy
  degenerate there. A new eta-sensitivity table/plot (MAD and max-spike vs eta over grid [0.01,0.02,0.05,0.10,0.20]) is computed
  for stationary, regime_switch, and adversarial. Iteration 1's self-generated eval_out.json (art_oRyejQXIp14c) is loaded
  purely as a labeled secondary comparison tagged self_generated_robustness_check (60% cell-level tolerance-verdict agreement
  with the new primary numbers), never blended into primary metrics. Overall verdict: PARTIALLY_CONFIRMED -- an important
  real-data finding documented in validity_notes is that per-regime base violation rates vary hugely (0.24% to 38.25%) around
  the single global alpha=0.10 target, so even the non-causal hindsight oracle fails the 3pp tolerance test in low-base-rate
  regimes (stationary/burst/regime_switch) by mathematical construction, not policy failure; conformal_aci still passes tolerance
  in drift and is materially closer to alpha than all frozen baselines in adversarial. Outputs: eval.py (fully self-contained,
  real-data-driven), eval_out.json (schema-validated against exp_eval_sol_out, includes per-policy-regime deviation stats,
  paired significance tests, matched-value and knapsack checks, eta sensitivity, and the secondary comparison), full/mini/preview
  variants, and 6 figure pairs (PNG+PDF) under figures/ showing rolling violation-rate trajectories per regime plus eta sensitivity.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

Overloaded request-serving systems -- a serverless function platform, a database connection pool, an API gateway in front of a microservice fleet -- must decide, for every incoming request, whether to admit it now or reject it before it consumes resources it cannot repay. This decision is an admission-control problem: choose a subset of arriving requests to serve so that the fraction of admitted requests that miss a latency service-level objective (SLO), such as a P99 response-time target, stays at or below an operator-chosen rate alpha, while admitting as much useful work as possible.

Getting this right matters wherever load is unpredictable and the cost of guessing wrong is real. A function-as-a-service platform processes invocations with wildly different, non-stationary demand across its functions; a single deployment, a viral event, or a shift in a co-located tenant's workload can change the traffic an admission controller sees within minutes. An operator with no bound on the SLO-violation rate either over-provisions to survive worst-case bursts, wasting capacity most of the time, or under-provisions and risks a violation cascade that a single bad five minutes of traffic can trigger. The evaluation in this paper targets that narrower, concrete setting -- a single shared queue or endpoint class governed by one admission threshold -- rather than a claim about coordinated guarantees across a whole multi-tenant fleet; extending the mechanism to per-function or per-tenant thresholds under a joint budget is future work, discussed at the end of this paper.

The problem is hard because the traffic and service-time processes that determine whether a given admission decision will violate an SLO are not known in advance, are rarely stationary, and can change abruptly. Any policy whose safety argument rests on a fitted model of that process is only as safe as the model's fit to the traffic that actually arrives, and the traffic that breaks the fit is exactly the traffic an operator most needs protection from.

The two paradigms in use today accept this fragility as the price of a formal argument, or drop the formal argument entirely. Queueing-theoretic and index-based controllers, including the classical Whittle-index construction for restless-bandit admission control [9] and its birth-death-model extension to queueing admission [3], derive elegant near-optimal policies -- but their optimality guarantee is a statement about expected long-run reward under an assumed distributional model of the arrival and service process, not a finite-sample bound on the violation rate actually realized when that model is wrong. Learned controllers such as TopFull [4], a reinforcement-learning admission and rate controller for SLO-oriented microservices reported to beat DAGOR- and Breakwater-style overload control on P99 latency, adapt empirically to whatever traffic a training run exposes them to -- but carry no finite-sample safety guarantee at all, so a distribution shift the policy did not see during training is a real, unbounded deployment risk rather than a bounded, quantified one.

This paper tests a third paradigm, adapted from a distinct branch of statistics not previously applied, to our knowledge, to admission control: online conformal risk control. Conformal Risk Control [1] and its online, non-exchangeable extension, Adaptive Conformal Inference (ACI) [2], choose a decision threshold by a feedback rule -- raise it when a monitored loss has recently run above target, lower it when it has run below -- that provably tracks a target loss rate over any long window, for any underlying data-generating process, with no distributional assumption. We repoint this rule at the admission decision itself: a single scalar threshold, updated after every observed outcome, decides whether to admit a request whose cheap, possibly poorly calibrated risk score falls below it. Request value is used only to rank requests already judged eligible by this threshold, so the resulting policy pursues throughput without weakening the guarantee it is built on.

[FIGURE:fig1]

We test this policy against four baselines -- a frozen fixed-score threshold, a misspecified queueing-index policy, a reinforcement-learning controller frozen after training on stationary traffic only, and a hindsight-optimal oracle -- on a 210,000-request dataset built from real Azure Functions invocation and duration traces, spanning five traffic regimes (stationary, burst, drift, an unannounced regime switch, and a synthetically constructed adversarial sequence). The central, and partly unexpected, empirical finding is that a fixed +/-3-percentage-point tolerance around the target rate is not a fair pass/fail line for any admission policy, including a hindsight-optimal oracle, in a regime whose natural violation rate already sits far below the target: when almost nothing needs to be rejected to hit the target, no policy can push the realized rate up to meet it, and every policy we test -- oracle included -- fails the tolerance in exactly those regimes. Where the target is instead a genuine constraint -- in the drift regime, where the natural violation rate (15.5%) exceeds the target, and in the adversarial regime, constructed to defeat a fixed rule -- the conformal controller is the only non-oracle policy that stays statistically indistinguishable from the oracle-quality tracking behavior, significantly outperforming all three non-oracle baselines in drift (Holm-corrected p < 0.001 in each case) and the frozen reinforcement-learning baseline in the adversarial regime. A value-aware admission layer built on top of the conformal eligibility set is statistically indistinguishable from first-come-first-served admission on this real trace, a result we report as a negative finding rather than smoothing it into a positive one.

## Summary of Contributions

- We introduce conformal admission control, an admission policy that repoints the Adaptive Conformal Inference threshold-tracking update onto the admit/reject decision for an SLO-violation loss, and state its finite-sample guarantee as an explicit theorem in the admission-control setting's own notation, including the precondition that the bound is over the number of *admitted* requests rather than raw arrivals (Section 3).
- We evaluate the policy on a 210,000-request dataset built from real Azure Functions traces across five traffic regimes, using an independently authored, frozen dataset that the policy code never touches except through its own explicit feedback signal (Section 4).
- We show that a single global tolerance line is not a fair test of any admission policy across regimes with very different natural violation rates: even a hindsight-optimal oracle fails a fixed +/-3-percentage-point criterion in regimes whose natural rate sits far from the target, which reframes what "distribution-free control" can and cannot mean in practice (Section 5.1).
- We show that where the target rate is a genuine constraint -- the drift and adversarial regimes -- the conformal controller significantly outperforms the frozen model-based and learned baselines, while in regimes it cannot be tested fairly it is statistically indistinguishable from them (Section 5.2).
- We report, rather than mask, that a value-aware admission layer shows no statistically significant value gain over first-come-first-served admission on the real trace, in contrast to a synthetic-simulator finding from an earlier iteration of this study, and discuss why (Section 5.4, Section 6).

# Related Work

**Conformal risk control and adaptive conformal inference.** Conformal prediction methods construct set-valued or thresholded predictions with a finite-sample, distribution-free coverage guarantee under the sole assumption that calibration and test data are exchangeable [6]. Conformal Risk Control [1] generalizes this to control the expected value of any bounded, monotone loss -- not only miscoverage -- at a target level, via a threshold chosen by inverting the empirical loss curve, and gives an online variant for sequential, non-exchangeable data. Distribution-Free, Risk-Controlling Prediction Sets [7] independently develops a closely related threshold-selection framework with the same finite-sample guarantee for monotone losses, applied to prediction-set-valued outputs such as image segmentation and classification-with-rejection. Adaptive Conformal Inference (ACI) [2] removes the exchangeability assumption entirely: a single online gradient step on the threshold, using only the realized indicator of the current loss, provably drives the long-run average loss to the target rate irrespective of the true, possibly adversarial, data-generating process. Achieving Risk Control in Online Learning Settings [8] extends this line further with alternative online update rules for the threshold-tracking problem. More recent work has strengthened the online-tracking guarantee itself: Improved Online Conformal Prediction via Strongly Adaptive Online Learning [10] replaces a single running threshold with a bank of experts, each active over its own window, to give simultaneous coverage guarantees over *every* recent interval length rather than only the long-run average the plain ACI update controls, and Parameter-Free and Group Conditional Online Conformal Prediction [11] removes the need to hand-tune a step size such as our eta and extends the guarantee to hold conditionally within declared subgroups of the stream. Neither of these more recent variants has been applied to a systems admission-control setting; we adopt the plain, single-parameter ACI update in this paper because its guarantee is the simplest to state and verify precisely in the notation an admission-control reader needs (Section 3), and because a strongly-adaptive multi-window threshold or a group-conditional threshold defined per endpoint is a direct, motivated extension of the single-threshold policy evaluated here, discussed further at the end of this paper. None of the five papers in this paragraph addresses systems admission control, queueing, or latency SLOs, and a targeted search of the conformal prediction literature crossed with admission-control and queueing terms surfaced no prior application of this machinery to request admission.

**Queueing-theoretic and index-based admission control.** The classical treatment of admission control as an optimal-stopping or restless-bandit problem dates to Whittle's index policy for restless bandits [9], later specialized to queueing admission control via a polyhedral, marginal-productivity index construction [3] that gives near-optimal expected long-run reward under an assumed birth-death arrival and service model. This family of results is a genuine engineering advance where the assumed model is a good fit, but its guarantee is conditional on that fit: it says nothing, finite-sample, about the realized violation rate when the true process departs from the assumed one, which is precisely the setting non-stationary production traffic creates.

**Learned and heuristic overload control.** Deep-reinforcement-learning and empirically tuned overload controllers, exemplified by TopFull [4] -- a per-API rate controller reported to outperform threshold-based systems such as DAGOR and Breakwater on SLO compliance and tail latency -- adapt their admission policy from observed system state without assuming a queueing model. Their safety is empirical: nothing in the training or deployment procedure bounds the violation rate a distribution-shifted test regime will realize, which is the property this paper's frozen reinforcement-learning baseline is designed to probe directly.

**Real traffic traces.** The dataset evaluated in this paper is built from the Azure Functions 2019 invocation and execution-duration trace [5], a widely used public characterization of a production serverless workload's non-stationary, bursty invocation pattern and per-function duration distribution.

# Preliminaries: Conformal Risk Control and Adaptive Conformal Inference

Conformal Risk Control [1] addresses the following problem: given a bounded, monotone loss function of a decision threshold, choose the threshold so that the expected loss is at most a target level alpha, with a finite-sample guarantee that holds regardless of the underlying data distribution, provided calibration and test examples are exchangeable. Adaptive Conformal Inference [2] removes the exchangeability requirement by replacing the batch threshold choice with an online update: after observing the loss incurred by the current threshold's decision, the threshold moves by a step proportional to the gap between the realized loss and the target rate alpha, in the direction that pushes the running average loss back toward alpha. This single-parameter update achieves the target long-run average loss rate over any window, for any sequence of losses -- including one generated adversarially -- because it is a bounded, self-correcting feedback rule rather than an estimate of a fixed underlying distribution.

## A Formal Statement for the Admission-Control Setting

We state the guarantee explicitly in the admission-control setting's own notation, because the loss it controls here -- a delayed, admission-conditional binary SLO-violation indicator -- differs in one respect from the sequential-forecasting loss the original result was stated for, and that difference changes what the bound says.

Let requests arrive at times $t = 1, 2, \dots, T$, each carrying a risk score $s(x_t) \in [0, 1]$. The controller maintains a threshold $\lambda_t$ and admits request $t$ iff $s(x_t) \le \lambda_t$. For an admitted request, the SLO-violation outcome $y_t \in \{0, 1\}$ becomes observable within a bounded delay, and the threshold updates as

$$\lambda_{t+1} = \lambda_t + \eta \, (\alpha - y_t) \quad \text{if request } t \text{ is admitted}, \qquad \lambda_{t+1} = \lambda_t \quad \text{otherwise},$$

with a fixed step size $\eta > 0$ and target rate $\alpha \in (0, 1)$. This admission-conditional update is a deliberate departure from the original ACI setting [2], which always observes an outcome at every step; here a rejected request contributes no signal, so the threshold is carried forward unchanged for it [ARTIFACT:art_bHFxugXcpJMg].

**Theorem (finite-sample tracking bound, adapted from Gibbs & Candès [2]).** Let $t_1 < t_2 < \dots < t_{N_T}$ index the requests admitted up to time $T$, and suppose $\lambda_t$ is restricted to a bounded range of width $B = \lambda_{\max} - \lambda_{\min}$ (which holds automatically once $s(x)$ and hence $\lambda_t$ are bounded, e.g. $B \le 1$ for a score normalized to $[0,1]$). Then, for *any* sequence of scores and outcomes -- stationary, drifting, switching, or adversarially constructed -- the update above satisfies

$$\left| \frac{1}{N_T} \sum_{i=1}^{N_T} y_{t_i} \;-\; \alpha \right| \;\le\; \frac{B}{\eta \, N_T}.$$

*Proof sketch.* Summing the update rule over admitted indices telescopes: $\lambda_{t_{N_T}+1} - \lambda_{t_1} = \eta \sum_{i=1}^{N_T} (\alpha - y_{t_i})$. Since $\lambda_t \in [\lambda_{\min}, \lambda_{\max}]$ for all $t$, the left side is bounded in absolute value by $B$, so $\left| \sum_i (\alpha - y_{t_i}) \right| \le B / \eta$; dividing by $N_T$ gives the stated bound. No assumption on how $y_{t_i}$ or $s(x_{t_i})$ were generated is used anywhere in this argument, which is exactly the property that makes the bound distribution-free. $\square$

Two things about this bound matter directly for the results in Section 5, and reviewing them here is the promised precondition check. First, the guarantee is over $N_T$, the number of *admitted* requests, not the number of arrivals $T$ -- a rarely-admitting regime (as the adversarial regime turns out to be, Section 5.2) weakens the bound in direct proportion to how few requests survive to be measured, and at $N_T$ small enough that $B/(\eta N_T) > 1$ the bound is vacuous rather than false. Second, the bound assumes the admission-conditional outcome $y_{t_i}$ is observed with a delay short relative to how fast $\lambda_t$ moves; our dataset's outcomes are computed from realized service time and are available effectively instantaneously, satisfying this precondition by construction, but a production deployment where SLO confirmation lags admission by minutes would need $\eta$ re-tuned against that delay, widening the effective window the bound applies to, exactly as flagged in the Discussion.

# Method: Conformal Admission Control

## Risk Score and Threshold-Tracking Admission Rule

Each arriving request $x_t$ carries a risk score $s(x_t) \in [0,1]$, computed at admission time only from three ingredients available before the request is served: the target function's coarse day-ahead median service time relative to its own SLO target, a local arrival-rate proxy (a trailing 30-minute mean arrival rate relative to a longer-run baseline rate), and a queue-depth proxy derived from the current minute's admitted-request count. Concretely, writing $\sigma(\cdot)$ for the logistic sigmoid,

$$s(x_t) = 0.5 \, \sigma\!\left(\frac{m_f - \mathrm{SLO}_f}{\mathrm{SLO}_f}\right) + 0.3 \, \sigma\!\left(\frac{r_{\text{local}} - r_{\text{base}}}{r_{\text{base}} + \epsilon}\right) + 0.2 \, \sigma\!\left(\frac{q - 5}{5}\right),$$

where $m_f$ is function $f$'s prior-day median service time, $\mathrm{SLO}_f$ is its documented P99-derived target, $r_{\text{local}}$ and $r_{\text{base}}$ are the trailing-window and baseline arrival rates, and $q$ is the queue-depth proxy, capped at 50. Every term is computable in $O(1)$ time per request from state already maintained for routing (a per-function running median, a trailing arrival-rate counter, and the current minute's admitted count), so the score adds no asymptotic overhead to the admission path. In the adversarial regime, this formula is not used; scores are instead drawn from a bimodal distribution ($\mathrm{Uniform}(0, 0.15)$ for eventually-safe requests, $\mathrm{Uniform}(0.85, 1.0)$ for eventually-violating ones) specifically so that no threshold rule computed from a smoothly-varying model of risk can separate the two clusters by construction [ARTIFACT:art_fAlkDy9YEd-N]. The controller does not require $s(x_t)$ to be a calibrated probability -- Section 3's theorem holds regardless of the score's accuracy -- only that it is available before the admission decision is made.

The threshold-tracking rule is the update stated formally in Section 3: admit iff $s(x_t) \le \lambda_t$, and after each admitted request's outcome is observed, $\lambda_{t+1} = \lambda_t + \eta (\alpha - y_t)$. We report results at a primary step size of $\eta = 0.05$ and sweep $\eta \in \{0.01, 0.02, 0.05, 0.1, 0.2\}$ in Section 5.3, following the pre-registered grid.

## Value-Aware Admission Layer

Within a fixed control interval, the conformal rule defines an eligibility set: the requests with $s(x) \le \lambda_t$. When more requests are eligible than the system has capacity to serve, the safety guarantee in Section 3 is agnostic to which eligible requests are chosen -- it is a statement about the violation rate among whichever requests get admitted, not about which specific ones those are. We exploit this slack by ranking eligible requests within each interval by a request-level value signal and admitting the highest-value requests first, up to capacity, rather than admitting first-come-first-served (FCFS). This reduces to a bounded knapsack problem over the eligible set with capacity as the constraint; the eligibility set itself, and hence the violation-rate guarantee, is unchanged by which ranking is used inside it.

# Experimental Setup

## Real-Trace Dataset as the Primary Evaluation

**All results reported in Section 5 below are computed on the real, trace-derived dataset described in this subsection, not on any self-generated or synthetic simulator.** We flag this explicitly here, at the top of the setup, rather than deferring it to a limitations paragraph, because an earlier iteration of this study reported headline numbers from a self-generated simulator when its dataset dependency happened to be unavailable at evaluation time; that self-generated evaluation is retained only as a secondary robustness check in Section 5.5, clearly labeled, and never blended into the primary metrics reported below.

The dataset comprises 210,000 admission-time request records built from the Azure Functions 2019 invocation-per-minute and execution-duration-percentile trace [5], spanning five traffic regimes: a stationary baseline (50,000 rows, selected for low coefficient of variation), a sudden burst (40,000 rows, a spike ratio of at least 10x baseline), a slow monotonic drift (50,000 rows), an unannounced regime switch (50,000 rows, a hard concatenation of two structurally distinct real function windows with no warning signal), and a synthetically constructed adversarial sequence (20,000 rows, roughly 9.5% of the dataset, explicitly flagged as synthetic in its provenance metadata) [ARTIFACT:art_fAlkDy9YEd-N]. Each request's label is a post-hoc binary SLO-violation indicator computed from its realized service time relative to its function's documented P99-derived target, using information excluded from the admission-time input to avoid label leakage. The overall violation rate is 9.06%, but this masks a wide regime-dependent spread that turns out to be central to the results below: 3.95% in stationary, 0.24% in burst, 15.53% in drift, 3.09% in regime switch, and 38.25% in the synthetically constructed adversarial regime.

A separate policy-implementation artifact loads this frozen dataset through data-loading code kept structurally apart from the five policy implementations, so that policies touch ground-truth outcome labels only through an explicit, per-decision feedback call inside the replay loop -- closing the self-referential-evaluation risk a reviewer of an earlier draft identified, in which the same script both generated traffic and implemented the policy under test [ARTIFACT:art_bHFxugXcpJMg]. On load, every regime's violation rate is hard-validated against the figures above to within 0.005 percentage points before any policy code runs; all five regimes matched exactly.

## Baselines, Seeds, and Statistics

We compare the conformal controller against four baselines evaluated on the identical real-trace sequences: a fixed threshold calibrated once on the stationary regime and never updated; a misspecified M/M/1-style queueing index policy that admits below a fixed instantaneous-load threshold; a frozen logistic-regression contextual-bandit-style controller trained only on the stationary regime, standing in for a reinforcement-learning-style overload controller exposed to unseen distribution shift at test time; and a hindsight-optimal oracle that re-thresholds each window to hit the target rate exactly, representing an upper bound unavailable to any online policy. Because the real trace carries no native seed or replicate dimension, we construct five independent seeds per (policy, regime) cell as i.i.d. bootstrap resamples of that regime's rows -- a documented substitute for genuine replicates that lets us run the over-seed bootstrap the evaluation plan originally specified (10,000 resamples, whole-seed resampling), rather than the block-over-time fallback an earlier iteration used with only three seeds [ARTIFACT:art_k4NZEyG_q_yz]. For every (policy, regime) cell we report the rolling admitted-request violation rate over a 500-request window, its mean absolute deviation (MAD) from alpha = 0.10 post burn-in, and the maximum transient spike above alpha. We pre-registered a tolerance of 3 percentage points (0.03) on MAD as the pass/fail criterion, and used a paired, Holm-Bonferroni-corrected bootstrap significance test (conformal vs. each baseline, per regime) across all 15 (regime, baseline) comparisons. A deterministic value proxy, $\mathrm{value} = (1/\mathrm{SLO}_f) \cdot (0.25 + 0.75 \cdot s(x))$, blends per-function SLO tightness with per-request risk score for the matched-violation-rate value comparison and the knapsack layer, since the dataset carries no native value field.

# Results

## A Global Tolerance Is Not a Fair Test Across Regimes with Different Natural Violation Rates

[FIGURE:fig2]

Before comparing policies, it is necessary to establish what the 3-percentage-point tolerance around alpha = 0.10 is actually testing, because the answer turns out to depend heavily on the regime. Figure 2 plots each regime's natural violation rate -- the rate realized when every request is admitted -- against the target. Three regimes (stationary, 3.95%; burst, 0.24%; regime switch, 3.09%) have a natural rate well *below* the 10% target, meaning a policy has to actively push the violation rate *up* toward alpha to hit it, which is not something an admission policy -- a mechanism that can only reject requests, never manufacture violations -- can do once it is already admitting nearly everyone. Two regimes (drift, 15.53%; adversarial, 38.25%) have a natural rate *above* the target, the setting an admission-control policy is actually built for: reject enough of the riskiest requests to bring the realized rate down to alpha.

This asymmetry is not a hypothetical concern; it determines the tolerance-pass outcome directly. The hindsight-optimal oracle -- which by construction re-thresholds every window to target alpha exactly, and has no online-tracking error to speak of -- still *fails* the 3-percentage-point tolerance in stationary (MAD 0.0599), burst (MAD 0.0974), and regime switch (MAD 0.0688), because at those regimes' natural rates there is nothing for a threshold to correct: with almost every request admitted at the natural rate already below alpha, the *realized* rate simply sits below alpha, and the gap from alpha is the natural rate's own distance from the target, not a policy failure. The oracle passes cleanly only in drift (MAD 0.0117) and adversarial (MAD 0.0077), the two regimes where the target is a genuine constraint. We report this as a finding about the evaluation methodology itself, not only about the policies: a fixed global tolerance line, applied uniformly across regimes whose natural violation rates differ by two orders of magnitude, tests whether the natural rate happens to sit near the target far more than it tests whether a policy tracks well.

## Where the Target Is a Real Constraint, Conformal Admission Control Wins

[FIGURE:fig3]

Table 1 reports the post-burn-in MAD for every (policy, regime) cell against the real trace. In the two regimes where the oracle itself passes tolerance -- drift and adversarial -- the conformal controller is materially and, in drift, statistically significantly closer to the target than every non-oracle baseline. In drift, conformal's MAD (0.0280) is the only non-oracle result within the 3-percentage-point tolerance, against 0.0559 (fixed threshold), 0.0556 (index-based), and 0.0557 (frozen RL); a Holm-corrected paired bootstrap test finds conformal significantly closer to alpha than all three baselines (p < 0.001 in each case). In the adversarial regime, conformal's MAD (0.2418) is substantially below fixed threshold (0.2821), index-based (0.3014), and frozen RL (0.4253); the comparison against the frozen RL baseline is Holm-significant (p < 0.001), while the comparisons against the fixed threshold (p_holm = 0.278) and index-based policy (p_holm = 0.093) do not clear the corrected significance bar, reflecting the wide bootstrap interval that comes with the very small number of requests any policy admits under this deliberately adversarial score distribution (as few as 56-367 admissions across five seeds, out of 20,000 adversarial rows).

| Regime | Natural rate | Conformal | Fixed threshold | Index-based | RL (frozen) | Oracle |
|---|---|---|---|---|---|---|
| Stationary | 3.95% | 0.0600 (fail) | 0.0599 (fail) | 0.0605 (fail) | 0.0601 (fail) | 0.0599 (fail) |
| Burst | 0.24% | 0.0974 (fail) | 0.0974 (fail) | 0.0973 (fail) | 0.0972 (fail) | 0.0974 (fail) |
| Drift | 15.53% | **0.0280 (pass)** | 0.0559 (fail) | 0.0556 (fail) | 0.0557 (fail) | 0.0117 (pass) |
| Regime switch | 3.09% | 0.0688 (fail) | 0.0688 (fail) | 0.0718 (fail) | 0.0710 (fail) | 0.0688 (fail) |
| Adversarial | 38.25% | 0.2418 (fail) | 0.2821 (fail) | 0.3014 (fail) | 0.4253 (fail) | 0.0077 (pass) |

*Table 1: Post-burn-in mean absolute deviation (MAD) from the target alpha = 0.10, per policy and regime, on the real Azure-trace dataset. n = 5 bootstrap seeds x full regime row count per cell. Bold marks the only non-oracle pass.*

In the three regimes where even the oracle cannot pass the tolerance for the structural reason established in Section 5.1, the picture is mixed rather than uniformly negative for conformal control. In regime switch, conformal is Holm-significantly closer to alpha than the index-based policy (p < 0.001) and the frozen RL controller (p < 0.001), but not significantly different from the fixed threshold (p_holm = 0.139) -- all four non-oracle policies converge to nearly the same MAD (0.0688-0.0718) because, as in stationary and burst, the natural rate sits so far below alpha that every policy ends up admitting almost everything and none has room to differentiate. In stationary and burst, none of the 6 pairwise comparisons (conformal vs. each of the 3 baselines, 2 regimes) reaches Holm significance; all five policies, oracle included, land within 0.001 of each other's MAD. Across all 15 (regime, baseline) comparisons, conformal is significantly closer to alpha than the baseline in 6 (40%), and every one of those 6 significant wins occurs in a regime where the natural rate is not already saturating the admission decision -- drift (3 of 3 baselines) and adversarial and regime-switch combined (3 of 6) [ARTIFACT:art_k4NZEyG_q_yz].

## The Safety Guarantee at Matched Violation Rate

We re-thresholded each baseline on the stationary regime to match the conformal controller's own realized violation rate, then compared total accepted value. Against the fixed threshold and the frozen RL controller, the conformal policy's accepted value differs by only 0.014% (375,373 vs. 375,426 request-value units), well within the bootstrap confidence interval's width and not distinguishable in practice. Against the misspecified index-based policy, conformal accepts roughly 13.0% more total value at the same matched violation rate (375,373 vs. 332,102), with a bootstrap 95% confidence interval on the gap ([-13.60%, -12.46%] in the baseline-relative direction) that excludes zero -- the index policy's fixed instantaneous-load threshold discards materially more admissible, safe work than a rule that reacts to the realized outcome it is trying to control. None of these three comparisons approaches the pre-registered disconfirming threshold of a 50% value loss.

## Eta Sensitivity

[FIGURE:fig4]

The step size eta trades off tracking speed against tracking noise, and its effect is regime-dependent in a way that is only visible once regimes with a genuine, sustained target-gap are examined. In the adversarial regime, where the natural violation rate (38.25%) sits far above alpha and stays there throughout, MAD falls monotonically as eta grows: 0.3916 at eta = 0.01, 0.3580 at 0.02, 0.2418 at 0.05 (the primary setting), 0.1443 at 0.10, and 0.0448 at 0.20 -- a larger step corrects a persistent, one-directional gap faster. In regime switch, the opposite pattern appears at the largest step size: MAD is flat across eta in {0.01, 0.02, 0.05} (0.0688 throughout) but rises to 0.0712 at eta = 0.10 and 0.0983 at eta = 0.20, because a threshold that reacts too aggressively overshoots around the switch point rather than settling. In stationary, MAD is essentially flat across the whole sweep (0.0599 to 0.0629), consistent with Section 5.1's finding that this regime's natural rate leaves the threshold with almost nothing to correct regardless of how fast it is allowed to move. We note, as a limitation rather than a settled conclusion, that a second, independently authored replay of the same real trace at these same eta values [ARTIFACT:art_bHFxugXcpJMg] finds the adversarial-regime trend running in the *opposite* direction using its own aggregate-deviation statistic; we trace this disagreement to the small number of requests that policy replay admits at large eta in the adversarial regime (as few as 7 admissions across the full regime at eta = 0.2), where Section 3's theorem bound is itself vacuous ($B/(\eta N_T) > 1$) and any statistic computed over that few admissions is correspondingly unstable. This is exactly the precondition failure the theorem in Section 3 predicts, and we report it rather than reconciling the two numbers by picking the more favorable one.

## The Value-Aware Admission Layer: A Negative Result on the Real Trace

We compared the value-aware admission rule against FCFS admission within the conformal eligibility set, using the regime-switch regime (chosen because the stationary regime's near-constant SLO target across its dominant function makes the value proxy nearly degenerate there). The two variants' MAD from alpha are statistically indistinguishable (FCFS 0.0679 vs. knapsack 0.0683, bootstrap 95% CI on the difference [-0.0024, 0.0040], including zero), confirming that reordering admissions among already-eligible requests does not measurably affect the safety guarantee, as the mechanism in Section 3.2 predicts by construction. Total accepted value, however, does *not* show the statistically significant gain an earlier, self-generated-simulator iteration of this study reported: knapsack admits 235,006 value units against FCFS's 234,913, a gain of 93 units whose bootstrap 95% confidence interval ([-4,481, 4,621]) comfortably includes zero [ARTIFACT:art_k4NZEyG_q_yz]. We report this as a genuine negative result rather than reframing it: on this real trace and value proxy, the deterministic value signal used here does not vary enough within a control interval's eligible set, once conditioned on the risk score it is partly derived from, to give a knapsack reordering meaningfully more to work with than first-come-first-served already captures.

## Robustness Check: Agreement with the Earlier Self-Generated Simulator

An earlier iteration of this study reported an evaluation from a self-generated multi-regime traffic simulator, used because the real-trace dataset and its consuming experiment artifact were both unavailable at that evaluation's run time. We retain that evaluation only as a labeled secondary robustness check, never blended into the primary numbers above. Its cell-level tolerance-pass/fail verdicts agree with the real-trace results reported here in 15 of 25 compared cells (60%) [ARTIFACT:art_k4NZEyG_q_yz]. Every disagreement runs in the same direction: the self-generated simulator reported a tolerance *pass* where the real trace shows a *fail*, in the low-natural-rate regimes (stationary, burst) where Section 5.1 shows the tolerance line is structurally unattainable at the real trace's actual base rates. This is consistent with, not contradictory to, the structural explanation in Section 5.1: a synthetic simulator whose regime generator does not reproduce the same extreme natural-rate asymmetry the real Azure trace exhibits will not reproduce the same structural tolerance failures either.

# Discussion

The central empirical finding of this iteration is not that the conformal controller failed to replicate an earlier, more uniformly positive result -- it is that the earlier result's framing (a single tolerance line, uniformly applied) obscured a structural fact about the traffic itself, which only became visible once the policy was tested against a dataset whose regimes were built independently of the policy code, rather than tuned by the same script that implements the policy under test. Once that structural fact is accounted for, the theoretical claim behind Adaptive Conformal Inference [2] is upheld precisely where it is actually being tested: in the two regimes where the target rate constrains real behavior (drift and adversarial), the conformal controller is the only non-oracle policy within tolerance in drift, and materially closer to the target than every frozen baseline in adversarial, exactly the pattern the theorem in Section 3 predicts for a policy that corrects toward the target regardless of what generated the last outcome, versus baselines that either never correct (fixed threshold, misspecified index) or correct only for the distribution seen at training time (frozen RL).

**Addressing the two structural-rigor critiques from the previous review.** First, on evidentiary grounding: this iteration's headline numbers come from a policy-implementation artifact that loads the frozen, independently-built real-trace dataset through data-loading code kept apart from the five policy implementations, with policies touching ground truth only through an explicit per-decision feedback call [ARTIFACT:art_bHFxugXcpJMg], and a separately authored verdict artifact that re-implements the same five policies from the plan's specification directly against that same frozen dataset as a cross-check [ARTIFACT:art_k4NZEyG_q_yz]. The two implementations largely agree at the level of tolerance-pass/fail verdicts and the qualitative pattern in Table 1, and where they disagree (the eta-sensitivity direction in the sparsely-admitting adversarial regime, Section 5.3), we report the disagreement rather than resolving it in the more favorable direction, and trace it to the small-$N_T$ failure mode the finite-sample theorem itself predicts. Second, on the formal guarantee: Section 3 now states the tracking bound as an explicit theorem with an explicit proof sketch, in the paper's own $(\lambda_t, y_t, \alpha, \eta)$ notation, including the admission-conditional deviation from the original ACI update and the precondition -- observability of $y_t$ within a bounded delay, and a bound stated over admitted count $N_T$ rather than raw arrival count $T$ -- that the admission-control setting must satisfy for the guarantee to be non-vacuous.

**Limitations.** First, and most importantly, the 3-percentage-point tolerance criterion pre-registered for this study is not a regime-agnostic measure of policy quality, as Section 5.1 shows directly: it can only be failed or passed meaningfully in a regime whose natural violation rate is not already far from the target, and future iterations of this evaluation should either set alpha relative to each regime's natural rate or restrict the tolerance-pass criterion to regimes where it is a genuine test, rather than reporting an aggregate pass count across regimes with structurally different answers. Second, the frozen reinforcement-learning baseline is a single frozen logistic-regression-style controller trained once on the stationary regime, standing in for, rather than reproducing, a full deep-RL system such as TopFull [4]; a continually retrained or online-fine-tuned learned controller might narrow the drift-regime gap this paper reports without closing the qualitative distinction, since even a retrained learned policy would still lack a finite-sample guarantee on its retrained state. Third, the value-aware admission layer's null result in Section 5.4 is specific to the deterministic value proxy used here, which is partly derived from the same risk score that determines eligibility; a genuinely independent value signal -- a real per-tenant billing weight, for instance -- might still show the gain an earlier, self-generated-simulator evaluation of this same mechanism reported, and this remains untested against the real trace. Fourth, as flagged in Section 3, the outcome-observation delay in this evaluation is effectively immediate, matching the theorem's precondition; a production deployment where SLO violations are confirmed only after a longer delay would need eta re-tuned against that delay, and the guarantee would then apply to a correspondingly longer effective window than the nominal one. Finally, as stated in the Introduction, the guarantee evaluated throughout this paper is for a single, shared scalar threshold over one queue or endpoint class; it is not a claim about coordinated per-function or per-tenant guarantees at the fleet scale that motivates the problem, and extending it to a joint multi-threshold budget is future work.

# Conclusion

This paper evaluated an admission-control policy built entirely from an online conformal-inference threshold update -- with no queueing model, no trained neural policy, and no exchangeability assumption -- against a real, independently-produced 210,000-request Azure Functions trace spanning five traffic regimes, closing an evidentiary gap left open by an earlier iteration of this study that had evaluated the same mechanism only against a self-generated simulator. The central finding is not simply that the conformal controller passed or failed a single pre-registered tolerance test; it is that the test itself is only a fair measure of policy quality in regimes where the target violation rate constrains real behavior. In those regimes -- drift, where the natural violation rate (15.53%) exceeds the 10% target, and an adversarially constructed sequence designed to defeat a fixed rule -- the conformal controller is the only non-oracle policy within the pre-registered tolerance in drift, and is significantly closer to the target than a frozen reinforcement-learning-style baseline in the adversarial regime, while remaining statistically indistinguishable from a well-calibrated fixed threshold at matched safety. In regimes whose natural violation rate already sits far from the target, even a hindsight-optimal oracle cannot pass the tolerance criterion, a structural fact this paper establishes rather than obscures. A value-aware admission layer, by contrast, shows no significant value gain over first-come-first-served on this real trace, reversing a positive finding from an earlier, self-generated-simulator evaluation of the same mechanism -- reported here as a genuine negative result rather than smoothed over.

Future work includes: setting the target rate alpha relative to each traffic regime's own natural violation rate, rather than a single global value, so that the tolerance criterion is a fair test in every regime rather than only some; extending the single-scalar threshold to a small number of per-endpoint or per-tenant thresholds under a joint violation-rate budget, closing the gap between the fleet-scale motivation in the Introduction and the single-threshold scope evaluated here; adopting a strongly-adaptive, multi-window online conformal update [10] or a parameter-free, group-conditional variant [11] in place of the plain single-eta ACI rule used here, which Section 5.3's eta-sensitivity results suggest could remove the need to hand-tune eta per regime; and testing the value-aware admission layer against a genuinely independent value signal, since the null result reported here may be specific to a value proxy that shares information with the eligibility-determining risk score.

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

[10] Bhatnagar, A., Wang, H., Xiong, C., & Bai, Y. (2023). Improved Online Conformal Prediction via Strongly Adaptive Online Learning. *International Conference on Machine Learning*. arXiv:2302.07869.

[11] Bharti, B., Pal, A., Teneggi, J., & Sulam, J. (2026). Parameter-Free and Group Conditional Online Conformal Prediction. arXiv:2606.00419.

</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (evidence) The paper's two clearest positive results are both compromised by the paper's own stated precondition for the theorem to be non-vacuous. In drift, the pass is real but the margin is modest (MAD 0.028 vs. a target-tolerance line of 0.03, i.e. barely inside). In adversarial, the 'win' over baselines is computed with as few as 56-367 admitted requests per cell, which the paper itself says puts the theorem's bound (B/(eta*N_T) > 1) in vacuous territory, and a second, independently authored replay at the same eta values finds the opposite eta-sensitivity trend there for exactly this reason. The paper reports this disagreement honestly, but the headline 'materially closer to the target than every frozen baseline in adversarial' claim in the Abstract/Introduction is stated without that same caveat attached.
  Action: Attach the small-N/vacuous-bound caveat directly to every place the adversarial-regime win is claimed as a headline result (Abstract, Introduction, Conclusion), not only in Section 5.3's discussion of the eta-sensitivity disagreement, and/or re-run the adversarial regime with a design (larger dataset, less extreme score separation) that yields enough admissions for the theorem's own bound to be non-vacuous before reporting it as a clean win.
- [MAJOR] (methodology) The 'frozen reinforcement-learning baseline' is, per the artifact, a single frozen logistic-regression contextual-bandit-style controller trained once on stationary traffic -- not a reinforcement-learning system, and not compared against TopFull or any real deep-RL overload controller from the literature this paper cites as motivation. Framing it throughout the main text as 'the frozen reinforcement-learning baseline' (rather than consistently as 'a logistic-regression stand-in for a learned controller') overstates the strength of the comparison the conformal controller is shown to beat, especially since the adversarial-regime win over this baseline is the paper's single Holm-significant result there.
  Action: Rename the baseline consistently throughout the main text (not only in Limitations) to something like 'frozen supervised stand-in for a learned controller,' and either implement a genuinely retrained/online-updated learned baseline as a sixth policy or explicitly scope the claim as 'beats a controller that cannot adapt at all,' which is a materially weaker and more honest claim than 'beats a reinforcement-learning controller.'
- [MINOR] (methodology) In Table 1, the fixed-threshold and misspecified index-based baselines produce nearly identical MAD in every regime (e.g., drift: 0.0559 vs. 0.0556; stationary: 0.0599 vs. 0.0605), despite being conceptually different policies (a static score cutoff vs. a queueing-theoretic load index). This near-tie is never discussed, and it raises the question of whether the index-based baseline is meaningfully exercising queueing-theoretic reasoning at all, or effectively degenerates to a similarly static rule on this dataset.
  Action: Add a sentence in Section 5.2 explaining why the two structurally different baselines converge to nearly the same MAD across all five regimes -- e.g., because neither has access to a feedback signal and both therefore behave as static thresholds on this trace -- so the near-tie reads as an expected structural fact rather than an unexplained coincidence a reviewer has to wonder about.
- [MINOR] (novelty) The related-work section correctly identifies that no prior work applies conformal risk control / ACI to systems admission control, and appropriately cites the two post-2022 online conformal tracking extensions ([10], [11]) as motivated future work rather than claiming to have used the strongest available variant. This adequately resolves the prior review's minor novelty concern, but the paper still evaluates only the plainest possible ACI variant, so its claim to generality ('this paper's ... approach') is really a claim about the single-eta update specifically, and a reader could reasonably ask whether the drift-regime win would strengthen or weaken under a strongly-adaptive multi-window rule.
  Action: Either run one of the two cited post-2022 variants as an additional condition in the eta-sensitivity or headline comparison (this would also directly test the paper's own hypothesis in the Future Work section that it 'could remove the need to hand-tune eta per regime'), or soften the framing in the Contributions list to explicitly scope the claim to the single-parameter ACI update rather than 'conformal admission control' as a general class.
- [MINOR] (clarity) Table 1's pass/fail flags are computed against the pre-registered 3-percentage-point tolerance, but the table caption and surrounding text do not make it immediately clear to a skimming reader that 4 of 5 'fail' rows for the conformal policy are structurally unattainable (per Section 5.1's own argument) rather than genuine tracking failures -- a reader who reads only Table 1 without the surrounding prose would reasonably conclude the method fails 4 out of 5 regimes outright.
  Action: Add a third status category to the table beyond pass/fail -- e.g., 'fail (structurally unattainable, see 5.1)' vs. 'fail (genuine miss)' -- so the table is self-contained and does not require reading Section 5.1's prose to correctly interpret the four non-drift 'fail' entries.
- [MINOR] (scope) The Introduction still opens with fleet-scale motivation (a serverless platform processing invocations across many functions and tenants) before narrowing, in its second paragraph, to the single-shared-threshold scope actually evaluated. This is an improvement over the prior draft (the narrowing now happens in the Introduction itself, not only in Limitations), but the gap between the motivating scenario and the evaluated mechanism is still large enough that a reader could reasonably expect per-function or per-tenant results that the paper does not provide.
  Action: Consider swapping the order: open with the single-queue/single-endpoint-class problem actually solved, and introduce the fleet-scale motivation only as the reason this narrower problem matters, rather than opening at fleet scale and then narrowing -- this would remove any residual expectation-setting mismatch without requiring new experiments.
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

### [2] HUMAN-USER prompt · 2026-08-25 19:23:37 UTC

```
Find a better admission control policy for overloaded request queues.
```
