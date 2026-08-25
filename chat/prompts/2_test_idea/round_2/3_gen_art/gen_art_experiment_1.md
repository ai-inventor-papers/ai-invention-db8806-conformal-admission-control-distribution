# gen_art_experiment_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_art`
> Run: `iter1_88afd6206a08` — Conformal Admission Control for Overloaded Request Queues
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-25 18:43:31 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<research_methodology>
Design experiments like a researcher, not a programmer running a script.

- Every method needs a meaningful baseline — the current standard approach, not a strawman.
- Control your variables. When comparing methods, hold everything else constant.
- Results need variance, not just point estimates. A single run proves nothing.
- Implement the proposed method and baseline side-by-side in the same pipeline to eliminate implementation-level confounds.
</research_methodology>

<task>
Implement the research methodology as a production-ready experimental system.
Adapt your implementation approach based on the hypothesis and domain requirements.
</task>

<critical_requirements>
- Fully implement the methodology described in hypothesis
- Use appropriate frameworks based on research domain
- Load and process data from the specified data_filepath
- Complete working systems
- Handle all edge cases, errors, and exceptions properly
- Always implement baseline comparison method
</critical_requirements>

<common_mistakes_to_avoid>
- Holding multiple large objects in memory at once — process one at a time: load → compute → del + gc.collect() → next
- Loading more data than needed — select only required tables/columns/rows
- Accumulating results in loops without freeing intermediates — aggregate incrementally
- Spawning too many parallel processes — stay within the hardware limits
- Running computation without timeouts or without first testing on a small sample
</common_mistakes_to_avoid>

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

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_1_idx1
type: experiment
title: Conformal Admission Control on Real Azure Traces
summary: >-
  Run the ACI-based conformal admission controller plus four baselines (fixed threshold, misspecified index policy, RL frozen
  on stationary regime, hindsight-optimal oracle) directly against the frozen, real Azure-trace-derived dataset (art_fAlkDy9YEd-N,
  210k rows / 5 regimes), with data-loading code strictly separated from policy code to close the self-referential-evaluation
  gap flagged in iteration 1. Sweep eta over 5 pre-registered values, run >=5 seeds per (policy, regime, eta) cell, and report
  violation-rate control and value-at-matched-safety with bootstrap CIs and Holm-corrected pairwise tests.
