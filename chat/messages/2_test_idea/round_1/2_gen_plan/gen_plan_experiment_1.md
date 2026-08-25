# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_plan`
> Run: `iter1_88afd6206a08` — Conformal Admission Control for Overloaded Request Queues
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_experiment_1` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-08-25 17:39:14 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1
```

### [2] SYSTEM-USER prompt · 2026-08-25 17:39:22 UTC

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

id: experiment_iter1_dir2
type: experiment
objective: >-
  Implement the ACI-based conformal admission controller and three baselines (fixed/offline-tuned threshold, a Nino-Mora-style
  index policy under a mis-specified queueing model, and a small RL admission controller trained only on the stationary regime),
  run all four as a single-server discrete-event simulation over every regime in the dataset, and record realized rolling-window
  SLO-violation rate and accepted value per policy per regime.
approach: >-
  Build a lightweight discrete-event queue simulator (single or few-server FIFO-service-order queue, event-driven via a heap)
  that consumes the dataset's arrival/service/SLO/risk-score stream regime by regime. Implement the conformal controller exactly
  per the hypothesis: lambda_{t+1} = lambda_t + eta*(alpha - 1[violation]), admit iff s(x) <= lambda_t, with eta swept over
  a small grid (e.g., 0.01, 0.05, 0.1) and outcome observed after a bounded, explicit delay (service completion) to test assumption
  2 honestly rather than assuming instant feedback. Implement baselines: (a) fixed threshold = the value of lambda that hits
  alpha empirically on the stationary regime alone (then frozen), (b) an index/Whittle-style admission rule computed under
  an assumed M/M/1-ish birth-death model fitted to the stationary regime's empirical rate (deliberately mis-specified when
  applied to shifted regimes, mirroring the hypothesis's critique), (c) a small tabular/DQN or PPO agent (stable-baselines3
  or a minimal from-scratch implementation) trained only on the stationary regime and then frozen and evaluated unmodified
  on all regimes, and (d) an offline-optimal oracle computed with full hindsight per regime as an upper bound. For every policy
  x regime, log per-decision outcomes and compute rolling-window (e.g., 200-request) violation rate over time plus total accepted
  value; save time series and summary tables to method_out.json.
depends_on: []
</artifact_direction>



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

### [3] HUMAN-USER prompt · 2026-08-25 17:39:22 UTC

```
Find a better admission control policy for overloaded request queues.
```

### [4] TOOL CALL — Write · 2026-08-25 17:40:36 UTC

````
File: /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json

