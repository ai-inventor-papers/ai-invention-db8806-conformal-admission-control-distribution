# gen_plan_dataset_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_plan`
> Run: `iter1_88afd6206a08` — Conformal Admission Control for Overloaded Request Queues
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_dataset_1` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-08-25 17:39:14 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/gen_plan/gen_plan_dataset_1
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
You are expanding an artifact direction of type: DATASET

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect
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

The dataset executor has 6h total (including writing code, debugging, testing, and fixing errors).

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

id: dataset_iter1_dir1
type: dataset
objective: >-
  Produce a realistic substrate of inter-arrival times, service times, and per-request latency-SLO targets that spans a stationary
  regime and several distribution-shift regimes (sudden burst, slow drift, unannounced regime switch, adversarial worst-case),
  derived from a REAL public request/invocation trace rather than a hand-tuned synthetic distribution.
approach: >-
  Acquire a public serverless/cluster invocation trace with genuine burstiness and non-stationarity (e.g., the Azure Functions
  2019/2021 invocation-per-minute traces on HuggingFace/Azure's public repo, or the Alibaba cluster trace) via aii-hf-datasets
  or direct URL download; extract per-minute invocation counts for a sample of functions to derive realistic non-stationary
  arrival-rate curves, and fit/resample service-time distributions from the trace's execution-duration fields where available
  (fall back to a documented log-normal service-time model calibrated to the trace's duration percentiles where duration data
  is coarse). Construct 5 labeled regimes from this real substrate: (1) a stationary window, (2) a real burst window (10x+
  spike present in the trace), (3) a slow-drift window (gradual load ramp), (4) a regime-switch window (concatenation of two
  different functions' traffic with no transition smoothing), (5) a synthetic adversarial worst-case sequence explicitly constructed
  post-hoc to probe the threshold tracker's failure modes (the only regime allowed to be synthetic, since no real trace is
  adversarial by construction). Assign each request an SLO target (e.g., a fixed multiple of the median service time, or a
  per-function percentile from the trace) and a cheap, deliberately imperfect risk score s(x) as a documented function of
  queue depth and predicted service time at arrival. Output standardized JSON rows of {arrival_time, service_time, slo_target,
  risk_score, regime_label, metadata_fold}.
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

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead
</artifact_executor_scope>

<artifact_planning_rules>
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for dataset artifacts:
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
  "description": "Plan for a DATASET artifact.",
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
    "ideal_dataset_criteria": {
      "description": "What makes an ideal dataset for this purpose - size, format, content requirements",
      "title": "Ideal Dataset Criteria",
      "type": "string"
    },
    "dataset_search_plan": {
      "description": "Step-by-step plan for finding/creating this dataset - sources to check, fallback options",
      "title": "Dataset Search Plan",
      "type": "string"
    },
    "target_num_datasets": {
      "description": "How many individual datasets should be delivered. Count each dataset separately, not collections \u2014 a benchmark suite of N datasets counts as N. This controls how broadly the executor searches, so setting it too low will under-collect.",
      "title": "Target Num Datasets",
      "type": "integer"
    }
  },
  "required": [
    "title",
    "ideal_dataset_criteria",
    "dataset_search_plan",
    "target_num_datasets"
  ],
  "title": "DatasetPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-25 17:39:22 UTC

```
Find a better admission control policy for overloaded request queues.
```

### [4] TOOL CALL — ToolSearch · 2026-08-25 17:39:24 UTC

```
{'query': 'select:WebSearch', 'max_results': 3}
```

### [5] TOOL RESULT — ToolSearch · 2026-08-25 17:39:24 UTC

```
{"matches": ["WebSearch"], "query": "select:WebSearch", "total_deferred_tools": 18}
```

### [6] TOOL CALL — WebSearch · 2026-08-25 17:39:26 UTC

```
Azure Functions invocation trace 2021 huggingface dataset per-minute
```

### [7] TOOL CALL — WebSearch · 2026-08-25 17:39:26 UTC

```
Alibaba cluster trace 2018 GitHub duration percentiles microservice call graph
```

### [8] TOOL RESULT — WebSearch · 2026-08-25 17:39:30 UTC

```
{"query": "Azure Functions invocation trace 2021 huggingface dataset per-minute", "results": [{"tool_use_id": "srvtoolu_01U2BL8v1YVbGSZhZ2A977xy", "content": [{"title": "Azure Functions Invocation Trace 2021", "url": "https://github.com/Azure/AzurePublicDataset/blob/master/AzureFunctionsInvocationTrace2021.md"}, {"title": "TraceData-MicroSoft-AzurePublicDataset/README.md at master · Stone-ResearchLife/TraceData-MicroSoft-AzurePublicDataset", "url": "https://github.com/Stone-ResearchLife/TraceData-MicroSoft-AzurePublicDataset/blob/master/README.md"}, {"title": "Azure Functions Blob Access Trace 2020", "url": "https://github.com/Azure/AzurePublicDataset/blob/master/AzureFunctionsBlobDataset2020.md"}, {"title": "AzureFunctionsDataset2019 Trace Analysis", "url": "https://github.com/Azure/AzurePublicDataset/blob/master/analysis/AzureFunctionsDataset2019-Trace_Analysis.md"}, {"title": "github.com", "url": "https://github.com/Azure/AzurePublicDataset"}]}, "Based on the search results, I found information about the Azure Functions Invocation Trace 2021 dataset:\n\nThe AzureFunctionsInvocationTrace2021 is a trace of function invocations for two weeks starting on 2021-01-31. The trace contains invocation arrival and departure (or completion) times, with schema including app (application id), func (function id), end_timestamp (in millisecond), and duration (in millisecond).\n\nHowever, I should note that this dataset is hosted on the Azure Public Dataset GitHub repository (not Hugging Face). The search results mention that you can download the dataset here: AzureFunctionsInvocationTraceForTwoWeeksJan2021.rar and that if you do use the Azure Functions 2021 trace in your research, please cite the SOSP'21 paper \"Faster and Cheaper Serverless Computing on Harvested Resources\".\n\nThe per-minute invocation data appears to be associated with the 2019 dataset rather than the 2021 dataset, where the 2019 dataset includes how many times per minute each (anonymized) function is invoked and its corresponding trigger group."], "durationSeconds": 5.36157248, "searchCount": 1}
```

### [9] TOOL RESULT — WebSearch · 2026-08-25 17:39:34 UTC

```
{"query": "Alibaba cluster trace 2018 GitHub duration percentiles microservice call graph", "results": [{"tool_use_id": "srvtoolu_016BcG6uzoc25vvothgCjb5h", "content": [{"title": "GitHub - aFang-share/clusterdata-alibaba: cluster data collected from production clusters in Alibaba for cluster management research · GitHub", "url": "https://github.com/aFang-share/clusterdata-alibaba"}, {"title": "GitHub - alibaba/clusterdata: cluster data collected from production clusters in Alibaba for cluster management research · GitHub", "url": "https://github.com/alibaba/clusterdata"}, {"title": "Alibaba Cluster Trace Program", "url": "https://github.com/SiNa88/clusterdata-prediction"}, {"title": "clusterdata/cluster-trace-microservices-v2021/README.md at master · alibaba/clusterdata", "url": "https://github.com/alibaba/clusterdata/blob/master/cluster-trace-microservices-v2021/README.md"}, {"title": "clusterdata/cluster-trace-microservices-v2022 at master · alibaba/clusterdata", "url": "https://github.com/alibaba/clusterdata/tree/master/cluster-trace-microservices-v2022"}, {"title": "clusterdata/README.md at master · alibaba/clusterdata", "url": "https://github.com/alibaba/clusterdata/blob/master/README.md"}, {"title": "Distributed Traces of Microservices Architecture: Publicly Available Datasets", "url": "https://www.abhishek-tiwari.com/distributed-traces-of-microservices-architecture-publicly-available-datasets/"}, {"title": "Characterizing Microservice Dependency and Performance: Alibaba Trace Analysis", "url": "http://hliangzhao.me/materials/alibaba_trace.pdf"}, {"title": "research.spec.org", "url": "https://research.spec.org/icpe_proceedings/2024/proceedings/p276.pdf"}, {"title": "Published November 29, 2024 | Version v3", "url": "https://zenodo.org/records/14245634"}]}, "Based on the search results, here's what I found about the Alibaba cluster trace datasets on GitHub:\n\n## Overview\n\nThe cluster-trace-v2018 includes about 4000 machines in a period of 8 days and contains DAG information of production batch workloads.\n\n## Microservices Traces (2021 and 2022)\n\nThe microservices traces introduced runtime metrics of microservices in the production cluster, including call dependencies, respond time, call rates, and so on.\n\nMore recent versions include:\n\n- **2021 Release**: The released traces contain detailed runtime metrics of nearly twenty thousand microservices collected from Alibaba production clusters of over ten thousand bare-metal nodes during 13 days in 2022.\n\n- **2022 Release**: This updated trace offers an extended duration (13 days) and includes additional information, such as the service ID within the call graph.\n\n## Call Graph Structure\n\nA call graph contains multiple calls between different pairs of microservices, where a pair of microservices contain one upstream microservice (UM) and one downstream microservice (DM).\n\n## Accessibility\n\nThe official repositories are available on GitHub at:\n- https://github.com/alibaba/clusterdata (official Alibaba repository)\n- Supporting documentation and READMEs available in subdirectories for each trace version\n\nBoth published trace data are sampled at 0.5% rate and includes 20M+ traces."], "durationSeconds": 8.227309072999999, "searchCount": 1}
```

### [10] ASSISTANT · 2026-08-25 17:40:06 UTC

```
Enough to plan concretely. Writing the plan output now.
```

### [11] TOOL CALL — Write · 2026-08-25 17:40:06 UTC

```
File: /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/gen_plan/gen_plan_dataset_1/.terminal_claude_agent_struct_out.json