runpod_compute_profile: cpu_heavy
implementation_pseudocode: |-
  # === MODULE 1: data_loader.py  (imports NOTHING from policy.py) ===
  # Purpose: read the 4 dataset part files, reconstruct 210k rows, group by regime,
  # sort each regime by arrival_time. Exposes ONLY read-only accessor functions.

  def load_dataset(dataset_dir):
      rows = []
      for part_path in sorted(glob(f"{dataset_dir}/full_data_out/full_data_out_*.json")):
          part = json.load(open(part_path))
          rows.extend(part['datasets'][0]['examples'])
      # each example: input = JSON string {arrival_time, risk_score, slo_target,
      #   regime_label, function_id, is_synthetic}; output = 0/1 violation label
      parsed = []
      for ex in rows:
          feat = json.loads(ex['input'])
          parsed.append({
              'arrival_time': feat['arrival_time'],
              'risk_score': feat['risk_score'],
              'slo_target': feat['slo_target'],
              'regime': feat['regime_label'],
              'function_id': feat['function_id'],
              'is_synthetic': feat['is_synthetic'],
              'y': int(ex['output']),                     # ground-truth violation label
              'value': feat.get('value', estimate_value_proxy(feat)),  # if dataset lacks
                                                            # an explicit value field, define
                                                            # value = 1.0 (uniform) as the
                                                            # documented fallback -- log which
                                                            # branch was taken in method_out.json
              'realized_service_time': ex['metadata_realized_service_time'],
          })
      return parsed

  def group_by_regime_sorted(parsed_rows):
      by_regime = defaultdict(list)
      for r in parsed_rows:
          by_regime[r['regime']].append(r)
      for regime in by_regime:
          by_regime[regime].sort(key=lambda r: r['arrival_time'])
      return by_regime   # {'stationary': [...], 'burst': [...], 'drift': [...],
                          #  'regime_switch': [...], 'adversarial': [...]}

  # VALIDATE ON LOAD: assert len(parsed_rows) == 210000; assert set(by_regime.keys())
  # == {'stationary','burst','drift','regime_switch','adversarial'}; assert observed
  # per-regime violation rates are within ~1pp of the documented rates
  # (stationary 3.95%, burst 0.24%, drift 15.53%, regime_switch 3.09%, adversarial
  # 38.25%) -- fail loudly (raise, do not silently continue) if this check fails,
  # since it is the first, cheapest signal that the loader has misread the schema.


  # === MODULE 2: policy.py  (imports NOTHING from data_loader.py; pure functions
  # of a stream of (risk_score, slo_target, ...) inputs and externally-supplied
  # outcome labels -- never touches ground truth except via the replay loop's
  # explicit feedback call) ===

  class ConformalPolicy:
      """
      ACI admission rule (Gibbs & Candes 2021 single-parameter online
      gradient update), applied to admission instead of prediction-interval
      coverage:
          lambda_{t+1} = lambda_t + eta * (alpha - y_t)
          admit request t  iff  s(x_t) <= lambda_t
      where y_t in {0,1} is the SLO-violation OUTCOME of request t if admitted
      (0 if rejected -- rejected requests contribute no feedback and lambda_t
      is carried forward unchanged, since there is no observed outcome to
      condition on; this is documented explicitly as a deviation worth noting
      since Gibbs & Candes' original setting always observes an outcome).
      alpha = target violation rate (0.10). eta = step size, swept over
      {0.01, 0.02, 0.05, 0.10, 0.20}.
      lambda_0 initialized to a generous starting quantile
      (e.g. the 90th percentile of risk_score over a small warm-up prefix of
      the FIRST 200 rows of the regime being run, held out from evaluation --
      NOT the whole regime, to avoid look-ahead) so early decisions are not
      degenerate.
      """
      def __init__(self, alpha, eta, lambda_0):
          self.alpha, self.eta, self.lam = alpha, eta, lambda_0
          self.history = []  # (t, lambda_t, admit, s, y_observed)

      def decide(self, s_x):
          return s_x <= self.lam           # admit iff score <= current threshold

      def update(self, admitted, y_t):
          if admitted:
              self.lam = self.lam + self.eta * (self.alpha - y_t)
          # else: lambda unchanged (no observed outcome)

  class FixedThresholdPolicy: ...      # threshold tuned once on stationary-regime
                                         # warm-up prefix to hit target alpha, then
                                         # frozen for the rest of that regime AND
                                         # reused unchanged on every other regime
  class MisspecifiedIndexPolicy: ...    # Whittle/marginal-productivity-style index
                                         # computed under an assumed birth-death /
                                         # M/M/1-ish queueing model fit ONLY on the
                                         # stationary-regime warm-up prefix (this is
                                         # the "misspecification": the model is wrong
                                         # for burst/drift/regime_switch/adversarial
                                         # by construction)
  class FrozenRLPolicy: ...             # small tabular/linear-function-approx
                                         # Q-learning or REINFORCE agent, state =
                                         # (discretized risk_score, discretized
                                         # recent violation rate), trained ONLY on
                                         # the stationary regime's warm-up prefix
                                         # (e.g. first 20% of stationary rows),
                                         # then policy FROZEN (no further learning)
                                         # for evaluation on all 5 regimes
  class OracleHindsightPolicy: ...      # given full knowledge of this regime's
                                         # y-labels in advance, solve the offline
                                         # knapsack: admit the max-value subset
                                         # whose realized violation rate <= alpha
                                         # (LP relaxation + rounding, or greedy by
                                         # value/1 with a violation-budget cap) --
                                         # this is the value-vs-safety upper bound,
                                         # not a deployable policy


  # === MODULE 3: replay.py (the event loop; imports both modules but keeps them
  # used only through their public functions) ===

  def replay_regime(rows, policy, rng_seed):
      rng = np.random.default_rng(rng_seed)   # used ONLY for admission tie-
                                               # breaking (e.g. among equal scores)
                                               # and RL exploration noise during its
                                               # separate training phase -- NEVER to
                                               # perturb the trace data itself
      log = []
      for t, row in enumerate(rows):
          admit = policy.decide(row['risk_score'], tie_break_rng=rng)
          y_t = row['y'] if admit else None   # outcome only observed if admitted
          policy.update(admit, row['y'] if admit else 0)
          log.append({
              't': t, 'timestamp': row['arrival_time'], 'admit': bool(admit),
              'outcome': (row['y'] if admit else None),
              'threshold': getattr(policy, 'lam', None),
              'value_if_admitted': row['value'] if admit else 0.0,
          })
      return log

  def compute_metrics(log, alpha, window=2000):
      # rolling-window realized violation rate among ADMITTED requests only
      admitted = [e for e in log if e['admit']]
      y = [e['outcome'] for e in admitted]
      rolling = rolling_mean(y, window)
      mad_vs_alpha = mean(abs(r - alpha) for r in rolling)   # headline stat,
                                                              # matches iter-1's
                                                              # Table 1 metric
      total_value = sum(e['value_if_admitted'] for e in log)
      admit_rate = len(admitted) / len(log)
      return {'mad_vs_alpha': mad_vs_alpha, 'rolling_violation_rate': rolling,
              'total_value': total_value, 'admit_rate': admit_rate,
              'n_admitted': len(admitted)}


  # === MAIN DRIVER (main.py) ===

  ALPHA = 0.10
  ETAS = [0.01, 0.02, 0.05, 0.10, 0.20]
  SEEDS = list(range(5))            # >=5 independent seeds per cell, as required
  REGIMES = ['stationary', 'burst', 'drift', 'regime_switch', 'adversarial']
  POLICIES = ['conformal', 'fixed_threshold', 'misspecified_index',
              'frozen_rl', 'oracle']

  rows = load_dataset(DATASET_DIR)
  by_regime = group_by_regime_sorted(rows)
  validate_regime_rates(by_regime)   # hard assert per the doc'd violation rates

  results = []                       # flat list of per-cell metric dicts
  for regime in REGIMES:
      regime_rows = by_regime[regime]
      warmup, eval_rows = regime_rows[:200], regime_rows[200:]  # warm-up excluded
                                                                  # from evaluation
                                                                  # metrics
      for policy_name in POLICIES:
          eta_grid = ETAS if policy_name == 'conformal' else [None]  # eta only
                                                                       # applies to
                                                                       # conformal
          for eta in eta_grid:
              for seed in SEEDS:
                  policy = build_policy(policy_name, alpha=ALPHA, eta=eta,
                                         warmup_rows=warmup, seed=seed,
                                         # RL and index policies are FIT ONLY on
                                         # the STATIONARY regime's warm-up rows,
                                         # never on the regime being evaluated,
                                         # except when regime == 'stationary'
                                         fit_rows=by_regime['stationary'][:2000]
                                                  if policy_name in
                                                  ('frozen_rl','misspecified_index')
                                                  else warmup)
                  log = replay_regime(eval_rows, policy, rng_seed=seed)
                  metrics = compute_metrics(log, ALPHA)
                  results.append({'regime': regime, 'policy': policy_name,
                                   'eta': eta, 'seed': seed, **metrics})

  # statistical layer
  per_cell = aggregate_over_seeds(results)   # mean/CI via seed-level bootstrap
                                              # (percentile bootstrap, 10000 resamples)
  pairwise = holm_corrected_tests(results,   # conformal vs each baseline, per
                                   groupby=['regime'], metric='mad_vs_alpha',
                                   method='holm')  # re-test the 2 stationary-
                                                    # regime comparisons flagged
                                                    # non-significant in iter 1
                                                    # (p_holm=0.098 vs fixed-
                                                    # threshold and frozen-RL) --
                                                    # now with >=5 seeds x the
                                                    # real trace, check whether
                                                    # significance is reached

  # Phase 3: value-aware knapsack layer vs FCFS-among-eligible, same conformal
  # eligibility set, best eta selected from the Phase-0/1 sweep by MAD-to-alpha
  knapsack_results = run_knapsack_vs_fcfs(by_regime, best_eta, ALPHA, SEEDS)

  write_method_out_json({
    'table1_violation_rate_by_regime_policy': per_cell,
    'eta_sensitivity_sweep': {r: {e: per_cell[(r,'conformal',e)] for e in ETAS}
                               for r in REGIMES},
    'pairwise_significance_tests': pairwise,
    'value_at_matched_safety_stationary': ...,
    'knapsack_vs_fcfs': knapsack_results,
    'risk_score_formula_verbatim': RISK_SCORE_DOCSTRING_COPIED_FROM_DATASET,
    'aci_update_rule_docstring': ConformalPolicy.__doc__,
    'seed_manifest': {'seeds': SEEDS, 'etas': ETAS, 'alpha': ALPHA},
    'dataset_validation': {'n_rows': len(rows), 'per_regime_violation_rate': ...},
  })
