# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_plan`
> Run: `iter1_88afd6206a08` — Conformal Admission Control for Overloaded Request Queues
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_experiment_1` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-08-25 18:40:16 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_plan/gen_plan_experiment_1
```

### [2] SYSTEM-USER prompt · 2026-08-25 18:40:22 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A plan generator (Step 3.2: GEN_PLAN in the invention loop)

You received the hypothesis, an artifact direction to elaborate, and dependency artifacts relevant to the plan.
Your job: elaborate this direction into a detailed, actionable plan for the executor agent.

Specific, actionable plan → valuable artifact. Vague plan → wasted execution.
</your_role>
</ai_inventor_context>

<artifact_type_info>
You are expanding an artifact direction of type: EXPERIMENT

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance
</artifact_type_info>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **SPEND BUDGET**: at most $10 USD of OpenRouter API calls for this artifact. Nothing outside your own code enforces this — the key you are given has no per-artifact cap — so it holds only if you track cumulative cost after every call and stop when you approach it. Budget the work up front: estimate the per-call cost and the number of calls BEFORE starting a sweep, not after it overruns. Exceeding it spends real money that the run cannot recover.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Free-first web search (general + scholarly modes), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-concept-fig-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<time_budget>

The experiment executor has 6h total (including writing code, debugging, testing, and fixing errors).

</time_budget>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<plan_guidelines>
You are expanding an artifact direction from the strategy into a detailed plan.
The artifact direction specifies what to do at a high level (type, objective, approach, dependencies).
Your job is to make it concrete and actionable as a detailed plan.
Use web research to look up technical details, verify feasibility, and find reference materials
that will make your plan more concrete and actionable for the executor.

GOOD PLANS:
- Make each component SPECIFIC and actionable (not vague platitudes)
- Consider both success AND failure scenarios
- Build on the approach in the artifact direction
- Add concrete details the executor needs

BAD PLANS:
- Vague hand-waving ("do research on X")
- Ignoring the approach in the artifact direction
- Missing critical details the executor needs
</plan_guidelines>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<hypothesis>
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
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter2_dir1
type: experiment
objective: >-
  Run the ACI-based conformal admission controller and the four baselines (fixed threshold, misspecified index policy, RL
  frozen on the stationary regime, hindsight-optimal oracle) directly against the frozen, real, trace-derived dataset (art_fAlkDy9YEd-N),
  using its already-computed risk_score, slo_target, regime_label, and ground-truth violation labels as fixed, external inputs
  the policy code never generates itself -- closing the self-referential-evaluation gap the reviewer flagged as MAJOR.