{
  "title": "Real Traffic Traces for Admission Control",
  "summary": "Build a standardized JSON dataset of arrival times, service times, and per-request SLO targets covering 5 regimes (stationary, real burst, slow drift, unannounced regime-switch, adversarial worst-case), derived primarily from the Azure Functions 2019/2021 invocation-per-minute trace and cross-checked against the Alibaba microservices call-graph trace, with risk scores and regime/fold labels attached for a conformal admission-control policy to consume.",
  "runpod_compute_profile": "cpu_heavy",
  "ideal_dataset_criteria": "A single standardized JSON dataset (data_out.json) of request-level rows with schema {arrival_time (float, seconds, monotonic within a regime), service_time (float, seconds, >0), slo_target (float, seconds), risk_score (float in [0,1] or unbounded real, documented), regime_label (one of ['stationary','burst','drift','regime_switch','adversarial']), function_id/source_id (string, from the real trace), metadata_fold (one of ['train','val','test'] or ['full']), request_id (int)}. Target scale: tens of thousands to a few hundred thousand rows total (enough for rolling-window violation-rate estimation with narrow CIs per regime, e.g. >=5,000 admitted-request-equivalent decisions per regime) while staying well under the 300MB limit — subsample functions/time windows from the raw trace rather than loading it whole. Must derive arrival-rate curves (inter-arrival times) and service-time distributions from REAL invocation-count and duration fields in a real public trace (Azure Functions or Alibaba microservices), not from a hand-picked synthetic distribution, for 4 of the 5 regimes; only the 'adversarial' regime may be constructed synthetically (explicitly documented as such). Each regime must be long enough (in decision count) to observe multiple ACI update cycles and at least one full rolling-window (e.g. >=2000 decisions) so downstream experiments can measure convergence to the target violation rate alpha. Service-time and SLO-target fields must be internally consistent (SLO target should be a documented function of service-time distribution, e.g. p99 of service time for that function, or median*k) so that a 'violation' is a meaningful, well-defined event. Risk score must be a documented, deliberately imperfect heuristic (not equal to the ground truth used to generate violations) computed from information available at admission time only (queue-depth proxy, predicted service time from a coarse per-function estimate, arrival rate estimate) so it is legitimately 'weakly informative but miscalibrated', matching the hypothesis's assumption 1. All regime boundaries, trace-derived vs synthetic provenance, and the exact SLO/risk-score formulas must be recorded in per-row metadata or an accompanying schema doc field so the downstream experiment executor does not have to re-derive them.",
  "dataset_search_plan": "1) PRIMARY SOURCE — Azure Functions traces (Azure/AzurePublicDataset GitHub repo, downloadable as .rar/.csv, NOT on HuggingFace despite the direction's suggestion; verify via aii-hf-datasets search first as a fallback in case a mirror exists, but plan the direct-URL path as primary): (a) AzureFunctionsDataset2019 gives per-minute invocation counts per anonymized function across a trigger group over ~2 weeks plus execution-duration percentiles (min/avg/max/percentiles per function, NOT raw per-invocation durations) — use this for AGGREGATE arrival-rate curves (the per-minute counts) and for calibrating a documented log-normal/empirical service-time model per function (fit to the reported percentiles, since raw per-call durations are not published at that granularity). (b) AzureFunctionsInvocationTrace2021 (2 weeks from 2021-01-31) gives arrival AND departure/completion timestamps with duration in ms per invocation at finer per-app/per-func granularity — prefer this for regimes needing real per-request service-time realizations, not just percentile fits, if the file size/format is tractable within the 300MB budget (download and subsample specific apps/functions with high invocation counts and visible burstiness rather than the full multi-GB archive). Download via direct URL (github release asset), not aii-hf-datasets, since these are not distributed as HF datasets.  2) SECONDARY SOURCE for cross-check / regime_switch construction — Alibaba cluster-trace-microservices-v2021 or v2022 (alibaba/clusterdata GitHub repo): call-graph traces with per-call response times (rt) and call rates across ~13 days for thousands of microservices; use two temporally/behaviorally distinct microservices' RT and call-rate series as the two halves of the 'regime_switch' regime (concatenate function A's real window then function B's real window with no smoothing), since this trace has explicit per-call latency (not just aggregate percentiles) which is more directly usable as 'service_time'. 3) CONSTRUCTION OF THE 5 REGIMES from the above two real sources: stationary = a real quiet, low-variance window from one Azure or Alibaba function/app with a small coefficient of variation in per-minute counts; burst = a real window from the same corpus where per-minute invocation count spikes >=10x over its trailing baseline (search across functions for this pattern rather than injecting it); drift = a real window with a sustained monotonic ramp in per-minute counts over the window (fit a rolling regression to identify candidate functions/windows); regime_switch = concatenation of two different real functions' windows (from Alibaba call-graph microservices, using their RT/call-rate series) with a hard cut, no transition smoothing; adversarial = the ONLY synthetic regime, hand-constructed post-hoc (e.g., alternating score-inversion bursts, adaptive-worst-case density chosen to try to desynchronize the ACI tracker) and clearly flagged in metadata as synthetic with the construction logic documented in the schema/readme. 4) FALLBACK if the 2021 Azure per-invocation trace is too large or its per-call durations are inaccessible within budget/time: fall back entirely to the 2019 per-minute counts (real arrivals) plus the documented log-normal service-time model calibrated to that trace's own percentile fields (still real-data-derived, not hand-tuned) — this keeps 4/5 regimes grounded in real arrival dynamics even if service times are a calibrated model rather than raw per-call realizations; document this fallback explicitly if triggered. 5) VALIDATION: after construction, check (a) schema conformance via aii-json, (b) each regime's actual traffic statistics (burst ratio, drift slope, switch discontinuity) match its label using simple descriptive stats computed during construction (not as a separate experiment artifact — just sanity-checking the data before shipping), (c) total file size under the 300MB cap, splitting via aii-file-size-limit if needed, and (d) produce full/mini/preview JSON variants.",
  "target_num_datasets": 1
}
```

### [12] TOOL RESULT — Write · 2026-08-25 17:40:06 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_1/gen_plan/gen_plan_dataset_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Real Traffic Traces for Admission Control\",\n  \"summary\": \"Build a standardized JSON dataset of arrival times, service times, and per-request SLO targets covering 5 regimes (stationary, real burst, slow drift, unannounced regime-switch, adversarial worst-case), derived primarily from the Azure Functions 2019/2021 invocation-per-minute trace and cross-checked against the Alibaba microservices call-graph trace, with risk scores and regime/fold labels attached for a conformal admission-control policy to consume.\",\n  \"runpod_compute_profile\": \"cpu_heavy\",\n  \"ideal_dataset_criteria\": \"A single standardized JSON dataset (data_out.json) of request-level rows with schema {arrival_time (float, seconds, monotonic within a regime), service_time (float, seconds, >0), slo_target (float, seconds), risk_score (float in [0,1] or unbounded real, documented), regime_label (one of ['stationary','burst','drift','regime_switch','adversarial']), function_id/source_id (string, from the real trace), metadata_fold (one of ['train','val','test'] or ['full']), request_id (int)}. Target scale: tens of thousands to a few hundred thousand rows total (enough for rolling-window violation-rate estimation with narrow CIs per regime, e.g. >=5,000 admitted-request-equivalent decisions per regime) while staying well under the 300MB limit — subsample functions/time windows from the raw trace rather than loading it whole. Must derive arrival-rate curves (inter-arrival times) and service-time distributions from REAL invocation-count and duration fields in a real public trace (Azure Functions or Alibaba microservices), not from a hand-picked synthetic distribution, for 4 of the 5 regimes; only the 'adversarial' regime may be constructed synthetically (explicitly documented as such). Each regime must be long enough (in decision count) to observe multiple ACI update cycles and at least one full rolling-window (e.g. >=2000 decisions) so downstream experiments can measure convergence to the target violation rate alpha. Service-time and SLO-target fields must be internally consistent (SLO target should be a documented function of service-time distribution, e.g. p99 of service time for that function, or median*k) so that a 'violation' is a meaningful, well-defined event. Risk score must be a documented, deliberately imperfect heuristic (not equal to the ground truth used to generate violations) computed from information available at admission time only (queue-depth proxy, predicted service time from a coarse per-function estimate, arrival rate estimate) so it is legitimately 'weakly informative but miscalibrated', matching the hypothesis's assumption 1. All regime boundaries, trace-derived vs synthetic provenance, and the exact SLO/risk-score formulas must be recorded in per-row metadata or an accompanying schema doc field so the downstream experiment executor does not have to re-derive them.\",\n  \"dataset_search_plan\": \"1) PRIMARY SOURCE — Azure Functions traces (Azure/AzurePublicDataset GitHub repo, downloadable as .rar/.csv, NOT on HuggingFace despite the direction's suggestion; verify via aii-hf-datasets search first as a fallback in case a mirror exists, but plan the direct-URL path as primary): (a) AzureFunctionsDataset2019 gives per-minute invocation counts per anonymized function across a trigger group over ~2 weeks plus execution-duration percentiles (min/avg/max/percentiles per function, NOT raw per-invocation durations) — use this for AGGREGATE arrival-rate curves (the per-minute counts) and for calibrating a documented log-normal/empirical service-time model per function (fit to the reported percentiles, since raw per-call durations are not published at that granularity). (b) AzureFunctionsInvocationTrace2021 (2 weeks from 2021-01-31) gives arrival AND departure/completion timestamps with duration in ms per invocation at finer per-app/per-func granularity — prefer this for regimes needing real per-request service-time realizations, not just percentile fits, if the file size/format is tractable within the 300MB budget (download and subsample specific apps/functions with high invocation counts and visible burstiness rather than the full multi-GB archive). Download via direct URL (github release asset), not aii-hf-datasets, since these are not distributed as HF datasets.  2) SECONDARY SOURCE for cross-check / regime_switch construction — Alibaba cluster-trace-microservices-v2021 or v2022 (alibaba/clusterdata GitHub repo): call-graph traces with per-call response times (rt) and call rates across ~13 days for thousands of microservices; use two temporally/behaviorally distinct microservices' RT and call-rate series as the two halves of the 'regime_switch' regime (concatenate function A's real window then function B's real window with no smoothing), since this trace has explicit per-call latency (not just aggregate percentiles) which is more directly usable as 'service_time'. 3) CONSTRUCTION OF THE 5 REGIMES from the above two real sources: stationary = a real quiet, low-variance window from one Azure or Alibaba function/app with a small coefficient of variation in per-minute counts; burst = a real window from the same corpus where per-minute invocation count spikes >=10x over its trailing baseline (search across functions for this pattern rather than injecting it); drift = a real window with a sustained monotonic ramp in per-minute counts over the window (fit a rolling regression to identify candidate functions/windows); regime_switch = concatenation of two different real functions' windows (from Alibaba call-graph microservices, using their RT/call-rate series) with a hard cut, no transition smoothing; adversarial = the ONLY synthetic regime, hand-constructed post-hoc (e.g., alternating score-inversion bursts, adaptive-worst-case density chosen to try to desynchronize the ACI tracker) and clearly flagged in metadata as synthetic with the construction logic documented in the schema/readme. 4) FALLBACK if the 2021 Azure per-invocation trace is too large or its per-call durations are inaccessible within budget/time: fall back entirely to the 2019 per-minute counts (real arrivals) plus the documented log-normal service-time model calibrated to that trace's own percentile fields (still real-data-derived, not hand-tuned) — this keeps 4/5 regimes grounded in real arrival dynamics even if service times are a calibrated model rather than raw per-call realizations; document this fallback explicitly if triggered. 5) VALIDATION: after construction, check (a) schema conformance via aii-json, (b) each regime's actual traffic statistics (burst ratio, drift slope, switch discontinuity) match its label using simple descriptive stats computed during construction (not as a separate experiment artifact — just sanity-checking the data before shipping), (c) total file size under the 300MB cap, splitting via aii-file-size-limit if needed, and (d) produce full/mini/preview JSON variants.\",\n  \"target_num_datasets\": 1\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [13] ASSISTANT · 2026-08-25 17:40:08 UTC

```
Plan written to `.terminal_claude_agent_struct_out.json`: a single standardized dataset combining the Azure Functions 2019/2021 invocation traces (real arrivals + duration percentiles/per-call durations) and the Alibaba microservices call-graph trace (real per-call latencies, used for the regime-switch construction), producing 5 labeled regimes — 4 trace-derived (stationary, burst, drift, regime-switch), 1 explicitly synthetic (adversarial) — with documented risk-score and SLO-target formulas.
```