fallback_plan: >-
  1) If the dataset's `input`/`output` schema does not literally match the documented field names (e.g. `risk_score` or `regime_label`
  missing or nested differently), first inspect `preview_data_out.json` (3 rows) before touching the full 210k-row files,
  adapt the loader's field-mapping only, and log the concrete schema in method_out.json rather than guessing. 2) If no explicit
  per-row `value` field exists in the dataset (the summary does not mention one explicitly), fall back to a documented, fixed
  value proxy (e.g. value = 1.0 uniformly, or value = 1/risk_score as a crude priority proxy) and state this substitution
  explicitly in method_out.json and flag it as a known limitation for the paper -- do not silently invent per-row values that
  could be mistaken for ground truth. 3) If the frozen-RL baseline is unstable or fails to train a sensible policy on only
  ~2000 stationary warm-up rows (a real risk with e.g. tabular Q-learning on sparse admission data), fall back to a simpler
  contextual-bandit-style linear policy (e.g. logistic regression on risk_score fit on the same warm-up rows, thresholded)
  and clearly document it as 'RL-style baseline (simplified)' rather than a full DRL agent -- the comparison's purpose (empirical-only
  safety, no formal guarantee) is preserved either way. 4) If the misspecified-index policy is hard to derive cleanly from
  Nino-Mora's polyhedral construction in the time available, substitute a simpler but still genuinely model-based baseline:
  fit an M/M/1-style queueing model (arrival rate, service rate) on the stationary warm-up prefix and derive an admission
  threshold from its steady-state overflow probability formula -- keep it clearly 'model-based, distributionally misspecified'
  in spirit. 5) If full 5-seed x 5-eta x 5-regime x 5-policy runs (625 cells, but conformal alone needs 5 regimes x 5 etas
  x 5 seeds = 125, others are 5 regimes x 1 eta x 5 seeds x 4 policies = 100, total 225 replay runs) are too slow given 210k
  rows, first profile a single replay of the largest regime; each replay is O(N) with O(1) per-row work, so 225 replays over
  ~50k rows average is well under an hour on cpu_heavy -- if still slow, parallelize regime x policy x eta x seed cells across
  processes (aii-parallel-computing, ProcessPoolExecutor) since cells are fully independent. 6) If the headline MAD-vs-alpha
  result does NOT hold within tolerance on the real trace data (unlike the self-generated simulator in iteration 1), do NOT
  suppress or rerun until it looks better -- report it exactly as found, since a disconfirming result on the primary real-data
  evaluation is itself the single most important finding this iteration is designed to surface, and downstream (paper) steps
  need the true number, not a flattering one. 7) If part files fail to load due to size (out-of-memory reading all 4 x ~50MB
  files at once), stream/parse them one at a time and only retain the parsed lightweight row dicts, discarding the raw JSON
  structures immediately after parsing each part.