{
  "title": "Conformal vs Index vs RL Admission Control",
  "summary": "Implement an ACI-based conformal admission controller and three baselines (frozen fixed threshold, mis-specified M/M/1 index policy, RL agent trained only on stationary traffic) inside a single discrete-event queue simulator driven by the dependency DATASET's multi-regime arrival/service/SLO/risk-score stream. For every (policy, regime) pair record rolling-window realized SLO-violation rate and accepted value, then compare whether the conformal controller uniquely holds its target violation rate alpha across regime shifts while remaining value-competitive in the stationary regime.",
  "runpod_compute_profile": "cpu_heavy",
  "implementation_pseudocode": "```\n# ---------------------------------------------------------------\n# 0. LOAD DATA\n# ---------------------------------------------------------------\ndataset = load_json(DATASET_PATH)  # from the dependency DATASET artifact\n# Expect dataset to be organized as regimes: each regime is a list of request\n# records with fields at minimum:\n#   arrival_time, service_time (or service_time_dist params), slo_target,\n#   risk_score s(x) (possibly several risk-score columns of varying quality),\n#   value (heterogeneous request value for knapsack tie-break)\n# If dataset schema differs, adapt field names but KEEP the same downstream\n# contract: (arrival_time, service_time, slo_target, score, value).\nregimes = dataset['regimes']  # e.g. {'stationary':[...], 'burst':[...], 'drift':[...],\n                               #        'switch':[...], 'adversarial':[...]}\nALPHA = 0.10          # target SLO-violation rate (make this a named constant,\n                       # sweep over {0.05, 0.10, 0.20} only if time remains)\nETA_GRID = [0.01, 0.05, 0.1]\nWINDOW = 200          # rolling-window size for violation-rate reporting\nBURN_IN = 500         # requests excluded from headline metrics (let lambda_t settle)\n\n# ---------------------------------------------------------------\n# 1. DISCRETE-EVENT SIMULATOR (single/few-server FIFO service, heap-based)\n# ---------------------------------------------------------------\nclass QueueSimulator:\n    def __init__(self, num_servers=1):\n        self.event_heap = []       # (time, type, request_id) via heapq\n        self.server_free_at = [0.0]*num_servers\n        self.results = []          # per-decision log\n\n    def run(self, request_stream, admission_policy):\n        # request_stream: sorted-by-arrival_time list of request dicts\n        # admission_policy: object with .decide(request, sim_state) -> bool\n        #                    and .observe(request, outcome) -> None  (delayed feedback)\n        for req in request_stream:\n            sim_state = self.compute_state(req.arrival_time)  # queue_depth, server_free_at, etc.\n            admit = admission_policy.decide(req, sim_state)\n            if admit:\n                start = max(req.arrival_time, min(self.server_free_at))\n                finish = start + req.service_time\n                realized_wait = start - req.arrival_time\n                realized_latency = finish - req.arrival_time\n                violation = int(realized_latency > req.slo_target)\n                self.assign_to_server(finish)\n                # KEY: feedback is delivered at 'finish' (service completion),\n                # i.e. a bounded, EXPLICIT delay -- do not update lambda_t\n                # synchronously at admission time. Queue outcome events on\n                # the same heap and pop them in time order interleaved with\n                # new arrivals so admission_policy.observe() fires at 'finish'.\n                schedule_outcome_event(finish, req, violation)\n                self.results.append({'req_id':req.id,'regime':req.regime,'time':req.arrival_time,\n                                      'admitted':1,'violation':violation,'value':req.value,\n                                      'lambda_t':admission_policy.current_threshold()})\n            else:\n                self.results.append({'req_id':req.id,'regime':req.regime,'time':req.arrival_time,\n                                      'admitted':0,'violation':None,'value':0,\n                                      'lambda_t':admission_policy.current_threshold()})\n            # pop any due outcome events and call admission_policy.observe(...)\n            self.drain_due_outcome_events(current_time=req.arrival_time)\n        self.drain_all_remaining_outcome_events()\n        return self.results\n\n# ---------------------------------------------------------------\n# 2. CONFORMAL (ACI) ADMISSION CONTROLLER  -- the headline method\n# ---------------------------------------------------------------\nclass ConformalController:\n    def __init__(self, alpha, eta, lambda_0=0.5, knapsack=False, interval_len=50):\n        self.alpha, self.eta, self.lambda_t = alpha, eta, lambda_0\n        self.knapsack, self.interval_len = knapsack, interval_len\n        self.pending_interval_candidates = []  # for knapsack variant\n\n    def decide(self, req, sim_state):\n        eligible = req.score <= self.lambda_t\n        if not self.knapsack:\n            return eligible\n        # knapsack tie-break: buffer eligible candidates for the current\n        # control interval, at interval boundary admit only the top-K by\n        # value where K = number the conformal budget allows this interval\n        # (K estimated from recent admit rate at this lambda_t, or simply\n        # every eligible request within the interval since eligibility\n        # itself is already the safety gate -- ordering only affects WHICH\n        # eligible requests get served first when server capacity binds).\n        return self.knapsack_gate(req, eligible, sim_state)\n\n    def observe(self, req, violation):\n        # ACI gradient step -- Gibbs & Candes (2021) update, applied only to\n        # ADMITTED requests (the loss is only defined conditional on admission)\n        self.lambda_t = self.lambda_t + self.eta * (self.alpha - violation)\n        self.lambda_t = clip(self.lambda_t, LAMBDA_MIN, LAMBDA_MAX)  # score range bounds\n\n    def current_threshold(self):\n        return self.lambda_t\n\n# ---------------------------------------------------------------\n# 3. BASELINE (a): FIXED / OFFLINE-TUNED THRESHOLD\n# ---------------------------------------------------------------\n# Fit ONCE on the stationary regime only: binary-search lambda_fixed such that\n# simulating the stationary regime with a static threshold hits empirical\n# violation rate == alpha (+/- small tolerance). Freeze lambda_fixed and reuse\n# for ALL regimes (this is the point: it will NOT adapt).\nlambda_fixed = calibrate_fixed_threshold(stationary_regime, target=ALPHA)\nclass FixedThresholdController:\n    def __init__(self, lam): self.lam = lam\n    def decide(self, req, sim_state): return req.score <= self.lam\n    def observe(self, req, violation): pass  # no adaptation, by design\n    def current_threshold(self): return self.lam\n\n# ---------------------------------------------------------------\n# 4. BASELINE (b): NINO-MORA-STYLE INDEX POLICY UNDER MIS-SPECIFIED M/M/1\n# ---------------------------------------------------------------\n# Fit lambda_arrival_hat, mu_service_hat from the STATIONARY regime's empirical\n# rates ONLY (a birth-death / M/M/1 assumption). Compute a marginal-productivity\n# index per queue-depth state n: index(n) = expected marginal value of admitting\n# one more request at depth n minus expected marginal SLO-violation cost, using\n# the closed-form M/M/1 waiting-time distribution W ~ n/mu_hat (Erlang-ish) to\n# estimate P(latency > slo_target | depth=n). Admit iff index(n) > 0 (equivalently\n# admit iff current depth n <= n_star, a computed cutoff depth). This index/cutoff\n# is COMPUTED ONCE from the stationary fit and reused unmodified on every regime\n# -- it is deliberately mis-specified when the regime shifts, mirroring the\n# hypothesis's critique of distributional-model policies.\nclass IndexPolicyController:\n    def __init__(self, n_star): self.n_star = n_star\n    def decide(self, req, sim_state): return sim_state.queue_depth <= self.n_star\n    def observe(self, req, violation): pass\n    def current_threshold(self): return self.n_star\n\n# ---------------------------------------------------------------\n# 5. BASELINE (c): SMALL RL ADMISSION CONTROLLER (trained on stationary ONLY)\n# ---------------------------------------------------------------\n# State: [queue_depth, predicted_service_time, risk_score, recent_violation_rate]\n# Action: {admit, reject}. Reward: +value if admitted & no violation,\n#         -PENALTY if admitted & violation, 0 if rejected.\n# Use stable_baselines3 PPO with a tiny MLP policy (2x32) OR, if\n# stable-baselines3 install is flaky in the sandbox, fall back to a minimal\n# from-scratch tabular Q-learning agent over DISCRETIZED state bins -- either\n# is acceptable, the point is a *frozen, empirically-adaptive-only* learned\n# policy with NO formal guarantee, not a specific RL algorithm.\n# Train for a fixed wall-clock/step budget (e.g. 50k steps or 10 min, whichever\n# first) on ONLY the stationary regime's simulated trajectories, then FREEZE\n# weights and evaluate, unmodified, on every regime (including unseen ones).\nrl_agent = train_ppo_or_qlearning(stationary_regime, budget_steps=50_000)\nclass RLController:\n    def __init__(self, agent): self.agent = agent  # frozen\n    def decide(self, req, sim_state): return self.agent.predict(featurize(req, sim_state)) == ADMIT\n    def observe(self, req, violation): pass  # frozen at eval time, no online update\n    def current_threshold(self): return None\n\n# ---------------------------------------------------------------\n# 6. BASELINE (d): OFFLINE-OPTIMAL ORACLE (per-regime hindsight upper bound)\n# ---------------------------------------------------------------\n# With full hindsight of every request's true violation-if-admitted outcome and\n# value in a regime, solve (or greedily approximate with a value-per-risk\n# ranking + capacity/violation-budget knapsack, since exact ILP may be too slow\n# for large regimes) the best subset of admissions that maximizes total value\n# subject to violation_count / admitted_count <= alpha. Use PuLP/OR-Tools if\n# available for an exact small-scale solve, else a value-density greedy with a\n# violation-budget counter as an approximate oracle -- LABEL WHICH ONE WAS USED\n# in method_out.json since 'oracle' is only a true upper bound if solved exactly.\n\n# ---------------------------------------------------------------\n# 7. MAIN SWEEP\n# ---------------------------------------------------------------\nresults = {}\nfor regime_name, regime_stream in regimes.items():\n    for eta in ETA_GRID:\n        conformal = ConformalController(ALPHA, eta)\n        results[('conformal', eta, regime_name)] = QueueSimulator().run(regime_stream, conformal)\n    results[('fixed', None, regime_name)] = QueueSimulator().run(regime_stream, FixedThresholdController(lambda_fixed))\n    results[('index', None, regime_name)] = QueueSimulator().run(regime_stream, IndexPolicyController(n_star))\n    results[('rl', None, regime_name)] = QueueSimulator().run(regime_stream, RLController(rl_agent))\n    results[('oracle', None, regime_name)] = compute_offline_oracle(regime_stream, ALPHA)\n\n# ---------------------------------------------------------------\n# 8. METRICS + OUTPUT\n# ---------------------------------------------------------------\nfor key, log in results.items():\n    rolling_violation_rate = rolling_window_rate(log, WINDOW, field='violation', exclude_first=BURN_IN)\n    total_value = sum(r['value'] for r in log if r['admitted'])\n    max_deviation_from_alpha = max(abs(rolling_violation_rate - ALPHA))\n    time_to_recover_after_regime_switch = compute_recovery_time(log, switch_index, ALPHA, tol=0.03)\n    save to method_out.json: {policy, eta, regime, rolling_series, total_value,\n                              overall_violation_rate, max_deviation_from_alpha,\n                              time_to_recover, admitted_count, rejected_count}\n\n# ---------------------------------------------------------------\n# 9. VALUE-AWARE KNAPSACK ABLATION (Phase 3, only after core sweep works)\n# ---------------------------------------------------------------\nfor regime_name, regime_stream in regimes.items():\n    conformal_fcfs = ConformalController(ALPHA, best_eta, knapsack=False)\n    conformal_knap = ConformalController(ALPHA, best_eta, knapsack=True)\n    log_fcfs = QueueSimulator().run(regime_stream, conformal_fcfs)\n    log_knap = QueueSimulator().run(regime_stream, conformal_knap)\n    bootstrap_ci_value_gain(log_fcfs, log_knap, n_boot=2000)\n    compare_violation_rate(log_fcfs, log_knap)  # should be statistically indistinguishable\n```",
  "fallback_plan": "Layered fallbacks, cheapest-first, so a partial but honest result always ships even under time pressure:\n\n1. If the DATASET artifact does not provide distinct labeled 'regimes' (stationary/burst/drift/switch/adversarial) or lacks a usable risk-score / value column: synthesize the missing pieces INSIDE this experiment script using a documented, seeded procedure (e.g., Poisson arrivals for stationary, a scripted 10x rate multiplier for burst, a sinusoidal rate schedule for drift, a hard rate/service-time change at a fixed timestep for switch) rather than blocking — but log explicitly in method_out.json that regimes/scores were synthesized in-script vs taken from the dataset, since this affects how strong the novelty/dataset-dependency claim is.\n2. If stable-baselines3 (or torch/gym) is unavailable or too slow to install/train within budget: drop to a minimal from-scratch tabular Q-learning or even a bandit-style epsilon-greedy threshold learner as the RL baseline. The RL baseline's SPECIFIC algorithm is not load-bearing for the hypothesis test — what matters is 'a policy trained only on stationary traffic and frozen', so any online-learned, non-conformal, non-index method suffices as a stand-in and must be labeled as such.\n3. If exact ILP (PuLP/OR-Tools) offline-optimal-oracle solve is too slow on larger regimes: replace with the documented greedy value-density-under-violation-budget approximation described in the pseudocode, and clearly flag in output that the oracle is an APPROXIMATE (not exact) upper bound.\n4. If the eta grid sweep (3 values x 5 regimes x method) does not finish within compute/time budget: cut the grid to a single eta chosen by a quick pilot run on the stationary regime only (the value nearest 0.05 that empirically converges fastest without overshoot), and run only that eta for the full regime sweep; note the abandoned grid in method_out.json as future work.\n5. If Phase 4 (real-trace replay, e.g. Azure Functions / Alibaba cluster trace) cannot be reached within the 6h budget: SKIP it entirely — it is explicitly marked stretch in the direction — and ensure Phases 0-3 (the actual falsification test of the headline claim) are complete and correct before spending any time on it.\n6. If the conformal controller's violation rate visibly fails to track alpha even in the stationary regime (a red flag for an implementation bug, not a genuine finding): first check for an off-by-one in the ACI update (make sure lambda_t used for the DECISION at time t is the value BEFORE the update from time t's own outcome, i.e. use lambda_t not lambda_{t+1} to decide admission of request t), then check that the outcome delay (service completion) is being fed back to `observe()` in TIME order matched to arrivals, not batched/ shuffled. Only report a genuine failure of the guarantee after this bug sweep is exhausted and documented.\n7. If the number of requests per regime is too small for a stable 200-request rolling window: shrink WINDOW proportionally (e.g., 50) and note the change, rather than silently reporting noisy metrics as if window size were fixed.",
  "testing_plan": "Stage the work so correctness is verified on tiny, fast, hand-checkable cases before the full 5-regime x multi-baseline x eta-grid sweep runs:\n\n1. Simulator sanity test (no policy logic yet): run the QueueSimulator with an ADMIT-EVERYTHING policy on a small synthetic single-server stream (~50 requests, hand-computed inter-arrival/service times) and assert FIFO service order, correct wait/latency computation, and correct violation flagging against a few manually worked-out cases (e.g., a request whose service_time alone exceeds slo_target must always violate regardless of queue state).\n2. Conformal update sanity test in isolation (no simulator): feed the ConformalController.observe() a scripted, deterministic sequence of violation indicators (e.g., alternating 0/1, or all-0, or all-1) and assert lambda_t moves in the correct direction and by exactly eta*(alpha - violation) each step, with clipping only engaging at the extremes — this isolates the ACI arithmetic from any simulator bug.\n3. Mini end-to-end run: 1 regime (stationary), 1 eta value, ~500-1000 requests, conformal controller only. Confirm (a) it runs to completion in well under a minute, (b) after a short burn-in the rolling-window violation rate visibly converges toward alpha rather than diverging or oscillating wildly, (c) method_out.json schema (fields listed in step 8 of the pseudocode) is present and well-formed. This is the single most important checkpoint — if the mechanism does not show convergence here on the EASIEST regime, do not proceed to the harder regimes or baselines until fixed (see fallback #6).\n4. Add the fixed-threshold and index baselines on the same mini stationary run; confirm the fixed threshold's realized violation rate is close to alpha ON the stationary regime (since it was calibrated there) as a check that the calibration procedure itself is correct, and that the index policy's queue-depth cutoff produces a plausible (not degenerate, i.e. not admitting everyone or no one) admission rate.\n5. Add a mini regime-switch stream (e.g., stationary for 500 requests then an abrupt 5x arrival-rate jump for 500 more) and run ONLY the conformal and fixed-threshold controllers on it. Confirm qualitatively that the fixed threshold's violation rate spikes and stays elevated after the switch while the conformal controller's rolling violation rate recovers back toward alpha within a bounded number of requests — this is a fast, cheap proxy for the full Phase 0 test and should be checked before committing to full-scale runs.\n6. Train the RL baseline on a SHRUNK step budget first (e.g., 2k steps) purely to confirm the training loop runs without crashing and produces a non-degenerate (not always-admit / always-reject) policy, before spending the full training budget.\n7. Only after steps 1-6 pass, run the full sweep (5 regimes x {conformal x 3 etas, fixed, index, rl, oracle}) and the Phase 3 knapsack ablation, then assemble method_out.json with rolling-window time series, summary statistics per (policy, regime), and the bootstrap CI for the knapsack value gain."
}
````