approach: >-
  Load the four data_out part files directly (do not re-derive regimes, SLO targets, or risk scores -- treat the dataset's
  per-example `input`/`output`/metadata_* fields as ground truth exactly as documented in its own summary, so this script
  has zero authorship overlap with the label-generation logic). Replay each regime's rows in arrival-time order through a
  lightweight event loop (no re-simulation of the queue itself is needed since realized service_time/violation outcome is
  already logged per row; the loop's only job is to decide admit/reject via each policy's rule and then feed the row's pre-computed
  outcome back into that policy's own state update, e.g. lambda_t for conformal). Implement the conformal policy exactly as
  lambda_{t+1} = lambda_t + eta*(alpha - y_t), admit iff s(x)<=lambda_t, with alpha=0.10 and eta swept over 5 pre-registered
  values (e.g. 0.01, 0.02, 0.05, 0.1, 0.2) reported numerically with the code's exact update loop as pseudocode/docstring,
  and document the risk-score formula already fixed in the dataset (closed-form, O(1) per request) verbatim in this script's
  docstring so the paper can quote it precisely. Re-implement the fixed-threshold, misspecified-index, frozen-RL, and oracle
  baselines from the iteration-1 design but keep policy code and data-loading code in clearly separate functions/modules with
  the data loader importing nothing from the policy module, so a reader can audit that ground truth is not touched by policy
  logic. Run every (policy, regime, eta) cell with >=5 independent seeds (varying admission tie-breaking / RL training seed
  only, never the trace data) and log per-decision (admit/reject, outcome, threshold value, timestamp) plus a fixed seed manifest
  to method_out.json so results are independently reproducible.
depends_on:
- id: art_fAlkDy9YEd-N
  label: dataset
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
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
out_dependency_files:
  file_list:
  - data.py
  - full_data_out/full_data_out_1.json
  - full_data_out/full_data_out_2.json
  - full_data_out/full_data_out_3.json
  - full_data_out/full_data_out_4.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out/full_data_out_1.json
  - full_data_out/full_data_out_2.json
  - full_data_out/full_data_out_3.json
  - full_data_out/full_data_out_4.json
  - mini_data_out.json
  - preview_data_out.json
</dependencies>

<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for experiment artifacts:
  - gpu: 1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models (fallback: GPUs cheap→expensive: 2000 Ada → A4000 → 4000 Ada → L4 → 4090 → 5090)
  - cpu_heavy: 4 vCPUs, 32GB RAM — large datasets, memory-intensive processing (fallback: CPUs cheap→expensive, then GPU hosts cheap→expensive (all ≥32GB RAM))

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
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
  "description": "Plan for an EXPERIMENT artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-25 18:40:22 UTC

```
Find a better admission control policy for overloaded request queues.
```

### [4] TOOL CALL — Write · 2026-08-25 18:41:34 UTC

```
File: /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json

{
  "title": "Conformal Admission Control on Real Azure Traces",
  "summary": "Run the ACI-based conformal admission controller plus four baselines (fixed threshold, misspecified index policy, RL frozen on stationary regime, hindsight-optimal oracle) directly against the frozen, real Azure-trace-derived dataset (art_fAlkDy9YEd-N, 210k rows / 5 regimes), with data-loading code strictly separated from policy code to close the self-referential-evaluation gap flagged in iteration 1. Sweep eta over 5 pre-registered values, run >=5 seeds per (policy, regime, eta) cell, and report violation-rate control and value-at-matched-safety with bootstrap CIs and Holm-corrected pairwise tests.",
  "runpod_compute_profile": "cpu_heavy",
  "implementation_pseudocode": "# === MODULE 1: data_loader.py  (imports NOTHING from policy.py) ===\n# Purpose: read the 4 dataset part files, reconstruct 210k rows, group by regime,\n# sort each regime by arrival_time. Exposes ONLY read-only accessor functions.\n\ndef load_dataset(dataset_dir):\n    rows = []\n    for part_path in sorted(glob(f\"{dataset_dir}/full_data_out/full_data_out_*.json\")):\n        part = json.load(open(part_path))\n        rows.extend(part['datasets'][0]['examples'])\n    # each example: input = JSON string {arrival_time, risk_score, slo_target,\n    #   regime_label, function_id, is_synthetic}; output = 0/1 violation label\n    parsed = []\n    for ex in rows:\n        feat = json.loads(ex['input'])\n        parsed.append({\n            'arrival_time': feat['arrival_time'],\n            'risk_score': feat['risk_score'],\n            'slo_target': feat['slo_target'],\n            'regime': feat['regime_label'],\n            'function_id': feat['function_id'],\n            'is_synthetic': feat['is_synthetic'],\n            'y': int(ex['output']),                     # ground-truth violation label\n            'value': feat.get('value', estimate_value_proxy(feat)),  # if dataset lacks\n                                                          # an explicit value field, define\n                                                          # value = 1.0 (uniform) as the\n                                                          # documented fallback -- log which\n                                                          # branch was taken in method_out.json\n            'realized_service_time': ex['metadata_realized_service_time'],\n        })\n    return parsed\n\ndef group_by_regime_sorted(parsed_rows):\n    by_regime = defaultdict(list)\n    for r in parsed_rows:\n        by_regime[r['regime']].append(r)\n    for regime in by_regime:\n        by_regime[regime].sort(key=lambda r: r['arrival_time'])\n    return by_regime   # {'stationary': [...], 'burst': [...], 'drift': [...],\n                        #  'regime_switch': [...], 'adversarial': [...]}\n\n# VALIDATE ON LOAD: assert len(parsed_rows) == 210000; assert set(by_regime.keys())\n# == {'stationary','burst','drift','regime_switch','adversarial'}; assert observed\n# per-regime violation rates are within ~1pp of the documented rates\n# (stationary 3.95%, burst 0.24%, drift 15.53%, regime_switch 3.09%, adversarial\n# 38.25%) -- fail loudly (raise, do not silently continue) if this check fails,\n# since it is the first, cheapest signal that the loader has misread the schema.\n\n\n# === MODULE 2: policy.py  (imports NOTHING from data_loader.py; pure functions\n# of a stream of (risk_score, slo_target, ...) inputs and externally-supplied\n# outcome labels -- never touches ground truth except via the replay loop's\n# explicit feedback call) ===\n\nclass ConformalPolicy:\n    \"\"\"\n    ACI admission rule (Gibbs & Candes 2021 single-parameter online\n    gradient update), applied to admission instead of prediction-interval\n    coverage:\n        lambda_{t+1} = lambda_t + eta * (alpha - y_t)\n        admit request t  iff  s(x_t) <= lambda_t\n    where y_t in {0,1} is the SLO-violation OUTCOME of request t if admitted\n    (0 if rejected -- rejected requests contribute no feedback and lambda_t\n    is carried forward unchanged, since there is no observed outcome to\n    condition on; this is documented explicitly as a deviation worth noting\n    since Gibbs & Candes' original setting always observes an outcome).\n    alpha = target violation rate (0.10). eta = step size, swept over\n    {0.01, 0.02, 0.05, 0.10, 0.20}.\n    lambda_0 initialized to a generous starting quantile\n    (e.g. the 90th percentile of risk_score over a small warm-up prefix of\n    the FIRST 200 rows of the regime being run, held out from evaluation --\n    NOT the whole regime, to avoid look-ahead) so early decisions are not\n    degenerate.\n    \"\"\"\n    def __init__(self, alpha, eta, lambda_0):\n        self.alpha, self.eta, self.lam = alpha, eta, lambda_0\n        self.history = []  # (t, lambda_t, admit, s, y_observed)\n\n    def decide(self, s_x):\n        return s_x <= self.lam           # admit iff score <= current threshold\n\n    def update(self, admitted, y_t):\n        if admitted:\n            self.lam = self.lam + self.eta * (self.alpha - y_t)\n        # else: lambda unchanged (no observed outcome)\n\nclass FixedThresholdPolicy: ...      # threshold tuned once on stationary-regime\n                                       # warm-up prefix to hit target alpha, then\n                                       # frozen for the rest of that regime AND\n                                       # reused unchanged on every other regime\nclass MisspecifiedIndexPolicy: ...    # Whittle/marginal-productivity-style index\n                                       # computed under an assumed birth-death /\n                                       # M/M/1-ish queueing model fit ONLY on the\n                                       # stationary-regime warm-up prefix (this is\n                                       # the \"misspecification\": the model is wrong\n                                       # for burst/drift/regime_switch/adversarial\n                                       # by construction)\nclass FrozenRLPolicy: ...             # small tabular/linear-function-approx\n                                       # Q-learning or REINFORCE agent, state =\n                                       # (discretized risk_score, discretized\n                                       # recent violation rate), trained ONLY on\n                                       # the stationary regime's warm-up prefix\n                                       # (e.g. first 20% of stationary rows),\n                                       # then policy FROZEN (no further learning)\n                                       # for evaluation on all 5 regimes\nclass OracleHindsightPolicy: ...      # given full knowledge of this regime's\n                                       # y-labels in advance, solve the offline\n                                       # knapsack: admit the max-value subset\n                                       # whose realized violation rate <= alpha\n                                       # (LP relaxation + rounding, or greedy by\n                                       # value/1 with a violation-budget cap) --\n                                       # this is the value-vs-safety upper bound,\n                                       # not a deployable policy\n\n\n# === MODULE 3: replay.py (the event loop; imports both modules but keeps them\n# used only through their public functions) ===\n\ndef replay_regime(rows, policy, rng_seed):\n    rng = np.random.default_rng(rng_seed)   # used ONLY for admission tie-\n                                             # breaking (e.g. among equal scores)\n                                             # and RL exploration noise during its\n                                             # separate training phase -- NEVER to\n                                             # perturb the trace data itself\n    log = []\n    for t, row in enumerate(rows):\n        admit = policy.decide(row['risk_score'], tie_break_rng=rng)\n        y_t = row['y'] if admit else None   # outcome only observed if admitted\n        policy.update(admit, row['y'] if admit else 0)\n        log.append({\n            't': t, 'timestamp': row['arrival_time'], 'admit': bool(admit),\n            'outcome': (row['y'] if admit else None),\n            'threshold': getattr(policy, 'lam', None),\n            'value_if_admitted': row['value'] if admit else 0.0,\n        })\n    return log\n\ndef compute_metrics(log, alpha, window=2000):\n    # rolling-window realized violation rate among ADMITTED requests only\n    admitted = [e for e in log if e['admit']]\n    y = [e['outcome'] for e in admitted]\n    rolling = rolling_mean(y, window)\n    mad_vs_alpha = mean(abs(r - alpha) for r in rolling)   # headline stat,\n                                                            # matches iter-1's\n                                                            # Table 1 metric\n    total_value = sum(e['value_if_admitted'] for e in log)\n    admit_rate = len(admitted) / len(log)\n    return {'mad_vs_alpha': mad_vs_alpha, 'rolling_violation_rate': rolling,\n            'total_value': total_value, 'admit_rate': admit_rate,\n            'n_admitted': len(admitted)}\n\n\n# === MAIN DRIVER (main.py) ===\n\nALPHA = 0.10\nETAS = [0.01, 0.02, 0.05, 0.10, 0.20]\nSEEDS = list(range(5))            # >=5 independent seeds per cell, as required\nREGIMES = ['stationary', 'burst', 'drift', 'regime_switch', 'adversarial']\nPOLICIES = ['conformal', 'fixed_threshold', 'misspecified_index',\n            'frozen_rl', 'oracle']\n\nrows = load_dataset(DATASET_DIR)\nby_regime = group_by_regime_sorted(rows)\nvalidate_regime_rates(by_regime)   # hard assert per the doc'd violation rates\n\nresults = []                       # flat list of per-cell metric dicts\nfor regime in REGIMES:\n    regime_rows = by_regime[regime]\n    warmup, eval_rows = regime_rows[:200], regime_rows[200:]  # warm-up excluded\n                                                                # from evaluation\n                                                                # metrics\n    for policy_name in POLICIES:\n        eta_grid = ETAS if policy_name == 'conformal' else [None]  # eta only\n                                                                     # applies to\n                                                                     # conformal\n        for eta in eta_grid:\n            for seed in SEEDS:\n                policy = build_policy(policy_name, alpha=ALPHA, eta=eta,\n                                       warmup_rows=warmup, seed=seed,\n                                       # RL and index policies are FIT ONLY on\n                                       # the STATIONARY regime's warm-up rows,\n                                       # never on the regime being evaluated,\n                                       # except when regime == 'stationary'\n                                       fit_rows=by_regime['stationary'][:2000]\n                                                if policy_name in\n                                                ('frozen_rl','misspecified_index')\n                                                else warmup)\n                log = replay_regime(eval_rows, policy, rng_seed=seed)\n                metrics = compute_metrics(log, ALPHA)\n                results.append({'regime': regime, 'policy': policy_name,\n                                 'eta': eta, 'seed': seed, **metrics})\n\n# statistical layer\nper_cell = aggregate_over_seeds(results)   # mean/CI via seed-level bootstrap\n                                            # (percentile bootstrap, 10000 resamples)\npairwise = holm_corrected_tests(results,   # conformal vs each baseline, per\n                                 groupby=['regime'], metric='mad_vs_alpha',\n                                 method='holm')  # re-test the 2 stationary-\n                                                  # regime comparisons flagged\n                                                  # non-significant in iter 1\n                                                  # (p_holm=0.098 vs fixed-\n                                                  # threshold and frozen-RL) --\n                                                  # now with >=5 seeds x the\n                                                  # real trace, check whether\n                                                  # significance is reached\n\n# Phase 3: value-aware knapsack layer vs FCFS-among-eligible, same conformal\n# eligibility set, best eta selected from the Phase-0/1 sweep by MAD-to-alpha\nknapsack_results = run_knapsack_vs_fcfs(by_regime, best_eta, ALPHA, SEEDS)\n\nwrite_method_out_json({\n  'table1_violation_rate_by_regime_policy': per_cell,\n  'eta_sensitivity_sweep': {r: {e: per_cell[(r,'conformal',e)] for e in ETAS}\n                             for r in REGIMES},\n  'pairwise_significance_tests': pairwise,\n  'value_at_matched_safety_stationary': ...,\n  'knapsack_vs_fcfs': knapsack_results,\n  'risk_score_formula_verbatim': RISK_SCORE_DOCSTRING_COPIED_FROM_DATASET,\n  'aci_update_rule_docstring': ConformalPolicy.__doc__,\n  'seed_manifest': {'seeds': SEEDS, 'etas': ETAS, 'alpha': ALPHA},\n  'dataset_validation': {'n_rows': len(rows), 'per_regime_violation_rate': ...},\n})",
  "fallback_plan": "1) If the dataset's `input`/`output` schema does not literally match the documented field names (e.g. `risk_score` or `regime_label` missing or nested differently), first inspect `preview_data_out.json` (3 rows) before touching the full 210k-row files, adapt the loader's field-mapping only, and log the concrete schema in method_out.json rather than guessing. 2) If no explicit per-row `value` field exists in the dataset (the summary does not mention one explicitly), fall back to a documented, fixed value proxy (e.g. value = 1.0 uniformly, or value = 1/risk_score as a crude priority proxy) and state this substitution explicitly in method_out.json and flag it as a known limitation for the paper -- do not silently invent per-row values that could be mistaken for ground truth. 3) If the frozen-RL baseline is unstable or fails to train a sensible policy on only ~2000 stationary warm-up rows (a real risk with e.g. tabular Q-learning on sparse admission data), fall back to a simpler contextual-bandit-style linear policy (e.g. logistic regression on risk_score fit on the same warm-up rows, thresholded) and clearly document it as 'RL-style baseline (simplified)' rather than a full DRL agent -- the comparison's purpose (empirical-only safety, no formal guarantee) is preserved either way. 4) If the misspecified-index policy is hard to derive cleanly from Nino-Mora's polyhedral construction in the time available, substitute a simpler but still genuinely model-based baseline: fit an M/M/1-style queueing model (arrival rate, service rate) on the stationary warm-up prefix and derive an admission threshold from its steady-state overflow probability formula -- keep it clearly 'model-based, distributionally misspecified' in spirit. 5) If full 5-seed x 5-eta x 5-regime x 5-policy runs (625 cells, but conformal alone needs 5 regimes x 5 etas x 5 seeds = 125, others are 5 regimes x 1 eta x 5 seeds x 4 policies = 100, total 225 replay runs) are too slow given 210k rows, first profile a single replay of the largest regime; each replay is O(N) with O(1) per-row work, so 225 replays over ~50k rows average is well under an hour on cpu_heavy -- if still slow, parallelize regime x policy x eta x seed cells across processes (aii-parallel-computing, ProcessPoolExecutor) since cells are fully independent. 6) If the headline MAD-vs-alpha result does NOT hold within tolerance on the real trace data (unlike the self-generated simulator in iteration 1), do NOT suppress or rerun until it looks better -- report it exactly as found, since a disconfirming result on the primary real-data evaluation is itself the single most important finding this iteration is designed to surface, and downstream (paper) steps need the true number, not a flattering one. 7) If part files fail to load due to size (out-of-memory reading all 4 x ~50MB files at once), stream/parse them one at a time and only retain the parsed lightweight row dicts, discarding the raw JSON structures immediately after parsing each part.",
  "testing_plan": "Step 1 (schema smoke test, seconds): load ONLY preview_data_out.json (3 rows) and mini_data_out.json through data_loader.py, print every parsed field, and manually verify against the dataset's documented schema (arrival_time, risk_score, slo_target, regime_label, function_id, is_synthetic, output-as-violation-label) before touching the full files. Step 2 (loader correctness on full data, ~1 regime): load just full_data_out_1.json, group by regime, and check per-regime violation rates against the documented figures (stationary 3.95%, burst 0.24%, drift 15.53%, regime_switch 3.09%, adversarial 38.25%) -- if these do not match within ~1pp, STOP and fix the loader before running any policy code, since every downstream number depends on this being correct. Step 3 (policy unit test on a tiny synthetic stream, not the real data): feed ConformalPolicy a hand-constructed sequence of 50 (score, outcome) pairs with a known closed-form expected lambda trajectory (e.g. all outcomes=1 should monotonically decrease lambda by eta*alpha... actually verify sign: y_t=1 means alpha-y_t<0 so lambda decreases, tightening admission -- confirm this matches intuition: more violations -> stricter threshold) and assert the implementation matches by hand-computed values to floating-point precision. Step 4 (single-cell end-to-end, ~1 min): run ONE (policy=conformal, regime=stationary, eta=0.1, seed=0) cell on the full stationary-regime rows, confirm it produces a metrics dict with sane ranges (0<=admit_rate<=1, 0<=mad_vs_alpha<=1, rolling violation rate roughly near alpha after burn-in) and that logs are non-empty and well-formed. Step 5 (small grid before full grid): run all 5 policies on just the stationary regime with 1 seed each (5 cells) and sanity-check relative behavior (oracle should have the highest value at matched safety; fixed-threshold/index/RL should behave reasonably in-distribution) before committing to the full 225-cell x 5-seed grid. Step 6 (full run): execute the complete grid, write method_out.json, then run aii-json validation on the output structure and spot-check that pairwise_significance_tests recomputes correctly by hand on 2-3 example cells (paired bootstrap CI and Holm correction). Step 7: confirm total wall-clock stayed well inside the 6h executor budget at each of the above checkpoints, aborting/simplifying per the fallback plan at the first checkpoint that looks too slow rather than discovering this at hour 5."
}
```

### [5] TOOL RESULT — Write · 2026-08-25 18:41:34 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Conformal Admission Control on Real Azure Traces\",\n  \"summary\": \"Run the ACI-based conformal admission controller plus four baselines (fixed threshold, misspecified index policy, RL frozen on stationary regime, hindsight-optimal oracle) directly against the frozen, real Azure-trace-derived dataset (art_fAlkDy9YEd-N, 210k rows / 5 regimes), with data-loading code strictly separated from policy code to close the self-referential-evaluation gap flagged in iteration 1. Sweep eta over 5 pre-registered values, run >=5 seeds per (policy, regime, eta) cell, and report violation-rate control and value-at-matched-safety with bootstrap CIs and Holm-corrected pairwise tests.\",\n  \"runpod_compute_profile\": \"cpu_heavy\",\n  \"implementation_pseudocode\": \"# === MODULE 1: data_loader.py  (imports NOTHING from policy.py) ===\\n# Purpose: read the 4 dataset part files, reconstruct 210k rows, group by regime,\\n# sort each regime by arrival_time. Exposes ONLY read-only accessor functions.\\n\\ndef load_dataset(dataset_dir):\\n    rows = []\\n    for part_path in sorted(glob(f\\\"{dataset_dir}/full_data_out/full_data_out_*.json\\\")):\\n        part = json.load(open(part_path))\\n        rows.extend(part['datasets'][0]['examples'])\\n    # each example: input = JSON string {arrival_time, risk_score, slo_target,\\n    #   regime_label, function_id, is_synthetic}; output = 0/1 violation label\\n    parsed = []\\n    for ex in rows:\\n        feat = json.loads(ex['input'])\\n        parsed.append({\\n            'arrival_time': feat['arrival_time'],\\n            'risk_score': feat['risk_score'],\\n            'slo_target': feat['slo_target'],\\n            'regime': feat['regime_label'],\\n            'function_id': feat['function_id'],\\n            'is_synthetic': feat['is_synthetic'],\\n            'y': int(ex['output']),                     # ground-truth violation label\\n            'value': feat.get('value', estimate_value_proxy(feat)),  # if dataset lacks\\n                                                          # an explicit value field, define\\n                                                          # value = 1.0 (uniform) as the\\n                                                          # documented fallback -- log which\\n                                                          # branch was taken in method_out.json\\n            'realized_service_time': ex['metadata_realized_service_time'],\\n        })\\n    return parsed\\n\\ndef group_by_regime_sorted(parsed_rows):\\n    by_regime = defaultdict(list)\\n    for r in parsed_rows:\\n        by_regime[r['regime']].append(r)\\n    for regime in by_regime:\\n        by_regime[regime].sort(key=lambda r: r['arrival_time'])\\n    return by_regime   # {'stationary': [...], 'burst': [...], 'drift': [...],\\n                        #  'regime_switch': [...], 'adversarial': [...]}\\n\\n# VALIDATE ON LOAD: assert len(parsed_rows) == 210000; assert set(by_regime.keys())\\n# == {'stationary','burst','drift','regime_switch','adversarial'}; assert observed\\n# per-regime violation rates are within ~1pp of the documented rates\\n# (stationary 3.95%, burst 0.24%, drift 15.53%, regime_switch 3.09%, adversarial\\n# 38.25%) -- fail loudly (raise, do not silently continue) if this check fails,\\n# since it is the first, cheapest signal that the loader has misread the schema.\\n\\n\\n# === MODULE 2: policy.py  (imports NOTHING from data_loader.py; pure functions\\n# of a stream of (risk_score, slo_target, ...) inputs and externally-supplied\\n# outcome labels -- never touches ground truth except via the replay loop's\\n# explicit feedback call) ===\\n\\nclass ConformalPolicy:\\n    \\\"\\\"\\\"\\n    ACI admission rule (Gibbs & Candes 2021 single-parameter online\\n    gradient update), applied to admission instead of prediction-interval\\n    coverage:\\n        lambda_{t+1} = lambda_t + eta * (alpha - y_t)\\n        admit request t  iff  s(x_t) <= lambda_t\\n    where y_t in {0,1} is the SLO-violation OUTCOME of request t if admitted\\n    (0 if rejected -- rejected requests contribute no feedback and lambda_t\\n    is carried forward unchanged, since there is no observed outcome to\\n    condition on; this is documented explicitly as a deviation worth noting\\n    since Gibbs & Candes' original setting always observes an outcome).\\n    alpha = target violation rate (0.10). eta = step size, swept over\\n    {0.01, 0.02, 0.05, 0.10, 0.20}.\\n    lambda_0 initialized to a generous starting quantile\\n    (e.g. the 90th percentile of risk_score over a small warm-up prefix of\\n    the FIRST 200 rows of the regime being run, held out from evaluation --\\n    NOT the whole regime, to avoid look-ahead) so early decisions are not\\n    degenerate.\\n    \\\"\\\"\\\"\\n    def __init__(self, alpha, eta, lambda_0):\\n        self.alpha, self.eta, self.lam = alpha, eta, lambda_0\\n        self.history = []  # (t, lambda_t, admit, s, y_observed)\\n\\n    def decide(self, s_x):\\n        return s_x <= self.lam           # admit iff score <= current threshold\\n\\n    def update(self, admitted, y_t):\\n        if admitted:\\n            self.lam = self.lam + self.eta * (self.alpha - y_t)\\n        # else: lambda unchanged (no observed outcome)\\n\\nclass FixedThresholdPolicy: ...      # threshold tuned once on stationary-regime\\n                                       # warm-up prefix to hit target alpha, then\\n                                       # frozen for the rest of that regime AND\\n                                       # reused unchanged on every other regime\\nclass MisspecifiedIndexPolicy: ...    # Whittle/marginal-productivity-style index\\n                                       # computed under an assumed birth-death /\\n                                       # M/M/1-ish queueing model fit ONLY on the\\n                                       # stationary-regime warm-up prefix (this is\\n                                       # the \\\"misspecification\\\": the model is wrong\\n                                       # for burst/drift/regime_switch/adversarial\\n                                       # by construction)\\nclass FrozenRLPolicy: ...             # small tabular/linear-function-approx\\n                                       # Q-learning or REINFORCE agent, state =\\n                                       # (discretized risk_score, discretized\\n                                       # recent violation rate), trained ONLY on\\n                                       # the stationary regime's warm-up prefix\\n                                       # (e.g. first 20% of stationary rows),\\n                                       # then policy FROZEN (no further learning)\\n                                       # for evaluation on all 5 regimes\\nclass OracleHindsightPolicy: ...      # given full knowledge of this regime's\\n                                       # y-labels in advance, solve the offline\\n                                       # knapsack: admit the max-value subset\\n                                       # whose realized violation rate <= alpha\\n                                       # (LP relaxation + rounding, or greedy by\\n                                       # value/1 with a violation-budget cap) --\\n                                       # this is the value-vs-safety upper bound,\\n                                       # not a deployable policy\\n\\n\\n# === MODULE 3: replay.py (the event loop; imports both modules but keeps them\\n# used only through their public functions) ===\\n\\ndef replay_regime(rows, policy, rng_seed):\\n    rng = np.random.default_rng(rng_seed)   # used ONLY for admission tie-\\n                                             # breaking (e.g. among equal scores)\\n                                             # and RL exploration noise during its\\n                                             # separate training phase -- NEVER to\\n                                             # perturb the trace data itself\\n    log = []\\n    for t, row in enumerate(rows):\\n        admit = policy.decide(row['risk_score'], tie_break_rng=rng)\\n        y_t = row['y'] if admit else None   # outcome only observed if admitted\\n        policy.update(admit, row['y'] if admit else 0)\\n        log.append({\\n            't': t, 'timestamp': row['arrival_time'], 'admit': bool(admit),\\n            'outcome': (row['y'] if admit else None),\\n            'threshold': getattr(policy, 'lam', None),\\n            'value_if_admitted': row['value'] if admit else 0.0,\\n        })\\n    return log\\n\\ndef compute_metrics(log, alpha, window=2000):\\n    # rolling-window realized violation rate among ADMITTED requests only\\n    admitted = [e for e in log if e['admit']]\\n    y = [e['outcome'] for e in admitted]\\n    rolling = rolling_mean(y, window)\\n    mad_vs_alpha = mean(abs(r - alpha) for r in rolling)   # headline stat,\\n                                                            # matches iter-1's\\n                                                            # Table 1 metric\\n    total_value = sum(e['value_if_admitted'] for e in log)\\n    admit_rate = len(admitted) / len(log)\\n    return {'mad_vs_alpha': mad_vs_alpha, 'rolling_violation_rate': rolling,\\n            'total_value': total_value, 'admit_rate': admit_rate,\\n            'n_admitted': len(admitted)}\\n\\n\\n# === MAIN DRIVER (main.py) ===\\n\\nALPHA = 0.10\\nETAS = [0.01, 0.02, 0.05, 0.10, 0.20]\\nSEEDS = list(range(5))            # >=5 independent seeds per cell, as required\\nREGIMES = ['stationary', 'burst', 'drift', 'regime_switch', 'adversarial']\\nPOLICIES = ['conformal', 'fixed_threshold', 'misspecified_index',\\n            'frozen_rl', 'oracle']\\n\\nrows = load_dataset(DATASET_DIR)\\nby_regime = group_by_regime_sorted(rows)\\nvalidate_regime_rates(by_regime)   # hard assert per the doc'd violation rates\\n\\nresults = []                       # flat list of per-cell metric dicts\\nfor regime in REGIMES:\\n    regime_rows = by_regime[regime]\\n    warmup, eval_rows = regime_rows[:200], regime_rows[200:]  # warm-up excluded\\n                                                                # from evaluation\\n                                                                # metrics\\n    for policy_name in POLICIES:\\n        eta_grid = ETAS if policy_name == 'conformal' else [None]  # eta only\\n                                                                     # applies to\\n                                                                     # conformal\\n        for eta in eta_grid:\\n            for seed in SEEDS:\\n                policy = build_policy(policy_name, alpha=ALPHA, eta=eta,\\n                                       warmup_rows=warmup, seed=seed,\\n                                       # RL and index policies are FIT ONLY on\\n                                       # the STATIONARY regime's warm-up rows,\\n                                       # never on the regime being evaluated,\\n                                       # except when regime == 'stationary'\\n                                       fit_rows=by_regime['stationary'][:2000]\\n                                                if policy_name in\\n                                                ('frozen_rl','misspecified_index')\\n                                                else warmup)\\n                log = replay_regime(eval_rows, policy, rng_seed=seed)\\n                metrics = compute_metrics(log, ALPHA)\\n                results.append({'regime': regime, 'policy': policy_name,\\n                                 'eta': eta, 'seed': seed, **metrics})\\n\\n# statistical layer\\nper_cell = aggregate_over_seeds(results)   # mean/CI via seed-level bootstrap\\n                                            # (percentile bootstrap, 10000 resamples)\\npairwise = holm_corrected_tests(results,   # conformal vs each baseline, per\\n                                 groupby=['regime'], metric='mad_vs_alpha',\\n                                 method='holm')  # re-test the 2 stationary-\\n                                                  # regime comparisons flagged\\n                                                  # non-significant in iter 1\\n                                                  # (p_holm=0.098 vs fixed-\\n                                                  # threshold and frozen-RL) --\\n                                                  # now with >=5 seeds x the\\n                                                  # real trace, check whether\\n                                                  # significance is reached\\n\\n# Phase 3: value-aware knapsack layer vs FCFS-among-eligible, same conformal\\n# eligibility set, best eta selected from the Phase-0/1 sweep by MAD-to-alpha\\nknapsack_results = run_knapsack_vs_fcfs(by_regime, best_eta, ALPHA, SEEDS)\\n\\nwrite_method_out_json({\\n  'table1_violation_rate_by_regime_policy': per_cell,\\n  'eta_sensitivity_sweep': {r: {e: per_cell[(r,'conformal',e)] for e in ETAS}\\n                             for r in REGIMES},\\n  'pairwise_significance_tests': pairwise,\\n  'value_at_matched_safety_stationary': ...,\\n  'knapsack_vs_fcfs': knapsack_results,\\n  'risk_score_formula_verbatim': RISK_SCORE_DOCSTRING_COPIED_FROM_DATASET,\\n  'aci_update_rule_docstring': ConformalPolicy.__doc__,\\n  'seed_manifest': {'seeds': SEEDS, 'etas': ETAS, 'alpha': ALPHA},\\n  'dataset_validation': {'n_rows': len(rows), 'per_regime_violation_rate': ...},\\n})\",\n  \"fallback_plan\": \"1) If the dataset's `input`/`output` schema does not literally match the documented field names (e.g. `risk_score` or `regime_label` missing or nested differently), first inspect `preview_data_out.json` (3 rows) before touching the full 210k-row files, adapt the loader's field-mapping only, and log the concrete schema in method_out.json rather than guessing. 2) If no explicit per-row `value` field exists in the dataset (the summary does not mention one explicitly), fall back to a documented, fixed value proxy (e.g. value = 1.0 uniformly, or value = 1/risk_score as a crude priority proxy) and state this substitution explicitly in method_out.json and flag it as a known limitation for the paper -- do not silently invent per-row values that could be mistaken for ground truth. 3) If the frozen-RL baseline is unstable or fails to train a sensible policy on only ~2000 stationary warm-up rows (a real risk with e.g. tabular Q-learning on sparse admission data), fall back to a simpler contextual-bandit-style linear policy (e.g. logistic regression on risk_score fit on the same warm-up rows, thresholded) and clearly document it as 'RL-style baseline (simplified)' rather than a full DRL agent -- the comparison's purpose (empirical-only safety, no formal guarantee) is preserved either way. 4) If the misspecified-index policy is hard to derive cleanly from Nino-Mora's polyhedral construction in the time available, substitute a simpler but still genuinely model-based baseline: fit an M/M/1-style queueing model (arrival rate, service rate) on the stationary warm-up prefix and derive an admission threshold from its steady-state overflow probability formula -- keep it clearly 'model-based, distributionally misspecified' in spirit. 5) If full 5-seed x 5-eta x 5-regime x 5-policy runs (625 cells, but conformal alone needs 5 regimes x 5 etas x 5 seeds = 125, others are 5 regimes x 1 eta x 5 seeds x 4 policies = 100, total 225 replay runs) are too slow given 210k rows, first profile a single replay of the largest regime; each replay is O(N) with O(1) per-row work, so 225 replays over ~50k rows average is well under an hour on cpu_heavy -- if still slow, parallelize regime x policy x eta x seed cells across processes (aii-parallel-computing, ProcessPoolExecutor) since cells are fully independent. 6) If the headline MAD-vs-alpha result does NOT hold within tolerance on the real trace data (unlike the self-generated simulator in iteration 1), do NOT suppress or rerun until it looks better -- report it exactly as found, since a disconfirming result on the primary real-data evaluation is itself the single most important finding this iteration is designed to surface, and downstream (paper) steps need the true number, not a flattering one. 7) If part files fail to load due to size (out-of-memory reading all 4 x ~50MB files at once), stream/parse them one at a time and only retain the parsed lightweight row dicts, discarding the raw JSON structures immediately after parsing each part.\",\n  \"testing_plan\": \"Step 1 (schema smoke test, seconds): load ONLY preview_data_out.json (3 rows) and mini_data_out.json through data_loader.py, print every parsed field, and manually verify against the dataset's documented schema (arrival_time, risk_score, slo_target, regime_label, function_id, is_synthetic, output-as-violation-label) before touching the full files. Step 2 (loader correctness on full data, ~1 regime): load just full_data_out_1.json, group by regime, and check per-regime violation rates against the documented figures (stationary 3.95%, burst 0.24%, drift 15.53%, regime_switch 3.09%, adversarial 38.25%) -- if these do not match within ~1pp, STOP and fix the loader before running any policy code, since every downstream number depends on this being correct. Step 3 (policy unit test on a tiny synthetic stream, not the real data): feed ConformalPolicy a hand-constructed sequence of 50 (score, outcome) pairs with a known closed-form expected lambda trajectory (e.g. all outcomes=1 should monotonically decrease lambda by eta*alpha... actually verify sign: y_t=1 means alpha-y_t<0 so lambda decreases, tightening admission -- confirm this matches intuition: more violations -> stricter threshold) and assert the implementation matches by hand-computed values to floating-point precision. Step 4 (single-cell end-to-end, ~1 min): run ONE (policy=conformal, regime=stationary, eta=0.1, seed=0) cell on the full stationary-regime rows, confirm it produces a metrics dict with sane ranges (0<=admit_rate<=1, 0<=mad_vs_alpha<=1, rolling violation rate roughly near alpha after burn-in) and that logs are non-empty and well-formed. Step 5 (small grid before full grid): run all 5 policies on just the stationary regime with 1 seed each (5 cells) and sanity-check relative behavior (oracle should have the highest value at matched safety; fixed-threshold/index/RL should behave reasonably in-distribution) before committing to the full 225-cell x 5-seed grid. Step 6 (full run): execute the complete grid, write method_out.json, then run aii-json validation on the output structure and spot-check that pairwise_significance_tests recomputes correctly by hand on 2-3 example cells (paired bootstrap CI and Holm correction). Step 7: confirm total wall-clock stayed well inside the 6h executor budget at each of the above checkpoints, aborting/simplifying per the fallback plan at the first checkpoint that looks too slow rather than discovering this at hour 5.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [6] ASSISTANT · 2026-08-25 18:41:36 UTC

```
Plan written to `.terminal_claude_agent_struct_out.json` — a real-trace-only evaluation of the conformal admission controller vs. 4 baselines with strict data/policy code separation, eta sweep, 5-seed cells, and Holm-corrected significance tests, closing iteration 1's self-referential-evaluation gap.
```