testing_plan: >-
  Step 1 (schema smoke test, seconds): load ONLY preview_data_out.json (3 rows) and mini_data_out.json through data_loader.py,
  print every parsed field, and manually verify against the dataset's documented schema (arrival_time, risk_score, slo_target,
  regime_label, function_id, is_synthetic, output-as-violation-label) before touching the full files. Step 2 (loader correctness
  on full data, ~1 regime): load just full_data_out_1.json, group by regime, and check per-regime violation rates against
  the documented figures (stationary 3.95%, burst 0.24%, drift 15.53%, regime_switch 3.09%, adversarial 38.25%) -- if these
  do not match within ~1pp, STOP and fix the loader before running any policy code, since every downstream number depends
  on this being correct. Step 3 (policy unit test on a tiny synthetic stream, not the real data): feed ConformalPolicy a hand-constructed
  sequence of 50 (score, outcome) pairs with a known closed-form expected lambda trajectory (e.g. all outcomes=1 should monotonically
  decrease lambda by eta*alpha... actually verify sign: y_t=1 means alpha-y_t<0 so lambda decreases, tightening admission
  -- confirm this matches intuition: more violations -> stricter threshold) and assert the implementation matches by hand-computed
  values to floating-point precision. Step 4 (single-cell end-to-end, ~1 min): run ONE (policy=conformal, regime=stationary,
  eta=0.1, seed=0) cell on the full stationary-regime rows, confirm it produces a metrics dict with sane ranges (0<=admit_rate<=1,
  0<=mad_vs_alpha<=1, rolling violation rate roughly near alpha after burn-in) and that logs are non-empty and well-formed.
  Step 5 (small grid before full grid): run all 5 policies on just the stationary regime with 1 seed each (5 cells) and sanity-check
  relative behavior (oracle should have the highest value at matched safety; fixed-threshold/index/RL should behave reasonably
  in-distribution) before committing to the full 225-cell x 5-seed grid. Step 6 (full run): execute the complete grid, write
  method_out.json, then run aii-json validation on the output structure and spot-check that pairwise_significance_tests recomputes
  correctly by hand on 2-3 example cells (paired bootstrap CI and Holm correction). Step 7: confirm total wall-clock stayed
  well inside the 6h executor budget at each of the above checkpoints, aborting/simplifying per the fallback plan at the first
  checkpoint that looks too slow rather than discovering this at hour 5.
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

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

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

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

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for framework choices, implementation patterns, agent orchestration.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read preview files from dependencies to understand data structure. Use ALL datasets provided — do not skip or select a subset. Read domain handbook if applicable (see <available_domain_handbooks>). Test basic functionality with 'uv run'.
TODO 3. Fully implement our method AND baseline (comparison) as described in artifact plan in './method.py'. Use exp_gen_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant methods or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
```

### [2] HUMAN-USER prompt · 2026-08-25 18:43:31 UTC

```
Find a better admission control policy for overloaded request queues.
```

### [3] SKILL-INPUT — aii-python · 2026-08-25 18:43:37 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: "Applies this repo's Python conventions to experiment and evaluation scripts: uv-only environment setup (never pip), loguru logging with stdout plus a rotating file sink, @logger.catch(reraise=True) with explicit exception types, pathlib file access, type hints, and a standard main() script skeleton. ALWAYS read before writing or editing any Python script that runs an experiment, evaluation, or data-processing job. Triggers: writing or refactoring a Python script, uv venv, uv pip install, pyproject dependencies, loguru, logging setup, try/except and error handling, pathlib, script structure, Python 3.12. NOT for: parallelism, GPU throughput or hardware sizing (use aii-parallel-computing and aii-use-hardware), scaling long autonomous jobs (use aii-long-running-tasks), splitting oversized output files (use aii-file-size-limit), calling LLMs (use aii-openrouter-llms), or notebooks meant for Colab (use aii-colab)."
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-08-25 18:43:37 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: "Scales an experiment or evaluation up in stages — mini, 10, 50, 100, 200, then the largest run that fits — recording runtime at each step and extrapolating time-per-example against the remaining time budget before growing further, with background execution and hard RLIMIT_AS and RLIMIT_CPU caps. ALWAYS read before launching any script expected to run for many minutes or hours over a dataset. Triggers: long-running job, overnight or unattended run, time budget, how many examples fit, extrapolate runtime, start small then scale up, run in background and poll, avoid a timeout, full-dataset evaluation, resource limits. NOT for choosing the concurrency mechanism itself (aii-parallel-computing), measuring the machine's CPU, RAM or GPU (aii-use-hardware), or provisioning cloud pods (aii-runpod)."
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [5] SKILL-INPUT — aii-json · 2026-08-25 18:43:37 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: "Validates JSON files against this repo's experiment-pipeline schemas (exp_sel_data_out, exp_gen_sol_out, exp_eval_sol_out, exp_proof_out) and generates size-optimized full, mini and preview variants of any JSON array file. ALWAYS use before treating a pipeline stage output as finished, whenever a schema or required-property error must be fixed, and whenever a large JSON file needs a small truncated version safe to read. Triggers: JSON schema validation, schema compliance, required property errors, pipeline stage outputs, the exp_*_out format names, mini and preview JSON generation, shrinking a large JSON before inspection. NOT for: discovering or downloading new datasets, which aii-hf-datasets and aii-owid-datasets cover; splitting oversized output files, which aii-file-size-limit covers; plotting JSON data, which aii-data-fig-gen covers; spreadsheet and .csv tabular data, which anthropic-xlsx covers."
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [6] SKILL-INPUT — aii-use-hardware · 2026-08-25 18:43:37 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: "Detects the CPU, RAM, GPU and VRAM actually available — cgroup v1 and v2 container quotas and CPU affinity rather than misleading host values — then sets RAM and VRAM budgets via resource.setrlimit and torch.cuda.set_per_process_memory_fraction so a script raises a catchable error instead of being OOM-killed, and picks the right torch wheel for the detected device. ALWAYS read before loading a large dataset, installing torch, or sizing batches and worker counts. Triggers: how much RAM or CPU or GPU is available, container memory limit, cgroup, OOM killed, MemoryError, os.cpu_count reports host cores, nproc, VRAM, CUDA available, CPU-only torch build, dataset too big for memory, chunking. NOT for spreading work across that hardware once measured (aii-parallel-computing), staged scale-up runs against a time budget (aii-long-running-tasks), or renting cloud machines (aii-runpod)."
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [7] SKILL-INPUT — aii-parallel-computing · 2026-08-25 18:43:37 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "Parallelises compute-heavy Python: asyncio with aiohttp and a bounded Semaphore for I/O-bound work, ProcessPoolExecutor under the spawn start method for CPU-bound work, NumPy vectorisation and batched PyTorch on GPU with an out-of-memory halving fallback. ALWAYS read before writing any script that loops over data, issues many API calls, downloads many files, or runs heavy computation — sequential loops are the default failure mode. Triggers: parallelise, make a slow script faster, concurrency, async, aiohttp, asyncio.gather, semaphore, multiprocessing, ProcessPoolExecutor, fork deadlock with loguru, worker count, batch size, CUDA out of memory, idle GPU, retries and rate limits. NOT for detecting what hardware exists or setting RAM and VRAM budgets (aii-use-hardware), staged scale-up against a time budget (aii-long-running-tasks), or provisioning cloud pods (aii-runpod)."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [8] SKILL-INPUT — aii-file-size-limit · 2026-08-25 18:43:37 UTC

The agent loaded the **aii-file-size-limit** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-file-size-limit
description: "Splits an oversized generated output file into numbered parts that each fit a size limit: checks sizes with ls -lh, writes full_data_out_1.json, full_data_out_2.json and so on into a matching directory, deletes the original, repoints the reading code at a sorted glob, and regenerates mini and preview variants per part. ALWAYS run right after a script writes JSON output, and whenever a file is too big to keep, exceeds a stated file size limit, or gets rejected for its size. Triggers: file too large, output exceeds the size limit, oversized or huge JSON, ls -lh size check after generating results, splitting or chunking an output file into parts, output directory instead of one file. NOT for: schema validation or making mini and preview variants of a file already within the limit (use aii-json), or general Python script conventions (use aii-python)."
---

## File Size Check

After generating output files, run `ls -lh` to check sizes. If ANY file exceeds the provided file size limit:

1. Create directory with same base name (e.g., `data_out/` for `full_data_out.json`)
2. Split into parts under the limit named: `full_data_out_1.json`, `full_data_out_2.json`, etc.
3. Place parts in directory (e.g., `data_out/full_data_out_1.json`, `data_out/full_data_out_2.json`)
4. Delete the original oversized file
5. Update the script to read from split files: `for f in sorted(glob.glob('data_out/full_data_out_*.json')): data.extend(json.load(open(f)))`
6. For each split part, generate its own mini/preview versions with the json skill's format script
```

### [9] SYSTEM-USER prompt · 2026-08-25 18:49:15 UTC

````
pected_files"
  ],
  "title": "ExperimentArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
</prompt>
````