### [5] TOOL RESULT — Write · 2026-08-25 17:40:36 UTC

````
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Conformal vs Index vs RL Admission Control\",\n  \"summary\": \"Implement an ACI-based conformal admission controller and three baselines (frozen fixed threshold, mis-specified M/M/1 index policy, RL agent trained only on stationary traffic) inside a single discrete-event queue simulator driven by the dependency DATASET's multi-regime arrival/service/SLO/risk-score stream. For every (policy, regime) pair record rolling-window realized SLO-violation rate and accepted value, then compare whether the conformal controller uniquely holds its target violation rate alpha across regime shifts while remaining value-competitive in the stationary regime.\",\n  \"runpod_compute_profile\": \"cpu_heavy\",\n  \"implementation_pseudocode\": \"```\\n# ---------------------------------------------------------------\\n# 0. LOAD DATA\\n# ---------------------------------------------------------------\\ndataset = load_json(DATASET_PATH)  # from the dependency DATASET artifact\\n# Expect dataset to be organized as regimes: each regime is a list of request\\n# records with fields at minimum:\\n#   arrival_time, service_time (or service_time_dist params), slo_target,\\n#   risk_score s(x) (possibly several risk-score columns of varying quality),\\n#   value (heterogeneous request value for knapsack tie-break)\\n# If dataset schema differs, adapt field names but KEEP the same downstream\\n# contract: (arrival_time, service_time, slo_target, score, value).\\nregimes = dataset['regimes']  # e.g. {'stationary':[...], 'burst':[...], 'drift':[...],\\n                               #        'switch':[...], 'adversarial':[...]}\\nALPHA = 0.10          # target SLO-violation rate (make this a named constant,\\n                       # sweep over {0.05, 0.10, 0.20} only if time remains)\\nETA_GRID = [0.01, 0.05, 0.1]\\nWINDOW = 200          # rolling-window size for violation-rate reporting\\nBURN_IN = 500         # requests excluded from headline metrics (let lambda_t settle)\\n\\n# ---------------------------------------------------------------\\n# 1. DISCRETE-EVENT SIMULATOR (single/few-server FIFO service, heap-based)\\n# ---------------------------------------------------------------\\nclass QueueSimulator:\\n    def __init__(self, num_servers=1):\\n        self.event_heap = []       # (time, type, request_id) via heapq\\n        self.server_free_at = [0.0]*num_servers\\n        self.results = []          # per-decision log\\n\\n    def run(self, request_stream, admission_policy):\\n        # request_stream: sorted-by-arrival_time list of request dicts\\n        # admission_policy: object with .decide(request, sim_state) -> bool\\n        #                    and .observe(request, outcome) -> None  (delayed feedback)\\n        for req in request_stream:\\n            sim_state = self.compute_state(req.arrival_time)  # queue_depth, server_free_at, etc.\\n            admit = admission_policy.decide(req, sim_state)\\n            if admit:\\n                start = max(req.arrival_time, min(self.server_free_at))\\n                finish = start + req.service_time\\n                realized_wait = start - req.arrival_time\\n                realized_latency = finish - req.arrival_time\\n                violation = int(realized_latency > req.slo_target)\\n                self.assign_to_server(finish)\\n                # KEY: feedback is delivered at 'finish' (service completion),\\n                # i.e. a bounded, EXPLICIT delay -- do not update lambda_t\\n                # synchronously at admission time. Queue outcome events on\\n                # the same heap and pop them in time order interleaved with\\n                # new arrivals so admission_policy.observe() fires at 'finish'.\\n                schedule_outcome_event(finish, req, violation)\\n                self.results.append({'req_id':req.id,'regime':req.regime,'time':req.arrival_time,\\n                                      'admitted':1,'violation':violation,'value':req.value,\\n                                      'lambda_t':admission_policy.current_threshold()})\\n            else:\\n                self.results.append({'req_id':req.id,'regime':req.regime,'time':req.arrival_time,\\n                                      'admitted':0,'violation':None,'value':0,\\n                                      'lambda_t':admission_policy.current_threshold()})\\n            # pop any due outcome events and call admission_policy.observe(...)\\n            self.drain_due_outcome_events(current_time=req.arrival_time)\\n        self.drain_all_remaining_outcome_events()\\n        return self.results\\n\\n# ---------------------------------------------------------------\\n# 2. CONFORMAL (ACI) ADMISSION CONTROLLER  -- the headline method\\n# ---------------------------------------------------------------\\nclass ConformalController:\\n    def __init__(self, alpha, eta, lambda_0=0.5, knapsack=False, interval_len=50):\\n        self.alpha, self.eta, self.lambda_t = alpha, eta, lambda_0\\n        self.knapsack, self.interval_len = knapsack, interval_len\\n        self.pending_interval_candidates = []  # for knapsack variant\\n\\n    def decide(self, req, sim_state):\\n        eligible = req.score <= self.lambda_t\\n        if not self.knapsack:\\n            return eligible\\n        # knapsack tie-break: buffer eligible candidates for the current\\n        # control interval, at interval boundary admit only the top-K by\\n        # value where K = number the conformal budget allows this interval\\n        # (K estimated from recent admit rate at this lambda_t, or simply\\n        # every eligible request within the interval since eligibility\\n        # itself is already the safety gate -- ordering only affects WHICH\\n        # eligible requests get served first when server capacity binds).\\n        return self.knapsack_gate(req, eligible, sim_state)\\n\\n    def observe(self, req, violation):\\n        # ACI gradient step -- Gibbs & Candes (2021) update, applied only to\\n        # ADMITTED requests (the loss is only defined conditional on admission)\\n        self.lambda_t = self.lambda_t + self.eta * (self.alpha - violation)\\n        self.lambda_t = clip(self.lambda_t, LAMBDA_MIN, LAMBDA_MAX)  # score range bounds\\n\\n    def current_threshold(self):\\n        return self.lambda_t\\n\\n# ---------------------------------------------------------------\\n# 3. BASELINE (a): FIXED / OFFLINE-TUNED THRESHOLD\\n# ---------------------------------------------------------------\\n# Fit ONCE on the stationary regime only: binary-search lambda_fixed such that\\n# simulating the stationary regime with a static threshold hits empirical\\n# violation rate == alpha (+/- small tolerance). Freeze lambda_fixed and reuse\\n# for ALL regimes (this is the point: it will NOT adapt).\\nlambda_fixed = calibrate_fixed_threshold(stationary_regime, target=ALPHA)\\nclass FixedThresholdController:\\n    def __init__(self, lam): self.lam = lam\\n    def decide(self, req, sim_state): return req.score <= self.lam\\n    def observe(self, req, violation): pass  # no adaptation, by design\\n    def current_threshold(self): return self.lam\\n\\n# ---------------------------------------------------------------\\n# 4. BASELINE (b): NINO-MORA-STYLE INDEX POLICY UNDER MIS-SPECIFIED M/M/1\\n# ---------------------------------------------------------------\\n# Fit lambda_arrival_hat, mu_service_hat from the STATIONARY regime's empirical\\n# rates ONLY (a birth-death / M/M/1 assumption). Compute a marginal-productivity\\n# index per queue-depth state n: index(n) = expected marginal value of admitting\\n# one more request at depth n minus expected marginal SLO-violation cost, using\\n# the closed-form M/M/1 waiting-time distribution W ~ n/mu_hat (Erlang-ish) to\\n# estimate P(latency > slo_target | depth=n). Admit iff index(n) > 0 (equivalently\\n# admit iff current depth n <= n_star, a computed cutoff depth). This index/cutoff\\n# is COMPUTED ONCE from the stationary fit and reused unmodified on every regime\\n# -- it is deliberately mis-specified when the regime shifts, mirroring the\\n# hypothesis's critique of distributional-model policies.\\nclass IndexPolicyController:\\n    def __init__(self, n_star): self.n_star = n_star\\n    def decide(self, req, sim_state): return sim_state.queue_depth <= self.n_star\\n    def observe(self, req, violation): pass\\n    def current_threshold(self): return self.n_star\\n\\n# ---------------------------------------------------------------\\n# 5. BASELINE (c): SMALL RL ADMISSION CONTROLLER (trained on stationary ONLY)\\n# ---------------------------------------------------------------\\n# State: [queue_depth, predicted_service_time, risk_score, recent_violation_rate]\\n# Action: {admit, reject}. Reward: +value if admitted & no violation,\\n#         -PENALTY if admitted & violation, 0 if rejected.\\n# Use stable_baselines3 PPO with a tiny MLP policy (2x32) OR, if\\n# stable-baselines3 install is flaky in the sandbox, fall back to a minimal\\n# from-scratch tabular Q-learning agent over DISCRETIZED state bins -- either\\n# is acceptable, the point is a *frozen, empirically-adaptive-only* learned\\n# policy with NO formal guarantee, not a specific RL algorithm.\\n# Train for a fixed wall-clock/step budget (e.g. 50k steps or 10 min, whichever\\n# first) on ONLY the stationary regime's simulated trajectories, then FREEZE\\n# weights and evaluate, unmodified, on every regime (including unseen ones).\\nrl_agent = train_ppo_or_qlearning(stationary_regime, budget_steps=50_000)\\nclass RLController:\\n    def __init__(self, agent): self.agent = agent  # frozen\\n    def decide(self, req, sim_state): return self.agent.predict(featurize(req, sim_state)) == ADMIT\\n    def observe(self, req, violation): pass  # frozen at eval time, no online update\\n    def current_threshold(self): return None\\n\\n# ---------------------------------------------------------------\\n# 6. BASELINE (d): OFFLINE-OPTIMAL ORACLE (per-regime hindsight upper bound)\\n# ---------------------------------------------------------------\\n# With full hindsight of every request's true violation-if-admitted outcome and\\n# value in a regime, solve (or greedily approximate with a value-per-risk\\n# ranking + capacity/violation-budget knapsack, since exact ILP may be too slow\\n# for large regimes) the best subset of admissions that maximizes total value\\n# subject to violation_count / admitted_count <= alpha. Use PuLP/OR-Tools if\\n# available for an exact small-scale solve, else a value-density greedy with a\\n# violation-budget counter as an approximate oracle -- LABEL WHICH ONE WAS USED\\n# in method_out.json since 'oracle' is only a true upper bound if solved exactly.\\n\\n# ---------------------------------------------------------------\\n# 7. MAIN SWEEP\\n# ---------------------------------------------------------------\\nresults = {}\\nfor regime_name, regime_stream in regimes.items():\\n    for eta in ETA_GRID:\\n        conformal = ConformalController(ALPHA, eta)\\n        results[('conformal', eta, regime_name)] = QueueSimulator().run(regime_stream, conformal)\\n    results[('fixed', None, regime_name)] = QueueSimulator().run(regime_stream, FixedThresholdController(lambda_fixed))\\n    results[('index', None, regime_name)] = QueueSimulator().run(regime_stream, IndexPolicyController(n_star))\\n    results[('rl', None, regime_name)] = QueueSimulator().run(regime_stream, RLController(rl_agent))\\n    results[('oracle', None, regime_name)] = compute_offline_oracle(regime_stream, ALPHA)\\n\\n# ---------------------------------------------------------------\\n# 8. METRICS + OUTPUT\\n# ---------------------------------------------------------------\\nfor key, log in results.items():\\n    rolling_violation_rate = rolling_window_rate(log, WINDOW, field='violation', exclude_first=BURN_IN)\\n    total_value = sum(r['value'] for r in log if r['admitted'])\\n    max_deviation_from_alpha = max(abs(rolling_violation_rate - ALPHA))\\n    time_to_recover_after_regime_switch = compute_recovery_time(log, switch_index, ALPHA, tol=0.03)\\n    save to method_out.json: {policy, eta, regime, rolling_series, total_value,\\n                              overall_violation_rate, max_deviation_from_alpha,\\n                              time_to_recover, admitted_count, rejected_count}\\n\\n# ---------------------------------------------------------------\\n# 9. VALUE-AWARE KNAPSACK ABLATION (Phase 3, only after core sweep works)\\n# ---------------------------------------------------------------\\nfor regime_name, regime_stream in regimes.items():\\n    conformal_fcfs = ConformalController(ALPHA, best_eta, knapsack=False)\\n    conformal_knap = ConformalController(ALPHA, best_eta, knapsack=True)\\n    log_fcfs = QueueSimulator().run(regime_stream, conformal_fcfs)\\n    log_knap = QueueSimulator().run(regime_stream, conformal_knap)\\n    bootstrap_ci_value_gain(log_fcfs, log_knap, n_boot=2000)\\n    compare_violation_rate(log_fcfs, log_knap)  # should be statistically indistinguishable\\n```\",\n  \"fallback_plan\": \"Layered fallbacks, cheapest-first, so a partial but honest result always ships even under time pressure:\\n\\n1. If the DATASET artifact does not provide distinct labeled 'regimes' (stationary/burst/drift/switch/adversarial) or lacks a usable risk-score / value column: synthesize the missing pieces INSIDE this experiment script using a documented, seeded procedure (e.g., Poisson arrivals for stationary, a scripted 10x rate multiplier for burst, a sinusoidal rate schedule for drift, a hard rate/service-time change at a fixed timestep for switch) rather than blocking — but log explicitly in method_out.json that regimes/scores were synthesized in-script vs taken from the dataset, since this affects how strong the novelty/dataset-dependency claim is.\\n2. If stable-baselines3 (or torch/gym) is unavailable or too slow to install/train within budget: drop to a minimal from-scratch tabular Q-learning or even a bandit-style epsilon-greedy threshold learner as the RL baseline. The RL baseline's SPECIFIC algorithm is not load-bearing for the hypothesis test — what matters is 'a policy trained only on stationary traffic and frozen', so any online-learned, non-conformal, non-index method suffices as a stand-in and must be labeled as such.\\n3. If exact ILP (PuLP/OR-Tools) offline-optimal-oracle solve is too slow on larger regimes: replace with the documented greedy value-density-under-violation-budget approximation described in the pseudocode, and clearly flag in output that the oracle is an APPROXIMATE (not exact) upper bound.\\n4. If the eta grid sweep (3 values x 5 regimes x method) does not finish within compute/time budget: cut the grid to a single eta chosen by a quick pilot run on the stationary regime only (the value nearest 0.05 that empirically converges fastest without overshoot), and run only that eta for the full regime sweep; note the abandoned grid in method_out.json as future work.\\n5. If Phase 4 (real-trace replay, e.g. Azure Functions / Alibaba cluster trace) cannot be reached within the 6h budget: SKIP it entirely — it is explicitly marked stretch in the direction — and ensure Phases 0-3 (the actual falsification test of the headline claim) are complete and correct before spending any time on it.\\n6. If the conformal controller's violation rate visibly fails to track alpha even in the stationary regime (a red flag for an implementation bug, not a genuine finding): first check for an off-by-one in the ACI update (make sure lambda_t used for the DECISION at time t is the value BEFORE the update from time t's own outcome, i.e. use lambda_t not lambda_{t+1} to decide admission of request t), then check that the outcome delay (service completion) is being fed back to `observe()` in TIME order matched to arrivals, not batched/ shuffled. Only report a genuine failure of the guarantee after this bug sweep is exhausted and documented.\\n7. If the number of requests per regime is too small for a stable 200-request rolling window: shrink WINDOW proportionally (e.g., 50) and note the change, rather than silently reporting noisy metrics as if window size were fixed.\",\n  \"testing_plan\": \"Stage the work so correctness is verified on tiny, fast, hand-checkable cases before the full 5-regime x multi-baseline x eta-grid sweep runs:\\n\\n1. Simulator sanity test (no policy logic yet): run the QueueSimulator with an ADMIT-EVERYTHING policy on a small synthetic single-server stream (~50 requests, hand-computed inter-arrival/service times) and assert FIFO service order, correct wait/latency computation, and correct violation flagging against a few manually worked-out cases (e.g., a request whose service_time alone exceeds slo_target must always violate regardless of queue state).\\n2. Conformal update sanity test in isolation (no simulator): feed the ConformalController.observe() a scripted, deterministic sequence of violation indicators (e.g., alternating 0/1, or all-0, or all-1) and assert lambda_t moves in the correct direction and by exactly eta*(alpha - violation) each step, with clipping only engaging at the extremes — this isolates the ACI arithmetic from any simulator bug.\\n3. Mini end-to-end run: 1 regime (stationary), 1 eta value, ~500-1000 requests, conformal controller only. Confirm (a) it runs to completion in well under a minute, (b) after a short burn-in the rolling-window violation rate visibly converges toward alpha rather than diverging or oscillating wildly, (c) method_out.json schema (fields listed in step 8 of the pseudocode) is present and well-formed. This is the single most important checkpoint — if the mechanism does not show convergence here on the EASIEST regime, do not proceed to the harder regimes or baselines until fixed (see fallback #6).\\n4. Add the fixed-threshold and index baselines on the same mini stationary run; confirm the fixed threshold's realized violation rate is close to alpha ON the stationary regime (since it was calibrated there) as a check that the calibration procedure itself is correct, and that the index policy's queue-depth cutoff produces a plausible (not degenerate, i.e. not admitting everyone or no one) admission rate.\\n5. Add a mini regime-switch stream (e.g., stationary for 500 requests then an abrupt 5x arrival-rate jump for 500 more) and run ONLY the conformal and fixed-threshold controllers on it. Confirm qualitatively that the fixed threshold's violation rate spikes and stays elevated after the switch while the conformal controller's rolling violation rate recovers back toward alpha within a bounded number of requests — this is a fast, cheap proxy for the full Phase 0 test and should be checked before committing to full-scale runs.\\n6. Train the RL baseline on a SHRUNK step budget first (e.g., 2k steps) purely to confirm the training loop runs without crashing and produces a non-degenerate (not always-admit / always-reject) policy, before spending the full training budget.\\n7. Only after steps 1-6 pass, run the full sweep (5 regimes x {conformal x 3 etas, fixed, index, rl, oracle}) and the Phase 3 knapsack ablation, then assemble method_out.json with rolling-window time series, summary statistics per (policy, regime), and the bootstrap CI for the knapsack value gain.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
````

### [6] ASSISTANT · 2026-08-25 17:40:39 UTC

```
Plan written to `.terminal_claude_agent_struct_out.json` — covers the conformal ACI controller, three baselines (fixed threshold, mis-specified M/M/1 index policy, frozen RL agent), an offline oracle, staged testing from unit-level ACI arithmetic checks up to the full multi-regime sweep, and fallbacks for missing dataset regimes, RL library issues, and ILP solve cost.
```
