# gen_demo_art_evaluation_2 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `iter1_88afd6206a08` — Conformal Admission Control for Overloaded Request Queues
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_evaluation_2` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-08-25 19:32:13 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz
```

### [2] SYSTEM-USER prompt · 2026-08-25 19:32:21 UTC

````
<conversion_philosophy>
**MINIMAL CHANGES — PRESERVE THE ORIGINAL CODE**

The goal is to make the artifact's code READABLE, UNDERSTANDABLE, and RUNNABLE in a short time
to someone reviewing the research, with the option to easily scale parameters back to original
values for a full run (which can take much longer). Think of this as annotating and reformatting,
not refactoring.

**DO:**
- Split the original script into logical notebook cells (imports, setup, processing, results)
- Add markdown cells BETWEEN code cells explaining what each section does and why
- Add inline comments where the logic is non-obvious
- Add a visualization/summary cell at the end showing key outputs
- Fix hardcoded file paths to use the GitHub data loading pattern

**DO NOT:**
- Rewrite functions or change algorithms
- Rename variables or restructure logic
- Add error handling, type hints, or "improvements" that weren't in the original
- Simplify or "clean up" the original code
- Remove any original comments or logic
- Change the computational approach

The reader should recognize the original script when looking at the notebook — it's the
same code, just split into cells with explanatory markdown between sections.
</conversion_philosophy>

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
Your workspace: `/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/`:
GOOD: `/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/file.py`, `/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<task>
Convert this artifact's Python script into a demo notebook with MINIMAL changes to the original code.
Split into cells, add markdown explanations between sections, add a visualization cell at the end.
Output: mini_demo_data.json + code_demo.ipynb (notebook that loads data from GitHub URL)
</task>

<artifact_info>
id: art_k4NZEyG_q_yz
type: evaluation
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
out_demo_files:
- path: eval.py
  description: Evaluation script with metrics computation
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json

URLs won't work yet — files pushed to GitHub AFTER notebook creation.
Use local fallback pattern so notebook works locally (now) and in Colab (after deployment).
</github_repo>

<data_file_sizes>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_file_sizes>

<install_dependencies_pattern>
Follow the aii-colab skill exactly. It has the install cell pattern, pre-installed package list, numpy 2.0 compat shims, and all Colab-specific rules.
</install_dependencies_pattern>

<data_loading_pattern>
`mini_demo_data.json` = curated subset for the demo.
Use this pattern for Colab compatibility (GitHub URL with local fallback):
```python
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json"
import json, os

def load_data():
    try:
        import urllib.request
        with urllib.request.urlopen(GITHUB_DATA_URL) as response:
            return json.loads(response.read().decode())
    except Exception: pass
    if os.path.exists("mini_demo_data.json"):
        with open("mini_demo_data.json") as f: return json.load(f)
    raise FileNotFoundError("Could not load mini_demo_data.json")
```
</data_loading_pattern>

<notebook_structure>
--- Setup ---
Cell 1 (markdown): Title, description, what this artifact does.
Cell 2 (code): Install dependencies — follow the aii-colab skill's install cell pattern exactly. Fill in all packages imported by the artifact's code.
Cell 3 (code): Imports — copy original import block as-is, plus any additional imports needed for the notebook (e.g. matplotlib for visualization).
Cell 4 (code): Data loading helper — use the <data_loading_pattern> above.
Cell 5 (code): `data = load_data()`

--- Config ---
Config cell (code): Define ALL tunable parameters (iterations, epochs, n_samples, hidden_size, etc.) as variables at the top of this cell. Start with the ABSOLUTE MINIMUM values — the smallest that produce any output at all (e.g. 1 iteration, 2 samples, smallest array size). These get gradually increased during testing — see TODOs.

--- Processing ---
Remaining cells: One code cell per logical section of the original script. Add a markdown cell BEFORE each code cell. Copy code as closely as possible, with these changes:
  1. Replace file paths to use the loaded `data` variable.
  2. Use the config variables from the config cell (NOT hardcoded values).
  3. Minimal fixes are allowed if something doesn't work in notebook context (e.g. adjusting paths, removing CLI args, fixing imports), but keep changes to the absolute minimum.

--- Results ---
Visualization cell (code): Print key results in a readable table, plot numeric data with matplotlib if appropriate.
</notebook_structure>

<priority>
WORKING > OPTIMIZED. A small-scale demo that runs correctly is the goal. Once the notebook passes with minimum config values, scale up only if time permits — do NOT spend multiple retries chasing larger parameters. If a working version exists, finish and move on.
</priority>

<max_notebook_total_runtime>600s (10 min)</max_notebook_total_runtime>

<test_environment>
To test-run the notebook in a clean environment (simulating Colab), create a disposable `.nb_env` in your workspace:
```bash
/usr/local/bin/python3.12 -m venv .nb_env
.nb_env/bin/pip install -q pip jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
rm -rf .nb_env
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.

What happens: the .venv starts empty (just jupyter). When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DemoExpectedFiles": {
      "description": "Expected output files from code demo notebook generation.",
      "properties": {
        "notebook": {
          "default": "",
          "description": "Path to the generated demo notebook. Example: 'code_demo.ipynb'",
          "title": "Notebook",
          "type": "string"
        },
        "mini_data_file": {
          "default": "",
          "description": "Path to the mini demo data JSON (curated subset). Example: 'mini_demo_data.json'",
          "title": "Mini Data File",
          "type": "string"
        }
      },
      "title": "DemoExpectedFiles",
      "type": "object"
    }
  },
  "description": "Dataset/experiment/evaluation \u2192 Jupyter notebook demo.\n\nTitle and summary come from the parent artifact (gen_art step),\nnot from the demo agent. The agent only outputs expected files.",
  "properties": {
    "out_expected_files": {
      "$ref": "#/$defs/DemoExpectedFiles",
      "description": "All output files you created. Must include the demo notebook."
    }
  },
  "required": [],
  "title": "CodeDemo",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-25 19:32:21 UTC

```
Find a better admission control policy for overloaded request queues.
```

### [4] TOOL CALL — Bash · 2026-08-25 19:32:27 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && ls -la && echo "---source---" && ls -la /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
```

### [5] TOOL CALL — Skill · 2026-08-25 19:32:27 UTC

```
aii-colab
```

### [6] TOOL CALL — Skill · 2026-08-25 19:32:27 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Bash · 2026-08-25 19:32:27 UTC

```
{"stdout": "total 2951\ndrwxrwxrwx 2 root root 1001880 Aug 25 19:32 .\ndrwxrwxrwx 4 root root 2000117 Aug 25 19:30 ..\n-rw-rw-rw- 1 root root   21897 Aug 25 19:32 .repl_agent.ptylog\n---source---\ntotal 13001\ndrwxrwxrwx 7 root root 2033775 Aug 25 18:55 .\ndrwxrwxrwx 4 root root 2070271 Aug 25 18:41 ..\n-rw-rw-rw- 1 root root  892864 Aug 25 18:55 .repl_agent.ptylog\n-rw-rw-rw- 1 root root    4643 Aug 25 18:55 .terminal_claude_agent_struct_out.json\ndrwxrwxrwx 5 root root 2013789 Aug 25 18:46 .venv\ndrwxrwxrwx 3 root root 2019732 Aug 25 18:43 data\n-rw-rw-rw- 1 root root   54153 Aug 25 18:54 eval.py\n-rw-rw-rw- 1 root root   62747 Aug 25 18:55 eval_out.json\ndrwxrwxrwx 2 root root 2000135 Aug 25 18:52 figures\n-rw-rw-rw- 1 root root   62747 Aug 25 18:55 full_eval_out.json\ndrwxrwxrwx 2 root root 1002012 Aug 25 18:49 logs\n-rw-rw-rw- 1 root root   51521 Aug 25 18:55 mini_eval_out.json\n-rw-rw-rw- 1 root root   33684 Aug 25 18:55 preview_eval_out.json\n-rw-rw-rw- 1 root root     391 Aug 25 18:55 pyproject.toml\ndrwxrwxrwx 2 root root 1006127 Aug 25 18:52 results", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [8] TOOL RESULT — Skill · 2026-08-25 19:32:27 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [9] TOOL RESULT — Skill · 2026-08-25 19:32:27 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [10] TOOL CALL — Read · 2026-08-25 19:32:33 UTC

```
/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/eval.py
```

### [11] TOOL RESULT — Read · 2026-08-25 19:32:33 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [12] TOOL CALL — Bash · 2026-08-25 19:32:33 UTC

```
cd /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1 && head -c 3000 preview_eval_out.json && echo "..." && ls data/
```

### [13] TOOL RESULT — Bash · 2026-08-25 19:32:33 UTC

```
{"stdout": "{\n  \"metadata\": {\n    \"evaluation_name\": \"conformal_admission_control_real_trace_verdict_iter2\",\n    \"dependency_status\": {\n      \"art_fAlkDy9YEd-N_dataset\": \"available_and_used_as_primary_data_source (real Azure trace, 210000 rows)\",\n      \"gen_art_experiment_1_iter2\": \"empty_at_execution_time -- no method_out.json existed\",\n      \"resolution\": \"5 admission policies implemented directly in eval.py, run against the REAL independently-produced trace dataset (not a self-generated simulator). See module docstring + VALIDITY_NOTES for full rationa...\"\n    },\n    \"validity_notes\": [\n      \"gen_art_experiment_1 (per-policy simulation logs / method_out.json) was EMPTY at evaluation time. Per the plan's own validity check, this technically triggers a HALT. Resolution taken (documented in e...\",\n      \"The dataset has no per-request 'value' field. A deterministic, documented proxy value = 1/slo_target (tighter SLO = more business-critical request) is used for the matched-value and knapsack analyses;...\",\n      \"The dataset has no per-request queueing 'load' signal either. A local-arrival-rate proxy (inverse of the trailing-50-request mean inter-arrival time, min-max normalized per regime-trace) is used where...\"\n    ],\n    \"pre_registered_validity_checks\": {\n      \"total_row_count\": 210000,\n      \"total_row_count_matches_210000\": true,\n      \"base_rate_cross_check\": {\n        \"overall\": {\n          \"expected\": 0.0906,\n          \"computed_from_dataset\": 0.0906,\n          \"abs_diff\": 0.0,\n          \"within_tolerance_5e-4\": true\n        },\n        \"stationary\": {\n          \"expected\": 0.0395,\n          \"computed_from_dataset\": 0.0395,\n          \"abs_diff\": 0.0,\n          \"within_tolerance_5e-4\": true\n        },\n        \"burst\": {\n          \"expected\": 0.0024,\n          \"computed_from_dataset\": 0.0024,\n          \"abs_diff\": 0.0,\n          \"within_tolerance_5e-4\": true\n        },\n        \"drift\": {\n          \"expected\": 0.1553,\n          \"computed_from_dataset\": 0.1553,\n          \"abs_diff\": 0.0,\n          \"within_tolerance_5e-4\": true\n        },\n        \"regime_switch\": {\n          \"expected\": 0.0309,\n          \"computed_from_dataset\": 0.0309,\n          \"abs_diff\": 0.0,\n          \"within_tolerance_5e-4\": true\n        },\n        \"adversarial\": {\n          \"expected\": 0.3825,\n          \"computed_from_dataset\": 0.3825,\n          \"abs_diff\": 0.0,\n          \"within_tolerance_5e-4\": true\n        }\n      },\n      \"all_base_rates_match\": true,\n      \"method_out_json_provenance_check\": {\n        \"passed\": false,\n        \"reason\": \"gen_art_experiment_1 directory was empty; no method_out.json exists to check provenance/metadata fields against. See VALIDITY_NOTES[0] for the resolution taken.\"\n      },\n      \"eval_and_experiment_different_code_paths\": {\n        \"passed\": null,\n        \"reason\": \"N/A -- no separate experiment artifact exists this iteration to compare against.\"\n      },\n      \"n_seeds_per_cell_ge_5\": {\n        \"passed\": true,\n        \"n_seeds\": 5,\n        \"...\ndata.py\nfull_data_out\niter1_eval_out.json\nmini_data_out.json\npreview_data_out.json", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-08-25 19:32:39 UTC

```
cd /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/data && ls -la full_data_out/ && python3 -c "
import json
d = json.load(open('preview_data_out.json'))
print(list(d.keys()))
ex = d['datasets'][0]['examples']
print(len(ex))
print(ex[0])
print(json.loads(ex[0]['input']))
"
```

### [15] TOOL RESULT — Bash [ERROR] · 2026-08-25 19:32:39 UTC

```
Error: Exit code 1
total 205954
drwxrwxrwx 2 root root  2019727 Aug 25 18:43 .
drwxrwxrwx 3 root root  2019732 Aug 25 18:43 ..
-rw-rw-rw- 1 root root 53484128 Aug 25 18:43 full_data_out_1.json
-rw-rw-rw- 1 root root 53192647 Aug 25 18:43 full_data_out_2.json
-rw-rw-rw- 1 root root 53470009 Aug 25 18:43 full_data_out_3.json
-rw-rw-rw- 1 root root 46709039 Aug 25 18:43 full_data_out_4.json
Traceback (most recent call last):
  File "<string>", line 8, in <module>
  File "/usr/local/lib/python3.12/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/json/decoder.py", line 338, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/json/decoder.py", line 354, in raw_decode
    obj, end = self.scan_once(s, idx)
               ^^^^^^^^^^^^^^^^^^^^^^
json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 115 (char 114)
['metadata', 'datasets']
3
{'input': '{"arrival_time": 1.0115, "risk_score": 0.454962, "slo_target": 0.01, "regime_label": "stationary", "function_id": "95dc325a4a22f2d6368e04c54265752aad1ef0207cd08ed2ffa698403f3c30b3/0148f7c3e28fbf32b7f5...', 'output': '0', 'metadata_fold': 0, 'metadata_task_type': 'classification', 'metadata_n_classes': 2, 'metadata_regime_label': 'stationary', 'metadata_function_id': '95dc325a4a22f2d6368e04c54265752aad1ef0207cd08ed2ffa698403f3c30b3/0148f7c3e28fbf32b7f514307b74ca3f1fb5f9c98a9d555319920f445bbae7f8/8b6b487641e053d54d0088e499987d181b34bb4010ed68a2635d08816e26022c', 'metadata_request_id': 0, 'metadata_is_synthetic': False, 'metadata_provenance': 'azure_functions_2019', 'metadata_service_time': 0.0028, 'metadata_slo_target': 0.01, 'metadata_feature_names': ['arrival_time', 'risk_score', 'slo_target']}
```

### [16] TOOL CALL — Bash · 2026-08-25 19:32:45 UTC

```
cd /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/data && ls -la mini_data_out.json && python3 -c "
import json
d = json.load(open('mini_data_out.json'))
ex = d['datasets'][0]['examples']
print(len(ex))
import collections
c = collections.Counter()
for e in ex:
    inp = json.loads(e['input'])
    c[inp['regime_label']] += 1
print(c)
print(ex[0])
"
```

### [17] TOOL RESULT — Bash · 2026-08-25 19:32:45 UTC

```
{"stdout": "-rw-rw-rw- 1 root root 4628 Aug 25 18:43 mini_data_out.json\n3\nCounter({'stationary': 3})\n{'input': '{\"arrival_time\": 1.0115, \"risk_score\": 0.454962, \"slo_target\": 0.01, \"regime_label\": \"stationary\", \"function_id\": \"95dc325a4a22f2d6368e04c54265752aad1ef0207cd08ed2ffa698403f3c30b3/0148f7c3e28fbf32b7f514307b74ca3f1fb5f9c98a9d555319920f445bbae7f8/8b6b487641e053d54d0088e499987d181b34bb4010ed68a2635d08816e26022c\", \"is_synthetic\": false}', 'output': '0', 'metadata_fold': 0, 'metadata_task_type': 'classification', 'metadata_n_classes': 2, 'metadata_regime_label': 'stationary', 'metadata_function_id': '95dc325a4a22f2d6368e04c54265752aad1ef0207cd08ed2ffa698403f3c30b3/0148f7c3e28fbf32b7f514307b74ca3f1fb5f9c98a9d555319920f445bbae7f8/8b6b487641e053d54d0088e499987d181b34bb4010ed68a2635d08816e26022c', 'metadata_request_id': 0, 'metadata_is_synthetic': False, 'metadata_provenance': 'azure_functions_2019', 'metadata_service_time': 0.0028, 'metadata_slo_target': 0.01, 'metadata_feature_names': ['arrival_time', 'risk_score', 'slo_target', 'regime_label', 'function_id', 'is_synthetic']}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-08-25 19:32:59 UTC

```
cd /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/data && python3 -c "
import json, glob
regimes = ['stationary','burst','drift','regime_switch','adversarial']
picked = {r: [] for r in regimes}
target = 20
parts = sorted(glob.glob('full_data_out/full_data_out_*.json'))
for p in parts:
    d = json.load(open(p))
    ex = d['datasets'][0]['examples']
    for e in ex:
        inp = json.loads(e['input'])
        r = inp['regime_label']
        if len(picked[r]) < target:
            picked[r].append(e)
    if all(len(v)>=target for v in picked.values()):
        break
    print(p, {k: len(v) for k,v in picked.items()})
out = {'metadata': {}, 'datasets':[{'dataset':'real_azure_trace_admission_control_mini','examples': [e for r in regimes for e in picked[r]]}]}
print('total', len(out['datasets'][0]['examples']))
json.dump(out, open('/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/mini_demo_data.json','w'))
"
```

### [19] TOOL RESULT — Bash · 2026-08-25 19:32:59 UTC

```
{"stdout": "full_data_out/full_data_out_1.json {'stationary': 20, 'burst': 20, 'drift': 0, 'regime_switch': 0, 'adversarial': 0}\nfull_data_out/full_data_out_2.json {'stationary': 20, 'burst': 20, 'drift': 20, 'regime_switch': 0, 'adversarial': 0}\nfull_data_out/full_data_out_3.json {'stationary': 20, 'burst': 20, 'drift': 20, 'regime_switch': 20, 'adversarial': 0}\ntotal 100", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — ToolSearch · 2026-08-25 19:33:11 UTC

```
{'query': 'select:NotebookEdit'}
```

### [21] TOOL RESULT — ToolSearch · 2026-08-25 19:33:11 UTC

```
{"matches": ["NotebookEdit"], "query": "select:NotebookEdit", "total_deferred_tools": 18}
```

### [22] TOOL CALL — Write · 2026-08-25 19:33:17 UTC

```
File: /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb

{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["# placeholder"],
   "id": "placeholder-cell"
  }
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python", "version": "3.12"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

### [23] TOOL RESULT — Write · 2026-08-25 19:33:17 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "content": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": [\"# placeholder\"],\n   \"id\": \"placeholder-cell\"\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n  \"language_info\": {\"name\": \"python\", \"version\": \"3.12\"}\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [24] TOOL CALL — Read · 2026-08-25 19:33:19 UTC

```
/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb
```

### [25] TOOL RESULT — Read · 2026-08-25 19:33:19 UTC

```
{"type": "notebook", "file": {"filePath": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "cells": [{"cellType": "markdown", "source": "# placeholder", "cell_id": "placeholder-cell"}]}}
```

### [26] ASSISTANT · 2026-08-25 19:33:31 UTC

```
Now let's build out all cells.
```

### [27] TOOL CALL — NotebookEdit · 2026-08-25 19:33:31 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': 'placeholder-cell', 'cell_type': 'markdown', 'new_source': "# Real-Trace Verdict for Admission Control\\n\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\n\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\n\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\n- the **max transient spike**,\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\n\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced."}
```

### [28] TOOL RESULT — NotebookEdit · 2026-08-25 19:33:31 UTC

```
{"new_source": "# Real-Trace Verdict for Admission Control\\n\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\n\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\n\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\n- the **max transient spike**,\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\n\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.", "old_source": "# placeholder", "cell_type": "markdown", "language": "python", "edit_mode": "replace", "cell_id": "placeholder-cell", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": [\"# placeholder\"],\n   \"id\": \"placeholder-cell\"\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n  \"language_info\": {\"name\": \"python\", \"version\": \"3.12\"}\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}\n", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [29] TOOL CALL — NotebookEdit · 2026-08-25 19:33:39 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': 'placeholder-cell', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': "import subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru -- not pre-installed on Colab, always install\n_pip('loguru==0.7.3')\n\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')"}
```

### [30] TOOL RESULT — NotebookEdit · 2026-08-25 19:33:39 UTC

```
{"new_source": "import subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru -- not pre-installed on Colab, always install\n_pip('loguru==0.7.3')\n\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "94b50414", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [31] TOOL CALL — NotebookEdit · 2026-08-25 19:33:43 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '94b50414', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': '# --- Imports (copied from the original eval.py\'s import block, plus matplotlib for viz) ---\nfrom __future__ import annotations\n\nimport gc\nimport json\nimport time\nfrom typing import Any\n\nimport numpy as np\nfrom loguru import logger\nimport matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\n\nlogger.remove()\nlogger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")'}
```

### [32] TOOL RESULT — NotebookEdit · 2026-08-25 19:33:45 UTC

```
{"new_source": "# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\nfrom __future__ import annotations\n\nimport gc\nimport json\nimport time\nfrom typing import Any\n\nimport numpy as np\nfrom loguru import logger\nimport matplotlib\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "986d6bb1", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [33] TOOL CALL — NotebookEdit · 2026-08-25 19:33:49 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '986d6bb1', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json"\nimport os\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception:\n        pass\n    if os.path.exists("mini_demo_data.json"):\n        with open("mini_demo_data.json") as f:\n            return json.load(f)\n    raise FileNotFoundError("Could not load mini_demo_data.json")'}
```

### [34] TOOL RESULT — NotebookEdit · 2026-08-25 19:33:49 UTC

```
{"new_source": "GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\"\nimport os\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception:\n        pass\n    if os.path.exists(\"mini_demo_data.json\"):\n        with open(\"mini_demo_data.json\") as f:\n            return json.load(f)\n    raise FileNotFoundError(\"Could not load mini_demo_data.json\")", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "53e42205", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [35] TOOL CALL — NotebookEdit · 2026-08-25 19:33:53 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '53e42205', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'data = load_data()\nprint("regimes present:", sorted({json.loads(e["input"])["regime_label"] for e in data["datasets"][0]["examples"]}))\nprint("total rows:", len(data["datasets"][0]["examples"]))'}
```

### [36] TOOL RESULT — NotebookEdit · 2026-08-25 19:33:53 UTC

```
{"new_source": "data = load_data()\nprint(\"regimes present:\", sorted({json.loads(e[\"input\"])[\"regime_label\"] for e in data[\"datasets\"][0][\"examples\"]}))\nprint(\"total rows:\", len(data[\"datasets\"][0][\"examples\"]))", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "3c0e4f6a", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"3c0e4f6a\",\n   \"source\": \"data = load_data()\\nprint(\\\"regimes present:\\\", sorted({json.loads(e[\\\"input\\\"])[\\\"regime_label\\\"] for e in data[\\\"datasets\\\"][0][\\\"examples\\\"]}))\\nprint(\\\"total rows:\\\", len(data[\\\"datasets\\\"][0][\\\"examples\\\"]))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [37] ASSISTANT · 2026-08-25 19:33:59 UTC

```
Now the config markdown + cell:
```

### [38] TOOL CALL — NotebookEdit · 2026-08-25 19:33:59 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '3c0e4f6a', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': "## Config\\n\\nAll tunable parameters from the original `eval.py`, collected in one place. Values here are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `N_SEEDS=5`, `N_BOOTSTRAP=10_000`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used."}
```

### [39] TOOL RESULT — NotebookEdit · 2026-08-25 19:33:59 UTC

```
{"new_source": "## Config\\n\\nAll tunable parameters from the original `eval.py`, collected in one place. Values here are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `N_SEEDS=5`, `N_BOOTSTRAP=10_000`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used.", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "a5404677", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"3c0e4f6a\",\n   \"source\": \"data = load_data()\\nprint(\\\"regimes present:\\\", sorted({json.loads(e[\\\"input\\\"])[\\\"regime_label\\\"] for e in data[\\\"datasets\\\"][0][\\\"examples\\\"]}))\\nprint(\\\"total rows:\\\", len(data[\\\"datasets\\\"][0][\\\"examples\\\"]))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"3c0e4f6a\",\n   \"source\": \"data = load_data()\\nprint(\\\"regimes present:\\\", sorted({json.loads(e[\\\"input\\\"])[\\\"regime_label\\\"] for e in data[\\\"datasets\\\"][0][\\\"examples\\\"]}))\\nprint(\\\"total rows:\\\", len(data[\\\"datasets\\\"][0][\\\"examples\\\"]))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"a5404677\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `eval.py`, collected in one place. Values here are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `N_SEEDS=5`, `N_BOOTSTRAP=10_000`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [40] TOOL CALL — NotebookEdit · 2026-08-25 19:34:07 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': 'a5404677', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'ALPHA = 0.10\nWINDOW = 5           # rolling window, in ADMITTED requests (original: 500)\nBURN_IN_MIN = 2      # (original: 500)\nBURN_IN_FRAC = 0.05\nTOL_PP = 0.03\nN_SEEDS = 3          # >=5 required for a genuine over-seed bootstrap in the full run (original: 5)\nN_BOOTSTRAP = 200    # whole-seed resample draws (original: 10_000)\nCALIB_SEED = 777\nREGIMES = ["stationary", "burst", "drift", "regime_switch", "adversarial"]\nBASELINES = ["fixed_threshold", "index_based", "rl_frozen"]\nALL_POLICIES = ["conformal_aci"] + BASELINES + ["oracle_hindsight"]\nRL_LOAD_WEIGHT = 0.6\nETA_GRID = [0.05, 0.10, 0.20]  # subset of original [0.01, 0.02, 0.05, 0.10, 0.20]\nETA_PRIMARY = 0.05\nLOAD_WINDOW = 5      # requests, for the local-arrival-rate load proxy (original: 50)\nRNG_GLOBAL = np.random.default_rng(20260825)'}
```

### [41] TOOL RESULT — NotebookEdit · 2026-08-25 19:34:07 UTC

```
{"new_source": "ALPHA = 0.10\nWINDOW = 5           # rolling window, in ADMITTED requests (original: 500)\nBURN_IN_MIN = 2      # (original: 500)\nBURN_IN_FRAC = 0.05\nTOL_PP = 0.03\nN_SEEDS = 3          # >=5 required for a genuine over-seed bootstrap in the full run (original: 5)\nN_BOOTSTRAP = 200    # whole-seed resample draws (original: 10_000)\nCALIB_SEED = 777\nREGIMES = [\"stationary\", \"burst\", \"drift\", \"regime_switch\", \"adversarial\"]\nBASELINES = [\"fixed_threshold\", \"index_based\", \"rl_frozen\"]\nALL_POLICIES = [\"conformal_aci\"] + BASELINES + [\"oracle_hindsight\"]\nRL_LOAD_WEIGHT = 0.6\nETA_GRID = [0.05, 0.10, 0.20]  # subset of original [0.01, 0.02, 0.05, 0.10, 0.20]\nETA_PRIMARY = 0.05\nLOAD_WINDOW = 5      # requests, for the local-arrival-rate load proxy (original: 50)\nRNG_GLOBAL = np.random.default_rng(20260825)", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "8d51313a", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"3c0e4f6a\",\n   \"source\": \"data = load_data()\\nprint(\\\"regimes present:\\\", sorted({json.loads(e[\\\"input\\\"])[\\\"regime_label\\\"] for e in data[\\\"datasets\\\"][0][\\\"examples\\\"]}))\\nprint(\\\"total rows:\\\", len(data[\\\"datasets\\\"][0][\\\"examples\\\"]))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"a5404677\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `eval.py`, collected in one place. Values here are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `N_SEEDS=5`, `N_BOOTSTRAP=10_000`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"3c0e4f6a\",\n   \"source\": \"data = load_data()\\nprint(\\\"regimes present:\\\", sorted({json.loads(e[\\\"input\\\"])[\\\"regime_label\\\"] for e in data[\\\"datasets\\\"][0][\\\"examples\\\"]}))\\nprint(\\\"total rows:\\\", len(data[\\\"datasets\\\"][0][\\\"examples\\\"]))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"a5404677\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `eval.py`, collected in one place. Values here are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `N_SEEDS=5`, `N_BOOTSTRAP=10_000`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"8d51313a\",\n   \"source\": \"ALPHA = 0.10\\nWINDOW = 5           # rolling window, in ADMITTED requests (original: 500)\\nBURN_IN_MIN = 2      # (original: 500)\\nBURN_IN_FRAC = 0.05\\nTOL_PP = 0.03\\nN_SEEDS = 3          # >=5 required for a genuine over-seed bootstrap in the full run (original: 5)\\nN_BOOTSTRAP = 200    # whole-seed resample draws (original: 10_000)\\nCALIB_SEED = 777\\nREGIMES = [\\\"stationary\\\", \\\"burst\\\", \\\"drift\\\", \\\"regime_switch\\\", \\\"adversarial\\\"]\\nBASELINES = [\\\"fixed_threshold\\\", \\\"index_based\\\", \\\"rl_frozen\\\"]\\nALL_POLICIES = [\\\"conformal_aci\\\"] + BASELINES + [\\\"oracle_hindsight\\\"]\\nRL_LOAD_WEIGHT = 0.6\\nETA_GRID = [0.05, 0.10, 0.20]  # subset of original [0.01, 0.02, 0.05, 0.10, 0.20]\\nETA_PRIMARY = 0.05\\nLOAD_WINDOW = 5      # requests, for the local-arrival-rate load proxy (original: 50)\\nRNG_GLOBAL = np.random.default_rng(20260825)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [42] ASSISTANT · 2026-08-25 19:34:15 UTC

```
Now data-loading (regime arrays) section:
```

### [43] TOOL CALL — NotebookEdit · 2026-08-25 19:34:15 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '8d51313a', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Step 0: parse the trace rows into per-regime NumPy arrays\\n\\nThe original script reads `full_data_out_*.json` parts off disk with `glob`. Here we read the same per-row schema (`arrival_time`, `risk_score`, `slo_target`, `regime_label`, `function_id`, plus the binary violation `label`) directly out of the already-loaded `data` object. The per-regime sort-by-`arrival_time` logic is unchanged.'}
```

### [44] TOOL RESULT — NotebookEdit · 2026-08-25 19:34:15 UTC

```
{"new_source": "## Step 0: parse the trace rows into per-regime NumPy arrays\\n\\nThe original script reads `full_data_out_*.json` parts off disk with `glob`. Here we read the same per-row schema (`arrival_time`, `risk_score`, `slo_target`, `regime_label`, `function_id`, plus the binary violation `label`) directly out of the already-loaded `data` object. The per-regime sort-by-`arrival_time` logic is unchanged.", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "18882e0f", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"3c0e4f6a\",\n   \"source\": \"data = load_data()\\nprint(\\\"regimes present:\\\", sorted({json.loads(e[\\\"input\\\"])[\\\"regime_label\\\"] for e in data[\\\"datasets\\\"][0][\\\"examples\\\"]}))\\nprint(\\\"total rows:\\\", len(data[\\\"datasets\\\"][0][\\\"examples\\\"]))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"a5404677\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `eval.py`, collected in one place. Values here are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `N_SEEDS=5`, `N_BOOTSTRAP=10_000`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"8d51313a\",\n   \"source\": \"ALPHA = 0.10\\nWINDOW = 5           # rolling window, in ADMITTED requests (original: 500)\\nBURN_IN_MIN = 2      # (original: 500)\\nBURN_IN_FRAC = 0.05\\nTOL_PP = 0.03\\nN_SEEDS = 3          # >=5 required for a genuine over-seed bootstrap in the full run (original: 5)\\nN_BOOTSTRAP = 200    # whole-seed resample draws (original: 10_000)\\nCALIB_SEED = 777\\nREGIMES = [\\\"stationary\\\", \\\"burst\\\", \\\"drift\\\", \\\"regime_switch\\\", \\\"adversarial\\\"]\\nBASELINES = [\\\"fixed_threshold\\\", \\\"index_based\\\", \\\"rl_frozen\\\"]\\nALL_POLICIES = [\\\"conformal_aci\\\"] + BASELINES + [\\\"oracle_hindsight\\\"]\\nRL_LOAD_WEIGHT = 0.6\\nETA_GRID = [0.05, 0.10, 0.20]  # subset of original [0.01, 0.02, 0.05, 0.10, 0.20]\\nETA_PRIMARY = 0.05\\nLOAD_WINDOW = 5      # requests, for the local-arrival-rate load proxy (original: 50)\\nRNG_GLOBAL = np.random.default_rng(20260825)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"3c0e4f6a\",\n   \"source\": \"data = load_data()\\nprint(\\\"regimes present:\\\", sorted({json.loads(e[\\\"input\\\"])[\\\"regime_label\\\"] for e in data[\\\"datasets\\\"][0][\\\"examples\\\"]}))\\nprint(\\\"total rows:\\\", len(data[\\\"datasets\\\"][0][\\\"examples\\\"]))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"a5404677\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `eval.py`, collected in one place. Values here are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `N_SEEDS=5`, `N_BOOTSTRAP=10_000`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"8d51313a\",\n   \"source\": \"ALPHA = 0.10\\nWINDOW = 5           # rolling window, in ADMITTED requests (original: 500)\\nBURN_IN_MIN = 2      # (original: 500)\\nBURN_IN_FRAC = 0.05\\nTOL_PP = 0.03\\nN_SEEDS = 3          # >=5 required for a genuine over-seed bootstrap in the full run (original: 5)\\nN_BOOTSTRAP = 200    # whole-seed resample draws (original: 10_000)\\nCALIB_SEED = 777\\nREGIMES = [\\\"stationary\\\", \\\"burst\\\", \\\"drift\\\", \\\"regime_switch\\\", \\\"adversarial\\\"]\\nBASELINES = [\\\"fixed_threshold\\\", \\\"index_based\\\", \\\"rl_frozen\\\"]\\nALL_POLICIES = [\\\"conformal_aci\\\"] + BASELINES + [\\\"oracle_hindsight\\\"]\\nRL_LOAD_WEIGHT = 0.6\\nETA_GRID = [0.05, 0.10, 0.20]  # subset of original [0.01, 0.02, 0.05, 0.10, 0.20]\\nETA_PRIMARY = 0.05\\nLOAD_WINDOW = 5      # requests, for the local-arrival-rate load proxy (original: 50)\\nRNG_GLOBAL = np.random.default_rng(20260825)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"18882e0f\",\n   \"source\": \"## Step 0: parse the trace rows into per-regime NumPy arrays\\\\n\\\\nThe original script reads `full_data_out_*.json` parts off disk with `glob`. Here we read the same per-row schema (`arrival_time`, `risk_score`, `slo_target`, `regime_label`, `function_id`, plus the binary violation `label`) directly out of the already-loaded `data` object. The per-regime sort-by-`arrival_time` logic is unchanged.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [45] TOOL CALL — NotebookEdit · 2026-08-25 19:34:23 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '18882e0f', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def load_regime_arrays() -> dict[str, dict[str, np.ndarray]]:\n    by_regime: dict[str, dict[str, list]] = {\n        r: {"arrival_time": [], "risk_score": [], "slo_target": [], "label": [], "function_id": []} for r in REGIMES\n    }\n    examples = data["datasets"][0]["examples"]\n    total = 0\n    for e in examples:\n        inp = json.loads(e["input"])\n        r = inp["regime_label"]\n        if r not in by_regime:\n            raise ValueError(f"Unexpected regime_label {r!r} in dataset (row provenance mismatch)")\n        by_regime[r]["arrival_time"].append(float(inp["arrival_time"]))\n        by_regime[r]["risk_score"].append(float(inp["risk_score"]))\n        by_regime[r]["slo_target"].append(float(inp["slo_target"]))\n        by_regime[r]["label"].append(int(e["output"]))\n        by_regime[r]["function_id"].append(inp["function_id"])\n        total += 1\n    logger.info(f"Loaded {total} rows from mini_demo_data.json")\n    out = {}\n    for r, cols in by_regime.items():\n        idx_sorted = np.argsort(np.asarray(cols["arrival_time"]), kind="stable")\n        out[r] = {\n            "arrival_time": np.asarray(cols["arrival_time"])[idx_sorted],\n            "risk_score": np.asarray(cols["risk_score"])[idx_sorted],\n            "slo_target": np.asarray(cols["slo_target"])[idx_sorted],\n            "label": np.asarray(cols["label"], dtype=bool)[idx_sorted],\n            "function_id": np.asarray(cols["function_id"], dtype=object)[idx_sorted],\n        }\n    return out, total\n\n\nregime_arrays, total_rows = load_regime_arrays()\nfor r in REGIMES:\n    lab = regime_arrays[r]["label"]\n    logger.info(f"regime={r}: n={len(lab)}, violation_rate={lab.mean():.4f}")'}
```

### [46] TOOL RESULT — NotebookEdit · 2026-08-25 19:34:23 UTC

```
{"new_source": "def load_regime_arrays() -> dict[str, dict[str, np.ndarray]]:\n    by_regime: dict[str, dict[str, list]] = {\n        r: {\"arrival_time\": [], \"risk_score\": [], \"slo_target\": [], \"label\": [], \"function_id\": []} for r in REGIMES\n    }\n    examples = data[\"datasets\"][0][\"examples\"]\n    total = 0\n    for e in examples:\n        inp = json.loads(e[\"input\"])\n        r = inp[\"regime_label\"]\n        if r not in by_regime:\n            raise ValueError(f\"Unexpected regime_label {r!r} in dataset (row provenance mismatch)\")\n        by_regime[r][\"arrival_time\"].append(float(inp[\"arrival_time\"]))\n        by_regime[r][\"risk_score\"].append(float(inp[\"risk_score\"]))\n        by_regime[r][\"slo_target\"].append(float(inp[\"slo_target\"]))\n        by_regime[r][\"label\"].append(int(e[\"output\"]))\n        by_regime[r][\"function_id\"].append(inp[\"function_id\"])\n        total += 1\n    logger.info(f\"Loaded {total} rows from mini_demo_data.json\")\n    out = {}\n    for r, cols in by_regime.items():\n        idx_sorted = np.argsort(np.asarray(cols[\"arrival_time\"]), kind=\"stable\")\n        out[r] = {\n            \"arrival_time\": np.asarray(cols[\"arrival_time\"])[idx_sorted],\n            \"risk_score\": np.asarray(cols[\"risk_score\"])[idx_sorted],\n            \"slo_target\": np.asarray(cols[\"slo_target\"])[idx_sorted],\n            \"label\": np.asarray(cols[\"label\"], dtype=bool)[idx_sorted],\n            \"function_id\": np.asarray(cols[\"function_id\"], dtype=object)[idx_sorted],\n        }\n    return out, total\n\n\nregime_arrays, total_rows = load_regime_arrays()\nfor r in REGIMES:\n    lab = regime_arrays[r][\"label\"]\n    logger.info(f\"regime={r}: n={len(lab)}, violation_rate={lab.mean():.4f}\")", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "e896fe37", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"3c0e4f6a\",\n   \"source\": \"data = load_data()\\nprint(\\\"regimes present:\\\", sorted({json.loads(e[\\\"input\\\"])[\\\"regime_label\\\"] for e in data[\\\"datasets\\\"][0][\\\"examples\\\"]}))\\nprint(\\\"total rows:\\\", len(data[\\\"datasets\\\"][0][\\\"examples\\\"]))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"a5404677\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `eval.py`, collected in one place. Values here are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `N_SEEDS=5`, `N_BOOTSTRAP=10_000`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"8d51313a\",\n   \"source\": \"ALPHA = 0.10\\nWINDOW = 5           # rolling window, in ADMITTED requests (original: 500)\\nBURN_IN_MIN = 2      # (original: 500)\\nBURN_IN_FRAC = 0.05\\nTOL_PP = 0.03\\nN_SEEDS = 3          # >=5 required for a genuine over-seed bootstrap in the full run (original: 5)\\nN_BOOTSTRAP = 200    # whole-seed resample draws (original: 10_000)\\nCALIB_SEED = 777\\nREGIMES = [\\\"stationary\\\", \\\"burst\\\", \\\"drift\\\", \\\"regime_switch\\\", \\\"adversarial\\\"]\\nBASELINES = [\\\"fixed_threshold\\\", \\\"index_based\\\", \\\"rl_frozen\\\"]\\nALL_POLICIES = [\\\"conformal_aci\\\"] + BASELINES + [\\\"oracle_hindsight\\\"]\\nRL_LOAD_WEIGHT = 0.6\\nETA_GRID = [0.05, 0.10, 0.20]  # subset of original [0.01, 0.02, 0.05, 0.10, 0.20]\\nETA_PRIMARY = 0.05\\nLOAD_WINDOW = 5      # requests, for the local-arrival-rate load proxy (original: 50)\\nRNG_GLOBAL = np.random.default_rng(20260825)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"18882e0f\",\n   \"source\": \"## Step 0: parse the trace rows into per-regime NumPy arrays\\\\n\\\\nThe original script reads `full_data_out_*.json` parts off disk with `glob`. Here we read the same per-row schema (`arrival_time`, `risk_score`, `slo_target`, `regime_label`, `function_id`, plus the binary violation `label`) directly out of the already-loaded `data` object. The per-regime sort-by-`arrival_time` logic is unchanged.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"3c0e4f6a\",\n   \"source\": \"data = load_data()\\nprint(\\\"regimes present:\\\", sorted({json.loads(e[\\\"input\\\"])[\\\"regime_label\\\"] for e in data[\\\"datasets\\\"][0][\\\"examples\\\"]}))\\nprint(\\\"total rows:\\\", len(data[\\\"datasets\\\"][0][\\\"examples\\\"]))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"a5404677\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `eval.py`, collected in one place. Values here are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `N_SEEDS=5`, `N_BOOTSTRAP=10_000`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"8d51313a\",\n   \"source\": \"ALPHA = 0.10\\nWINDOW = 5           # rolling window, in ADMITTED requests (original: 500)\\nBURN_IN_MIN = 2      # (original: 500)\\nBURN_IN_FRAC = 0.05\\nTOL_PP = 0.03\\nN_SEEDS = 3          # >=5 required for a genuine over-seed bootstrap in the full run (original: 5)\\nN_BOOTSTRAP = 200    # whole-seed resample draws (original: 10_000)\\nCALIB_SEED = 777\\nREGIMES = [\\\"stationary\\\", \\\"burst\\\", \\\"drift\\\", \\\"regime_switch\\\", \\\"adversarial\\\"]\\nBASELINES = [\\\"fixed_threshold\\\", \\\"index_based\\\", \\\"rl_frozen\\\"]\\nALL_POLICIES = [\\\"conformal_aci\\\"] + BASELINES + [\\\"oracle_hindsight\\\"]\\nRL_LOAD_WEIGHT = 0.6\\nETA_GRID = [0.05, 0.10, 0.20]  # subset of original [0.01, 0.02, 0.05, 0.10, 0.20]\\nETA_PRIMARY = 0.05\\nLOAD_WINDOW = 5      # requests, for the local-arrival-rate load proxy (original: 50)\\nRNG_GLOBAL = np.random.default_rng(20260825)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"18882e0f\",\n   \"source\": \"## Step 0: parse the trace rows into per-regime NumPy arrays\\\\n\\\\nThe original script reads `full_data_out_*.json` parts off disk with `glob`. Here we read the same per-row schema (`arrival_time`, `risk_score`, `slo_target`, `regime_label`, `function_id`, plus the binary violation `label`) directly out of the already-loaded `data` object. The per-regime sort-by-`arrival_time` logic is unchanged.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"e896fe37\",\n   \"source\": \"def load_regime_arrays() -> dict[str, dict[str, np.ndarray]]:\\n    by_regime: dict[str, dict[str, list]] = {\\n        r: {\\\"arrival_time\\\": [], \\\"risk_score\\\": [], \\\"slo_target\\\": [], \\\"label\\\": [], \\\"function_id\\\": []} for r in REGIMES\\n    }\\n    examples = data[\\\"datasets\\\"][0][\\\"examples\\\"]\\n    total = 0\\n    for e in examples:\\n        inp = json.loads(e[\\\"input\\\"])\\n        r = inp[\\\"regime_label\\\"]\\n        if r not in by_regime:\\n            raise ValueError(f\\\"Unexpected regime_label {r!r} in dataset (row provenance mismatch)\\\")\\n        by_regime[r][\\\"arrival_time\\\"].append(float(inp[\\\"arrival_time\\\"]))\\n        by_regime[r][\\\"risk_score\\\"].append(float(inp[\\\"risk_score\\\"]))\\n        by_regime[r][\\\"slo_target\\\"].append(float(inp[\\\"slo_target\\\"]))\\n        by_regime[r][\\\"label\\\"].append(int(e[\\\"output\\\"]))\\n        by_regime[r][\\\"function_id\\\"].append(inp[\\\"function_id\\\"])\\n        total += 1\\n    logger.info(f\\\"Loaded {total} rows from mini_demo_data.json\\\")\\n    out = {}\\n    for r, cols in by_regime.items():\\n        idx_sorted = np.argsort(np.asarray(cols[\\\"arrival_time\\\"]), kind=\\\"stable\\\")\\n        out[r] = {\\n            \\\"arrival_time\\\": np.asarray(cols[\\\"arrival_time\\\"])[idx_sorted],\\n            \\\"risk_score\\\": np.asarray(cols[\\\"risk_score\\\"])[idx_sorted],\\n            \\\"slo_target\\\": np.asarray(cols[\\\"slo_target\\\"])[idx_sorted],\\n            \\\"label\\\": np.asarray(cols[\\\"label\\\"], dtype=bool)[idx_sorted],\\n            \\\"function_id\\\": np.asarray(cols[\\\"function_id\\\"], dtype=object)[idx_sorted],\\n        }\\n    return out, total\\n\\n\\nregime_arrays, total_rows = load_regime_arrays()\\nfor r in REGIMES:\\n    lab = regime_arrays[r][\\\"label\\\"]\\n    logger.info(f\\\"regime={r}: n={len(lab)}, violation_rate={lab.mean():.4f}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [47] ASSISTANT · 2026-08-25 19:34:31 UTC

```
Now value/load proxies + seeded trace section:
```

### [48] TOOL CALL — NotebookEdit · 2026-08-25 19:34:31 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': 'e896fe37', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Step 0b: value + load proxies, bootstrap-resampled seeded traces\\n\\nThe dataset has no native per-request `value` or `load` field, so the original script builds two documented proxies: `value` blends per-function SLO tightness with the per-request `risk_score`, and `load` is a local inverse-inter-arrival-time signal. Because the real trace has no native seed/replicate dimension, each "seed" is an i.i.d. bootstrap resample of that regime\'s rows, re-sorted by arrival time — this is what supplies the `N_SEEDS` needed for the over-seed bootstrap later.'}
```

### [49] TOOL RESULT — NotebookEdit · 2026-08-25 19:34:31 UTC

```
{"new_source": "## Step 0b: value + load proxies, bootstrap-resampled seeded traces\\n\\nThe dataset has no native per-request `value` or `load` field, so the original script builds two documented proxies: `value` blends per-function SLO tightness with the per-request `risk_score`, and `load` is a local inverse-inter-arrival-time signal. Because the real trace has no native seed/replicate dimension, each \"seed\" is an i.i.d. bootstrap resample of that regime's rows, re-sorted by arrival time — this is what supplies the `N_SEEDS` needed for the over-seed bootstrap later.", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "c3fc8367", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"3c0e4f6a\",\n   \"source\": \"data = load_data()\\nprint(\\\"regimes present:\\\", sorted({json.loads(e[\\\"input\\\"])[\\\"regime_label\\\"] for e in data[\\\"datasets\\\"][0][\\\"examples\\\"]}))\\nprint(\\\"total rows:\\\", len(data[\\\"datasets\\\"][0][\\\"examples\\\"]))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"a5404677\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `eval.py`, collected in one place. Values here are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `N_SEEDS=5`, `N_BOOTSTRAP=10_000`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"8d51313a\",\n   \"source\": \"ALPHA = 0.10\\nWINDOW = 5           # rolling window, in ADMITTED requests (original: 500)\\nBURN_IN_MIN = 2      # (original: 500)\\nBURN_IN_FRAC = 0.05\\nTOL_PP = 0.03\\nN_SEEDS = 3          # >=5 required for a genuine over-seed bootstrap in the full run (original: 5)\\nN_BOOTSTRAP = 200    # whole-seed resample draws (original: 10_000)\\nCALIB_SEED = 777\\nREGIMES = [\\\"stationary\\\", \\\"burst\\\", \\\"drift\\\", \\\"regime_switch\\\", \\\"adversarial\\\"]\\nBASELINES = [\\\"fixed_threshold\\\", \\\"index_based\\\", \\\"rl_frozen\\\"]\\nALL_POLICIES = [\\\"conformal_aci\\\"] + BASELINES + [\\\"oracle_hindsight\\\"]\\nRL_LOAD_WEIGHT = 0.6\\nETA_GRID = [0.05, 0.10, 0.20]  # subset of original [0.01, 0.02, 0.05, 0.10, 0.20]\\nETA_PRIMARY = 0.05\\nLOAD_WINDOW = 5      # requests, for the local-arrival-rate load proxy (original: 50)\\nRNG_GLOBAL = np.random.default_rng(20260825)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"18882e0f\",\n   \"source\": \"## Step 0: parse the trace rows into per-regime NumPy arrays\\\\n\\\\nThe original script reads `full_data_out_*.json` parts off disk with `glob`. Here we read the same per-row schema (`arrival_time`, `risk_score`, `slo_target`, `regime_label`, `function_id`, plus the binary violation `label`) directly out of the already-loaded `data` object. The per-regime sort-by-`arrival_time` logic is unchanged.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"e896fe37\",\n   \"source\": \"def load_regime_arrays() -> dict[str, dict[str, np.ndarray]]:\\n    by_regime: dict[str, dict[str, list]] = {\\n        r: {\\\"arrival_time\\\": [], \\\"risk_score\\\": [], \\\"slo_target\\\": [], \\\"label\\\": [], \\\"function_id\\\": []} for r in REGIMES\\n    }\\n    examples = data[\\\"datasets\\\"][0][\\\"examples\\\"]\\n    total = 0\\n    for e in examples:\\n        inp = json.loads(e[\\\"input\\\"])\\n        r = inp[\\\"regime_label\\\"]\\n        if r not in by_regime:\\n            raise ValueError(f\\\"Unexpected regime_label {r!r} in dataset (row provenance mismatch)\\\")\\n        by_regime[r][\\\"arrival_time\\\"].append(float(inp[\\\"arrival_time\\\"]))\\n        by_regime[r][\\\"risk_score\\\"].append(float(inp[\\\"risk_score\\\"]))\\n        by_regime[r][\\\"slo_target\\\"].append(float(inp[\\\"slo_target\\\"]))\\n        by_regime[r][\\\"label\\\"].append(int(e[\\\"output\\\"]))\\n        by_regime[r][\\\"function_id\\\"].append(inp[\\\"function_id\\\"])\\n        total += 1\\n    logger.info(f\\\"Loaded {total} rows from mini_demo_data.json\\\")\\n    out = {}\\n    for r, cols in by_regime.items():\\n        idx_sorted = np.argsort(np.asarray(cols[\\\"arrival_time\\\"]), kind=\\\"stable\\\")\\n        out[r] = {\\n            \\\"arrival_time\\\": np.asarray(cols[\\\"arrival_time\\\"])[idx_sorted],\\n            \\\"risk_score\\\": np.asarray(cols[\\\"risk_score\\\"])[idx_sorted],\\n            \\\"slo_target\\\": np.asarray(cols[\\\"slo_target\\\"])[idx_sorted],\\n            \\\"label\\\": np.asarray(cols[\\\"label\\\"], dtype=bool)[idx_sorted],\\n            \\\"function_id\\\": np.asarray(cols[\\\"function_id\\\"], dtype=object)[idx_sorted],\\n        }\\n    return out, total\\n\\n\\nregime_arrays, total_rows = load_regime_arrays()\\nfor r in REGIMES:\\n    lab = regime_arrays[r][\\\"label\\\"]\\n    logger.info(f\\\"regime={r}: n={len(lab)}, violation_rate={lab.mean():.4f}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Trace Verdict for Admission Control\\\\n\\\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Azure Functions trace data** (210,000 rows across 5 traffic regimes: `stationary`, `burst`, `drift`, `regime_switch`, `adversarial`).\\\\n\\\\nThe original experiment step (`gen_art_experiment_1`) was empty when this evaluation ran, so — as documented in the original script's docstring — the 5 admission policies (`conformal_aci`, `fixed_threshold`, `index_based`, `rl_frozen`, `oracle_hindsight`) are implemented directly in the evaluation code and run against the real trace data. For each `(policy, regime)` cell the script computes:\\\\n\\\\n- a rolling **admitted-request violation rate** (window of `WINDOW` admitted requests),\\\\n- the post-burn-in **mean absolute deviation (MAD)** from the target `alpha`, with a pass/fail tolerance flag,\\\\n- the **max transient spike**,\\\\n- over-seed **bootstrap 95% CIs** and **Holm-Bonferroni-corrected** paired significance tests (conformal vs. each baseline).\\\\n\\\\nThis demo runs the *same code* on a small 100-row subset (20 rows per regime) with shrunk config values (window size, seed count, bootstrap draws) so it finishes in seconds instead of the full run's longer wall-clock time. The code itself — the policies, the rolling-stat math, the bootstrap/Holm logic — is unchanged from the original `eval.py`; only the input size and a few tunable constants are reduced.\",\n   \"id\": \"placeholder-cell\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"94b50414\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"986d6bb1\",\n   \"source\": \"# --- Imports (copied from the original eval.py's import block, plus matplotlib for viz) ---\\nfrom __future__ import annotations\\n\\nimport gc\\nimport json\\nimport time\\nfrom typing import Any\\n\\nimport numpy as np\\nfrom loguru import logger\\nimport matplotlib\\nmatplotlib.use(\\\"Agg\\\")\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"53e42205\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"3c0e4f6a\",\n   \"source\": \"data = load_data()\\nprint(\\\"regimes present:\\\", sorted({json.loads(e[\\\"input\\\"])[\\\"regime_label\\\"] for e in data[\\\"datasets\\\"][0][\\\"examples\\\"]}))\\nprint(\\\"total rows:\\\", len(data[\\\"datasets\\\"][0][\\\"examples\\\"]))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"a5404677\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `eval.py`, collected in one place. Values here are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `N_SEEDS=5`, `N_BOOTSTRAP=10_000`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"8d51313a\",\n   \"source\": \"ALPHA = 0.10\\nWINDOW = 5           # rolling window, in ADMITTED requests (original: 500)\\nBURN_IN_MIN = 2      # (original: 500)\\nBURN_IN_FRAC = 0.05\\nTOL_PP = 0.03\\nN_SEEDS = 3          # >=5 required for a genuine over-seed bootstrap in the full run (original: 5)\\nN_BOOTSTRAP = 200    # whole-seed resample draws (original: 10_000)\\nCALIB_SEED = 777\\nREGIMES = [\\\"stationary\\\", \\\"burst\\\", \\\"drift\\\", \\\"regime_switch\\\", \\\"adversarial\\\"]\\nBASELINES = [\\\"fixed_threshold\\\", \\\"index_based\\\", \\\"rl_frozen\\\"]\\nALL_POLICIES = [\\\"conformal_aci\\\"] + BASELINES + [\\\"oracle_hindsight\\\"]\\nRL_LOAD_WEIGHT = 0.6\\nETA_GRID = [0.05, 0.10, 0.20]  # subset of original [0.01, 0.02, 0.05, 0.10, 0.20]\\nETA_PRIMARY = 0.05\\nLOAD_WINDOW = 5      # requests, for the local-arrival-rate load proxy (original: 50)\\nRNG_GLOBAL = np.random.default_rng(20260825)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"18882e0f\",\n   \"source\": \"## Step 0: parse the trace rows into per-regime NumPy arrays\\\\n\\\\nThe original script reads `full_data_out_*.json` parts off disk with `glob`. Here we read the same per-row schema (`arrival_time`, `risk_score`, `slo_target`, `regime_label`, `function_id`, plus the binary violation `label`) directly out of the already-loaded `data` object. The per-regime sort-by-`arrival_time` logic is unchanged.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"e896fe37\",\n   \"source\": \"def load_regime_arrays() -> dict[str, dict[str, np.ndarray]]:\\n    by_regime: dict[str, dict[str, list]] = {\\n        r: {\\\"arrival_time\\\": [], \\\"risk_score\\\": [], \\\"slo_target\\\": [], \\\"label\\\": [], \\\"function_id\\\": []} for r in REGIMES\\n    }\\n    examples = data[\\\"datasets\\\"][0][\\\"examples\\\"]\\n    total = 0\\n    for e in examples:\\n        inp = json.loads(e[\\\"input\\\"])\\n        r = inp[\\\"regime_label\\\"]\\n        if r not in by_regime:\\n            raise ValueError(f\\\"Unexpected regime_label {r!r} in dataset (row provenance mismatch)\\\")\\n        by_regime[r][\\\"arrival_time\\\"].append(float(inp[\\\"arrival_time\\\"]))\\n        by_regime[r][\\\"risk_score\\\"].append(float(inp[\\\"risk_score\\\"]))\\n        by_regime[r][\\\"slo_target\\\"].append(float(inp[\\\"slo_target\\\"]))\\n        by_regime[r][\\\"label\\\"].append(int(e[\\\"output\\\"]))\\n        by_regime[r][\\\"function_id\\\"].append(inp[\\\"function_id\\\"])\\n        total += 1\\n    logger.info(f\\\"Loaded {total} rows from mini_demo_data.json\\\")\\n    out = {}\\n    for r, cols in by_regime.items():\\n        idx_sorted = np.argsort(np.asarray(cols[\\\"arrival_time\\\"]), kind=\\\"stable\\\")\\n        out[r] = {\\n            \\\"arrival_time\\\": np.asarray(cols[\\\"arrival_time\\\"])[idx_sorted],\\n            \\\"risk_score\\\": np.asarray(cols[\\\"risk_score\\\"])[idx_sorted],\\n            \\\"slo_target\\\": np.asarray(cols[\\\"slo_target\\\"])[idx_sorted],\\n            \\\"label\\\": np.asarray(cols[\\\"label\\\"], dtype=bool)[idx_sorted],\\n            \\\"function_id\\\": np.asarray(cols[\\\"function_id\\\"], dtype=object)[idx_sorted],\\n        }\\n    return out, total\\n\\n\\nregime_arrays, total_rows = load_regime_arrays()\\nfor r in REGIMES:\\n    lab = regime_arrays[r][\\\"label\\\"]\\n    logger.info(f\\\"regime={r}: n={len(lab)}, violation_rate={lab.mean():.4f}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"c3fc8367\",\n   \"source\": \"## Step 0b: value + load proxies, bootstrap-resampled seeded traces\\\\n\\\\nThe dataset has no native per-request `value` or `load` field, so the original script builds two documented proxies: `value` blends per-function SLO tightness with the per-request `risk_score`, and `load` is a local inverse-inter-arrival-time signal. Because the real trace has no native seed/replicate dimension, each \\\"seed\\\" is an i.i.d. bootstrap resample of that regime's rows, re-sorted by arrival time — this is what supplies the `N_SEEDS` needed for the over-seed bootstrap later.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [50] TOOL CALL — NotebookEdit · 2026-08-25 19:34:43 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': 'c3fc8367', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def value_proxy(slo_target: np.ndarray, risk_score: np.ndarray, global_median_inv_slo: float) -> np.ndarray:\n    """Deterministic proxy: (1/slo_target) scaled by a per-request risk_score factor so the\n    value signal varies at REQUEST granularity, not just per-function. Pure 1/slo_target alone\n    is a per-function constant on this real trace (most regimes are dominated by a single\n    function_id -- see VALIDITY_NOTES), which would make knapsack-vs-FCFS trivially\n    indistinguishable from FCFS everywhere. risk_score is already a genuine per-request\n    admission-time signal, so blending it in keeps the proxy request-specific and documented."""\n    return (1.0 / slo_target) * (0.25 + 0.75 * risk_score) / global_median_inv_slo\n\n\ndef local_load_proxy(arrival_time: np.ndarray, window: int = LOAD_WINDOW) -> np.ndarray:\n    n = len(arrival_time)\n    load = np.zeros(n)\n    for i in range(n):\n        lo = max(0, i - window + 1)\n        span = arrival_time[i] - arrival_time[lo]\n        cnt = i - lo\n        load[i] = (cnt / span) if span > 1e-9 else (load[i - 1] if i > 0 else 0.0)\n    lo_v, hi_v = np.percentile(load, [1, 99])\n    if hi_v <= lo_v:\n        hi_v = lo_v + 1e-9\n    return np.clip((load - lo_v) / (hi_v - lo_v), 0.0, 1.0)\n\n\ndef estimate_switch_index(function_id: np.ndarray) -> int:\n    n = len(function_id)\n    first = function_id[0]\n    for i in range(1, n - 100):\n        if function_id[i] != first:\n            block = function_id[i : i + 100]\n            if np.all(block != first):\n                return i\n    return n // 2\n\n\ndef make_seeded_trace(regime_arrays: dict[str, np.ndarray], seed: int, global_median_inv_slo: float) -> dict[str, np.ndarray]:\n    n = len(regime_arrays["label"])\n    rng = np.random.default_rng(seed * 1_000_003 + 17)\n    resample_idx = rng.integers(0, n, size=n)\n    order = np.argsort(regime_arrays["arrival_time"][resample_idx], kind="stable")\n    idx = resample_idx[order]\n    arrival_time = regime_arrays["arrival_time"][idx]\n    risk_score = regime_arrays["risk_score"][idx]\n    label = regime_arrays["label"][idx]\n    slo_target = regime_arrays["slo_target"][idx]\n    function_id = regime_arrays["function_id"][idx]\n    load = local_load_proxy(arrival_time)\n    return {\n        "arrival_time": arrival_time,\n        "score": risk_score,\n        # composite_score is the nonconformity signal actually used by conformal_aci and\n        # fixed_threshold: on this real trace, raw risk_score is NEAR-CONSTANT within most\n        # regimes (single dominant function_id per regime -- see VALIDITY_NOTES), which would\n        # collapse a score-only threshold into an all-or-nothing step function and defeat\n        # ACI\'s online modulation entirely. Both risk_score and the load proxy are legitimate\n        # admission-time-only signals, so blending them (0.5/0.5) restores genuine granularity\n        # while staying faithful to the "admission-time features only" constraint.\n        "composite_score": 0.5 * risk_score + 0.5 * load,\n        "would_violate": label,\n        "value": value_proxy(slo_target, risk_score, global_median_inv_slo),\n        "load": load,\n        "function_id": function_id,\n    }'}
```

### [51] TOOL RESULT — NotebookEdit · 2026-08-25 19:34:43 UTC

```
{"new_source": "def value_proxy(slo_target: np.ndarray, risk_score: np.ndarray, global_median_inv_slo: float) -> np.ndarray:\n    \"\"\"Deterministic proxy: (1/slo_target) scaled by a per-request risk_score factor so the\n    value signal varies at REQUEST granularity, not just per-function. Pure 1/slo_target alone\n    is a per-function constant on this real trace (most regimes are dominated by a single\n    function_id -- see VALIDITY_NOTES), which would make knapsac... [truncated, 25708 chars total]
```

### [52] ASSISTANT · 2026-08-25 19:34:51 UTC

```
Now the policies section:
```

### [53] TOOL CALL — NotebookEdit · 2026-08-25 19:34:51 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': 'a22f4ec9', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## The 5 admission policies\\n\\n`conformal_aci` is the proposed policy — it online-adjusts an admission threshold via an ACI-style update after every admitted request. The four comparisons are: a frozen `fixed_threshold` calibrated once offline, a frozen `index_based` load cap, a frozen `rl_frozen` load/score blend, and the non-causal `oracle_hindsight` that greedily admits the lowest-violation-probability requests per window subject to the alpha budget (an upper bound, not a deployable policy).'}
```

### [54] TOOL RESULT — NotebookEdit · 2026-08-25 19:34:51 UTC

```
{"new_source": "## The 5 admission policies\\n\\n`conformal_aci` is the proposed policy — it online-adjusts an admission threshold via an ACI-style update after every admitted request. The four comparisons are: a frozen `fixed_threshold` calibrated once offline, a frozen `index_based` load cap, a frozen `rl_frozen` load/score blend, and the non-causal `oracle_hindsight` that greedily admits the lowest-violation-probability requests per window subject to the alpha budge... [truncated, 27130 chars total]
```

### [55] TOOL CALL — NotebookEdit · 2026-08-25 19:35:01 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '5dcac23d', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def run_conformal_aci(stream: dict[str, np.ndarray], alpha: float, eta: float, tau0: float, key: str = "composite_score") -> np.ndarray:\n    n = len(stream[key])\n    dec = np.zeros(n, dtype=bool)\n    score = stream[key]\n    wviol = stream["would_violate"]\n    tau = tau0\n    for i in range(n):\n        admit = score[i] <= tau\n        dec[i] = admit\n        if admit:\n            tau += eta * (alpha - float(wviol[i]))\n            if tau < 0.0:\n                tau = 0.0\n            elif tau > 1.0:\n                tau = 1.0\n    return dec\n\n\ndef calibrate_scalar_threshold(cal: dict[str, np.ndarray], key: str, target: float) -> float:\n    lo, hi = 0.0, 1.0\n    sig = cal[key]\n    wviol = cal["would_violate"]\n    for _ in range(30):\n        mid = 0.5 * (lo + hi)\n        admit = sig <= mid\n        if admit.sum() == 0:\n            lo = mid\n            continue\n        rate = wviol[admit].mean()\n        if rate < target:\n            lo = mid\n        else:\n            hi = mid\n    return 0.5 * (lo + hi)\n\n\ndef run_index_based(stream: dict[str, np.ndarray], load_thresh: float) -> np.ndarray:\n    return stream["load"] <= load_thresh\n\n\ndef run_rl_frozen(stream: dict[str, np.ndarray], mean_load: float, std_load: float, k: float) -> np.ndarray:\n    combined = RL_LOAD_WEIGHT * stream["load"] + (1 - RL_LOAD_WEIGHT) * stream["score"]\n    thresh = RL_LOAD_WEIGHT * mean_load + k * std_load\n    return combined <= thresh\n\n\ndef run_oracle_hindsight(stream: dict[str, np.ndarray], alpha: float, window: int) -> np.ndarray:\n    n = len(stream["would_violate"])\n    dec = np.zeros(n, dtype=bool)\n    lab = stream["would_violate"].astype(np.float64)\n    score = stream["score"]\n    for start in range(0, n, window):\n        end = min(start + window, n)\n        idx = np.arange(start, end)\n        order = idx[np.lexsort((score[idx], lab[idx]))]\n        cum = np.cumsum(lab[order])\n        counts = np.arange(1, len(order) + 1)\n        cum_mean = cum / counts\n        k = int(np.sum(cum_mean <= alpha))\n        dec[order[:k]] = True\n    return dec'}
```

### [56] TOOL RESULT — NotebookEdit · 2026-08-25 19:35:01 UTC

```
{"new_source": "def run_conformal_aci(stream: dict[str, np.ndarray], alpha: float, eta: float, tau0: float, key: str = \"composite_score\") -> np.ndarray:\n    n = len(stream[key])\n    dec = np.zeros(n, dtype=bool)\n    score = stream[key]\n    wviol = stream[\"would_violate\"]\n    tau = tau0\n    for i in range(n):\n        admit = score[i] <= tau\n        dec[i] = admit\n        if admit:\n            tau += eta * (alpha - float(wviol[i]))\n            if tau < 0.0... [truncated, 31732 chars total]
```

### [57] ASSISTANT · 2026-08-25 19:35:07 UTC

```
Now rolling stats + bootstrap helpers section:
```

### [58] TOOL CALL — NotebookEdit · 2026-08-25 19:35:07 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': 'c4d8f78f', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Rolling stats over admitted requests, plus bootstrap/Holm helpers\\n\\n`admitted_rolling_rate` computes the rolling violation rate over the *admitted* subsequence only (a rejected request cannot violate its SLO). `mad_and_spike` reduces that trajectory to a single post-burn-in MAD-from-alpha and a max transient spike. `whole_seed_bootstrap_ci` and `holm_bonferroni` are the exact bootstrap/multiple-testing machinery used for the significance tests further down.'}
```

### [59] TOOL RESULT — NotebookEdit · 2026-08-25 19:35:09 UTC

```
{"new_source": "## Rolling stats over admitted requests, plus bootstrap/Holm helpers\\n\\n`admitted_rolling_rate` computes the rolling violation rate over the *admitted* subsequence only (a rejected request cannot violate its SLO). `mad_and_spike` reduces that trajectory to a single post-burn-in MAD-from-alpha and a max transient spike. `whole_seed_bootstrap_ci` and `holm_bonferroni` are the exact bootstrap/multiple-testing machinery used for the significance tests fur... [truncated, 33044 chars total]
```

### [60] TOOL CALL — NotebookEdit · 2026-08-25 19:35:17 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '39f562a2', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def admitted_rolling_rate(dec: np.ndarray, wviol: np.ndarray, window: int) -> np.ndarray:\n    admitted_labels = wviol[dec].astype(np.float64)\n    n = len(admitted_labels)\n    if n == 0:\n        return np.array([])\n    cs = np.cumsum(admitted_labels)\n    win = np.empty(n)\n    win[:window] = cs[:window] / np.arange(1, min(window, n) + 1)\n    if n > window:\n        win[window:] = (cs[window:] - cs[:-window]) / window\n    return win\n\n\ndef mad_and_spike(rate: np.ndarray, burn_in: int) -> tuple[float, float]:\n    post = rate[burn_in:]\n    if len(post) == 0:\n        return float("nan"), float("nan")\n    dev = np.abs(post - ALPHA)\n    return float(dev.mean()), float(dev.max())\n\n\ndef safe_float(x: Any) -> float | None:\n    return None if (x is None or (isinstance(x, float) and np.isnan(x))) else float(x)\n\n\ndef ci95(samples: np.ndarray) -> list[float | None]:\n    samples = np.asarray(samples, dtype=float)\n    samples = samples[~np.isnan(samples)]\n    if len(samples) == 0:\n        return [None, None]\n    return [float(np.percentile(samples, 2.5)), float(np.percentile(samples, 97.5))]\n\n\ndef holm_bonferroni(pvals: list[float]) -> list[float]:\n    order = np.argsort(pvals)\n    m = len(pvals)\n    adj = np.empty(m)\n    running_max = 0.0\n    for rank, idx in enumerate(order):\n        raw = pvals[idx] * (m - rank)\n        running_max = max(running_max, raw)\n        adj[idx] = min(running_max, 1.0)\n    return adj.tolist()\n\n\ndef whole_seed_bootstrap_ci(per_seed_values: list[float], n_boot: int, rng: np.random.Generator) -> tuple[list[float | None], np.ndarray]:\n    vals = np.asarray([v for v in per_seed_values if v is not None and not np.isnan(v)])\n    if len(vals) == 0:\n        return [None, None], np.array([])\n    n = len(vals)\n    picks = rng.integers(0, n, size=(n_boot, n))\n    samples = vals[picks].mean(axis=1)\n    return ci95(samples), samples\n\n\ndef burn_in_for(regime_n_total: int) -> int:\n    return max(BURN_IN_MIN, int(round(BURN_IN_FRAC * regime_n_total)))'}
```

### [61] TOOL RESULT — NotebookEdit · 2026-08-25 19:35:17 UTC

```
{"new_source": "def admitted_rolling_rate(dec: np.ndarray, wviol: np.ndarray, window: int) -> np.ndarray:\n    admitted_labels = wviol[dec].astype(np.float64)\n    n = len(admitted_labels)\n    if n == 0:\n        return np.array([])\n    cs = np.cumsum(admitted_labels)\n    win = np.empty(n)\n    win[:window] = cs[:window] / np.arange(1, min(window, n) + 1)\n    if n > window:\n        win[window:] = (cs[window:] - cs[:-window]) / window\n    return win\n\n\ndef mad_a... [truncated, 37460 chars total]
```

### [62] ASSISTANT · 2026-08-25 19:35:25 UTC

```
Now calibration + simulate + compute_deviation_stats section:
```

### [63] TOOL CALL — NotebookEdit · 2026-08-25 19:35:25 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '26873aff', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Calibrate frozen baselines, then simulate all policies x regimes x seeds\\n\\nAll of `fixed_threshold`, `index_based`, and `rl_frozen` are calibrated ONCE on a held-out slice of the `stationary` regime — they never see the target alpha again after this point, unlike `conformal_aci`, which keeps adapting online. Then every policy is run over every regime and every bootstrap seed.'}
```

### [64] TOOL RESULT — NotebookEdit · 2026-08-25 19:35:25 UTC

```
{"new_source": "## Calibrate frozen baselines, then simulate all policies x regimes x seeds\\n\\nAll of `fixed_threshold`, `index_based`, and `rl_frozen` are calibrated ONCE on a held-out slice of the `stationary` regime — they never see the target alpha again after this point, unlike `conformal_aci`, which keeps adapting online. Then every policy is run over every regime and every bootstrap seed.", "cell_type": "markdown", "language": "python", "edit_mode": "insert", ... [truncated, 38574 chars total]
```

### [65] TOOL CALL — NotebookEdit · 2026-08-25 19:35:41 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '87d80d33', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def calibrate_all(regime_arrays: dict[str, dict[str, np.ndarray]], global_median_inv_slo: float) -> dict[str, Any]:\n    n = len(regime_arrays["stationary"]["label"])\n    rng = np.random.default_rng(CALIB_SEED)\n    cal_idx = rng.choice(n, size=min(20_000, n), replace=False)\n    cal_order = np.argsort(regime_arrays["stationary"]["arrival_time"][cal_idx], kind="stable")\n    cal_idx = cal_idx[cal_order]\n    cal = {\n        "arrival_time": regime_arrays["stationary"]["arrival_time"][cal_idx],\n        "score": regime_arrays["stationary"]["risk_score"][cal_idx],\n        "would_violate": regime_arrays["stationary"]["label"][cal_idx],\n        "value": value_proxy(regime_arrays["stationary"]["slo_target"][cal_idx], regime_arrays["stationary"]["risk_score"][cal_idx], global_median_inv_slo),\n    }\n    cal["load"] = local_load_proxy(cal["arrival_time"])\n    cal["composite_score"] = 0.5 * cal["score"] + 0.5 * cal["load"]\n\n    tau0_fixed = calibrate_scalar_threshold(cal, "composite_score", ALPHA)\n    load_thresh_index = float(np.percentile(cal["load"], 70.0))  # frozen operational cap, NOT alpha-calibrated (misspecified by design)\n\n    mean_load = float(cal["load"].mean())\n    std_load = float(cal["load"].std()) or 1e-6\n    best_k, best_diff = 0.0, np.inf\n    for k in np.linspace(-6.0, 6.0, 481):\n        dec = run_rl_frozen(cal, mean_load, std_load, k)\n        if dec.sum() == 0:\n            continue\n        rate = cal["would_violate"][dec].mean()\n        diff = abs(rate - ALPHA)\n        if diff < best_diff:\n            best_diff, best_k = diff, k\n\n    logger.info(f"Calibrated on stationary(fold-mixed, n={len(cal_idx)}): tau0={tau0_fixed:.4f} load_thresh={load_thresh_index:.4f} rl_k={best_k:.3f}")\n    return {\n        "tau0_fixed": float(tau0_fixed),\n        "load_thresh_index": float(load_thresh_index),\n        "rl_k": float(best_k),\n        "mean_load_stationary": mean_load,\n        "std_load_stationary": std_load,\n        "n_calibration_rows": int(len(cal_idx)),\n    }\n\n\ndef simulate_policy_decisions(\n    regime_arrays: dict[str, dict[str, np.ndarray]],\n    calib: dict[str, Any],\n    global_median_inv_slo: float,\n    eta: float,\n) -> dict[str, dict[str, dict[int, dict[str, np.ndarray]]]]:\n    """logs[policy][regime][seed] -> {decision, would_violate, value, function_id}"""\n    logs: dict[str, dict[str, dict[int, dict[str, np.ndarray]]]] = {p: {r: {} for r in REGIMES} for p in ALL_POLICIES}\n    t0 = time.time()\n    for regime in REGIMES:\n        for seed in range(N_SEEDS):\n            stream = make_seeded_trace(regime_arrays[regime], seed, global_median_inv_slo)\n            dec_conf = run_conformal_aci(stream, ALPHA, eta, calib["tau0_fixed"])\n            dec_fixed = stream["composite_score"] <= calib["tau0_fixed"]\n            dec_index = run_index_based(stream, calib["load_thresh_index"])\n            dec_rl = run_rl_frozen(stream, calib["mean_load_stationary"], calib["std_load_stationary"], calib["rl_k"])\n            dec_oracle = run_oracle_hindsight(stream, ALPHA, WINDOW)\n            for pname, dec in [\n                ("conformal_aci", dec_conf),\n                ("fixed_threshold", dec_fixed),\n                ("index_based", dec_index),\n                ("rl_frozen", dec_rl),\n                ("oracle_hindsight", dec_oracle),\n            ]:\n                logs[pname][regime][seed] = {\n                    "decision": dec,\n                    "would_violate": stream["would_violate"],\n                    "value": stream["value"],\n                    "function_id": stream["function_id"],\n                }\n        logger.info(f"[eta={eta}] simulated regime={regime} for {N_SEEDS} seeds x {len(ALL_POLICIES)} policies ({time.time()-t0:.1f}s elapsed)")\n    return logs\n\n\nall_slo = np.concatenate([regime_arrays[r]["slo_target"] for r in REGIMES])\nglobal_median_inv_slo = float(np.median(1.0 / all_slo))\nboot_rng = np.random.default_rng(2026)\ncalib = calibrate_all(regime_arrays, global_median_inv_slo)\nlogs_primary = simulate_policy_decisions(regime_arrays, calib, global_median_inv_slo, ETA_PRIMARY)'}
```

### [66] TOOL RESULT — NotebookEdit · 2026-08-25 19:35:41 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [67] ASSISTANT · 2026-08-25 19:35:49 UTC

```
Now compute_deviation_stats and paired significance:
```

### [68] TOOL CALL — NotebookEdit · 2026-08-25 19:35:49 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '26d6f0de', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Per (policy, regime) deviation stats, plus Holm-corrected paired significance\\n\\nFor every `(policy, regime)` cell: average the rolling-rate trajectory across seeds, reduce to a post-burn-in MAD point estimate + bootstrap 95% CI, and flag pass/fail against the `TOL_PP` tolerance. Then, for each `(regime, baseline)` pair, bootstrap the paired MAD difference (`baseline - conformal`) across seeds and Holm-Bonferroni-correct the resulting p-values across all pairs.'}
```

### [69] TOOL RESULT — NotebookEdit · 2026-08-25 19:35:49 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [70] TOOL CALL — NotebookEdit · 2026-08-25 19:36:09 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '9d83b092', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def compute_deviation_stats(\n    logs: dict[str, Any], regime_arrays: dict[str, dict[str, np.ndarray]], boot_rng: np.random.Generator\n) -> tuple[dict[str, Any], dict[str, dict[str, np.ndarray]]]:\n    per_policy_regime: dict[str, dict[str, Any]] = {p: {} for p in ALL_POLICIES}\n    rolling_series_for_plots: dict[str, dict[str, np.ndarray]] = {}\n\n    for regime in REGIMES:\n        rolling_series_for_plots[regime] = {}\n        n_total = len(regime_arrays[regime]["label"])\n        burn_in = burn_in_for(n_total)\n        for pname in ALL_POLICIES:\n            per_seed_mad, per_seed_spike, per_seed_admits = [], [], []\n            rates_by_seed = []\n            for seed in range(N_SEEDS):\n                rec = logs[pname][regime][seed]\n                rate = admitted_rolling_rate(rec["decision"], rec["would_violate"], WINDOW)\n                rates_by_seed.append(rate)\n                bi = min(burn_in, max(len(rate) - 1, 0))\n                m, s = mad_and_spike(rate, bi)\n                per_seed_mad.append(m)\n                per_seed_spike.append(s)\n                per_seed_admits.append(int(rec["decision"].sum()))\n            maxlen = max((len(r) for r in rates_by_seed), default=0)\n            if maxlen > 0:\n                padded = np.full((N_SEEDS, maxlen), np.nan)\n                for si, r in enumerate(rates_by_seed):\n                    padded[si, : len(r)] = r\n                with np.errstate(invalid="ignore"):\n                    rolling_series_for_plots[regime][pname] = np.nanmean(padded, axis=0)\n            else:\n                rolling_series_for_plots[regime][pname] = np.array([])\n\n            mad_ci, mad_samples = whole_seed_bootstrap_ci(per_seed_mad, N_BOOTSTRAP, boot_rng)\n            spike_ci, spike_samples = whole_seed_bootstrap_ci(per_seed_spike, N_BOOTSTRAP, boot_rng)\n            mad_valid = [m for m in per_seed_mad if not np.isnan(m)]\n            mad_point = float(np.mean(mad_valid)) if mad_valid else float("nan")\n            spike_valid = [s for s in per_seed_spike if not np.isnan(s)]\n            spike_point = float(np.max(spike_valid)) if spike_valid else float("nan")\n            insufficient = bool(sum(per_seed_admits) < WINDOW // 2)\n\n            entry = {\n                "mad_point": safe_float(mad_point),\n                "mad_ci95": mad_ci,\n                "max_spike_point": safe_float(spike_point),\n                "max_spike_ci95": spike_ci,\n                "n_seeds": N_SEEDS,\n                "total_admits_across_seeds": int(sum(per_seed_admits)),\n                "per_seed_admits": per_seed_admits,\n                "burn_in_admitted_requests": burn_in,\n                "insufficient_admissions": insufficient,\n                "bootstrap_method": "over_seed_resample_with_replacement",\n                "n_bootstrap": N_BOOTSTRAP,\n                "tolerance_pass_3pp": bool((not insufficient) and (not np.isnan(mad_point)) and mad_point <= TOL_PP),\n            }\n            if regime == "regime_switch":\n                switch_idx_full = estimate_switch_index(regime_arrays[regime]["function_id"])\n                entry["estimated_switch_index_in_full_trace"] = int(switch_idx_full)\n            per_policy_regime[pname][regime] = entry\n            gc.collect()\n        logger.info(f"[regime={regime}] deviation stats done for {len(ALL_POLICIES)} policies (burn_in={burn_in})")\n    return per_policy_regime, rolling_series_for_plots\n\n\ndef compute_paired_significance(logs: dict[str, Any], regime_arrays: dict[str, Any], boot_rng: np.random.Generator) -> list[dict[str, Any]]:\n    pair_records = []\n    for regime in REGIMES:\n        n_total = len(regime_arrays[regime]["label"])\n        burn_in = burn_in_for(n_total)\n        for baseline in BASELINES:\n            mad_c_seed, mad_b_seed = [], []\n            for seed in range(N_SEEDS):\n                rc = logs["conformal_aci"][regime][seed]\n                rb = logs[baseline][regime][seed]\n                rate_c = admitted_rolling_rate(rc["decision"], rc["would_violate"], WINDOW)\n                rate_b = admitted_rolling_rate(rb["decision"], rb["would_violate"], WINDOW)\n                bi_c = min(burn_in, max(len(rate_c) - 1, 0))\n                bi_b = min(burn_in, max(len(rate_b) - 1, 0))\n                m_c, _ = mad_and_spike(rate_c, bi_c)\n                m_b, _ = mad_and_spike(rate_b, bi_b)\n                mad_c_seed.append(m_c)\n                mad_b_seed.append(m_b)\n            paired_diff = np.array(\n                [b - c for b, c in zip(mad_b_seed, mad_c_seed) if not (np.isnan(b) or np.isnan(c))]\n            )  # >0 => baseline deviates more => conformal better\n            insufficient_pair = len(paired_diff) < 3\n            if insufficient_pair:\n                pair_records.append(\n                    {"regime": regime, "baseline": baseline, "paired_diff_ci95": [None, None], "p_boot": None, "insufficient_admissions": True}\n                )\n                continue\n            n = len(paired_diff)\n            picks = boot_rng.integers(0, n, size=(N_BOOTSTRAP, n))\n            boot_means = paired_diff[picks].mean(axis=1)\n            lo, hi = ci95(boot_means)\n            p_boot = float(2 * min((boot_means <= 0).mean(), (boot_means >= 0).mean()))\n            pair_records.append(\n                {\n                    "regime": regime,\n                    "baseline": baseline,\n                    "paired_diff_ci95": [lo, hi],\n                    "p_boot": p_boot,\n                    "insufficient_admissions": False,\n                    "n_seed_pairs": int(n),\n                }\n            )\n            del picks, boot_means\n            gc.collect()\n    holm_pvals = [r["p_boot"] if r["p_boot"] is not None else 1.0 for r in pair_records]\n    holm_adj = holm_bonferroni(holm_pvals)\n    for r, p_adj in zip(pair_records, holm_adj):\n        r["p_holm"] = None if r["p_boot"] is None else p_adj\n        r["conformal_significantly_better"] = bool(\n            (not r.get("insufficient_admissions", False))\n            and r["paired_diff_ci95"][0] is not None\n            and r["paired_diff_ci95"][0] > 0\n            and r["p_holm"] is not None\n            and r["p_holm"] < 0.05\n        )\n    logger.info(f"Paired significance tests: {len(pair_records)} (regime x baseline), Holm-corrected, over-seed resample")\n    return pair_records\n\n\nper_policy_regime, rolling_series = compute_deviation_stats(logs_primary, regime_arrays, boot_rng)\npair_records = compute_paired_significance(logs_primary, regime_arrays, boot_rng)'}
```

### [71] TOOL RESULT — NotebookEdit · 2026-08-25 19:36:10 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [72] ASSISTANT · 2026-08-25 19:36:17 UTC

```
Now matched-value/knapsack + eta sensitivity + plots + final results sections:
```

### [73] TOOL CALL — NotebookEdit · 2026-08-25 19:36:17 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': 'c4eed057', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': "## Matched-violation-rate value comparison, and knapsack-vs-FCFS\\n\\nTo compare *value*, not just violation rate, each baseline is re-thresholded to match conformal-ACI's realized violation rate on `stationary`, then the total admitted `value` is compared. Separately, a value-aware knapsack admission rule is compared against plain FCFS among conformal-eligible requests on `regime_switch` (chosen over `stationary` because `stationary` here is dominated by a single `function_id`, making the value proxy degenerate there)."}
```

### [74] TOOL RESULT — NotebookEdit · 2026-08-25 19:36:17 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [75] TOOL CALL — NotebookEdit · 2026-08-25 19:36:41 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': 'b80e1a6e', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def rethreshold_scalar(stream: dict[str, np.ndarray], key: str, target: float) -> tuple[float, np.ndarray]:\n    tau = calibrate_scalar_threshold(stream, key, target)\n    return tau, (stream[key] <= tau)\n\n\ndef rethreshold_rl(stream: dict[str, np.ndarray], mean_load: float, std_load: float, target: float) -> tuple[float, np.ndarray]:\n    best_k, best_diff, best_dec = 0.0, np.inf, np.zeros(len(stream["composite_score"]), dtype=bool)\n    for k in np.linspace(-6.0, 6.0, 241):\n        dec = run_rl_frozen(stream, mean_load, std_load, k)\n        if dec.sum() == 0:\n            continue\n        diff = abs(stream["would_violate"][dec].mean() - target)\n        if diff < best_diff:\n            best_diff, best_k, best_dec = diff, k, dec\n    return best_k, best_dec\n\n\ndef matched_value_and_knapsack(\n    regime_arrays: dict[str, Any], calib: dict[str, Any], logs_primary: dict[str, Any], global_median_inv_slo: float, boot_rng: np.random.Generator\n) -> tuple[dict[str, Any], dict[str, Any]]:\n    seed0 = 0\n    stream = make_seeded_trace(regime_arrays["stationary"], seed0, global_median_inv_slo)\n    dec_conf = logs_primary["conformal_aci"]["stationary"][seed0]["decision"]\n    conf_rate = float(stream["would_violate"][dec_conf].sum() / max(dec_conf.sum(), 1))\n    total_value_conformal = float(stream["value"][dec_conf].sum())\n\n    value_gap: dict[str, Any] = {}\n    for baseline in BASELINES + ["oracle_hindsight"]:\n        if baseline == "fixed_threshold":\n            tau, dec_matched = rethreshold_scalar(stream, "composite_score", conf_rate)\n            method = f"bisection re-threshold on composite_score; tau={tau:.4f}"\n        elif baseline == "index_based":\n            tau, dec_matched = rethreshold_scalar(stream, "load", conf_rate)\n            method = f"bisection re-threshold on load proxy; tau={tau:.4f}"\n        elif baseline == "rl_frozen":\n            k, dec_matched = rethreshold_rl(stream, calib["mean_load_stationary"], calib["std_load_stationary"], conf_rate)\n            method = f"bisection re-search over frozen boundary width k; k={k:.4f}"\n        else:\n            dec_matched = logs_primary["oracle_hindsight"]["stationary"][seed0]["decision"]\n            method = "hindsight-optimal oracle already targets alpha per window by construction"\n\n        total_value_matched = float(stream["value"][dec_matched].sum())\n        realized_rate_matched = float(stream["would_violate"][dec_matched].sum() / max(dec_matched.sum(), 1))\n        gap_pct = (total_value_matched - total_value_conformal) / total_value_matched * 100 if total_value_matched > 0 else float("nan")\n\n        n = len(stream["value"])\n        picks = boot_rng.integers(0, n, size=(N_BOOTSTRAP, min(n, 20_000)))\n        val_conf = stream["value"] * dec_conf.astype(float)\n        val_match = stream["value"] * dec_matched.astype(float)\n        tv_conf = val_conf[picks].sum(axis=1) * (n / picks.shape[1])\n        tv_match = val_match[picks].sum(axis=1) * (n / picks.shape[1])\n        with np.errstate(invalid="ignore", divide="ignore"):\n            gap_samples = np.where(tv_match > 0, (tv_match - tv_conf) / tv_match * 100, np.nan)\n        gap_ci = ci95(gap_samples)\n        degenerate = bool(total_value_matched < 0.05 * total_value_conformal)\n\n        value_gap[baseline] = {\n            "rethreshold_method": method,\n            "target_violation_rate_matched_pct": round(conf_rate * 100, 3),\n            "realized_violation_rate_matched_pct": round(realized_rate_matched * 100, 3),\n            "total_value_conformal": total_value_conformal,\n            "total_value_baseline_matched": total_value_matched,\n            "value_gap_pct": safe_float(gap_pct),\n            "value_gap_pct_ci95": gap_ci,\n            "degenerate_matched_denominator": degenerate,\n            "disconfirmed_over_50pct_loss": bool(\n                (not degenerate) and (not np.isnan(gap_pct)) and gap_pct > 50 and gap_ci[0] is not None and gap_ci[0] > 50\n            ),\n        }\n        del picks, tv_conf, tv_match\n        gc.collect()\n    logger.info("Matched-violation-rate value comparison (stationary) computed for all baselines")\n\n    KNAPSACK_REGIME = "regime_switch"\n    stream_knap = make_seeded_trace(regime_arrays[KNAPSACK_REGIME], 0, global_median_inv_slo)\n    eligible = stream_knap["composite_score"] <= calib["tau0_fixed"]\n    n = len(eligible)\n    dec_fcfs = np.zeros(n, dtype=bool)\n    dec_knap = np.zeros(n, dtype=bool)\n    capacity_frac = 0.55\n    for start in range(0, n, WINDOW):\n        end = min(start + WINDOW, n)\n        idx = np.arange(start, end)\n        elig_idx = idx[eligible[idx]]\n        cap = min(int(round(capacity_frac * len(idx))), len(elig_idx))\n        dec_fcfs[elig_idx[:cap]] = True\n        if cap > 0:\n            order = elig_idx[np.argsort(-stream_knap["value"][elig_idx])]\n            dec_knap[order[:cap]] = True\n\n    rate_fcfs = admitted_rolling_rate(dec_fcfs, stream_knap["would_violate"], WINDOW)\n    rate_knap = admitted_rolling_rate(dec_knap, stream_knap["would_violate"], WINDOW)\n    bi = burn_in_for(n)\n    mad_fcfs, _ = mad_and_spike(rate_fcfs, min(bi, max(len(rate_fcfs) - 1, 0)))\n    mad_knap, _ = mad_and_spike(rate_knap, min(bi, max(len(rate_knap) - 1, 0)))\n\n    picks = boot_rng.integers(0, n, size=(N_BOOTSTRAP, min(n, 20_000)))\n    scale = n / picks.shape[1]\n    wv = stream_knap["would_violate"].astype(float)\n    dec_fcfs_f, dec_knap_f = dec_fcfs.astype(float), dec_knap.astype(float)\n    rate_fcfs_boot = (dec_fcfs_f[picks] * wv[picks]).sum(axis=1) / np.maximum(dec_fcfs_f[picks].sum(axis=1), 1)\n    rate_knap_boot = (dec_knap_f[picks] * wv[picks]).sum(axis=1) / np.maximum(dec_knap_f[picks].sum(axis=1), 1)\n    mad_diff_samples = np.abs(rate_knap_boot - ALPHA) - np.abs(rate_fcfs_boot - ALPHA)\n    mad_diff_ci = ci95(mad_diff_samples)\n\n    val_fcfs = (stream_knap["value"] * dec_fcfs_f)\n    val_knap = (stream_knap["value"] * dec_knap_f)\n    vg_fcfs = val_fcfs[picks].sum(axis=1) * scale\n    vg_knap = val_knap[picks].sum(axis=1) * scale\n    value_gain_ci = ci95(vg_knap - vg_fcfs)\n\n    knapsack_check = {\n        "regime_used": KNAPSACK_REGIME,\n        "capacity_frac": capacity_frac,\n        "mad_fcfs": safe_float(mad_fcfs),\n        "mad_knapsack": safe_float(mad_knap),\n        "mad_diff_ci95_knapsack_minus_fcfs": mad_diff_ci,\n        "guarantee_indistinguishable": bool(mad_diff_ci[0] is not None and mad_diff_ci[0] <= 0 <= mad_diff_ci[1]),\n        "total_value_fcfs": float(val_fcfs.sum()),\n        "total_value_knapsack": float(val_knap.sum()),\n        "value_gain_ci95": value_gain_ci,\n        "value_gain_significant_and_positive": bool(value_gain_ci[0] is not None and value_gain_ci[0] > 0),\n    }\n    logger.info(f"Knapsack vs FCFS: mad_diff_ci={mad_diff_ci}, value_gain_ci={value_gain_ci}")\n    return value_gap, knapsack_check\n\n\nvalue_gap, knapsack_check = matched_value_and_knapsack(regime_arrays, calib, logs_primary, global_median_inv_slo, boot_rng)'}
```

### [76] TOOL RESULT — NotebookEdit · 2026-08-25 19:36:41 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [77] ASSISTANT · 2026-08-25 19:36:49 UTC

```
Now eta sensitivity + verdict + plots + final results/visualization:
```

### [78] TOOL CALL — NotebookEdit · 2026-08-25 19:36:49 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': 'be04af49', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': "## Eta sensitivity\\n\\nSweeps `conformal_aci`'s adaptation rate `eta` over `ETA_GRID` to show the tradeoff between tracking speed (lower MAD) and transient overshoot (max spike), for `stationary`, `regime_switch`, and `adversarial`."}
```

### [79] TOOL RESULT — NotebookEdit · 2026-08-25 19:36:50 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [80] TOOL CALL — NotebookEdit · 2026-08-25 19:36:57 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '0fb87fd2', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def eta_sensitivity(\n    regime_arrays: dict[str, Any], calib: dict[str, Any], global_median_inv_slo: float\n) -> dict[str, Any]:\n    result: dict[str, Any] = {}\n    target_regimes = ["stationary", "regime_switch", "adversarial"]\n    for regime in target_regimes:\n        result[regime] = {}\n        n_total = len(regime_arrays[regime]["label"])\n        burn_in = burn_in_for(n_total)\n        for eta in ETA_GRID:\n            mads, spikes = [], []\n            for seed in range(N_SEEDS):\n                stream = make_seeded_trace(regime_arrays[regime], seed, global_median_inv_slo)\n                dec = run_conformal_aci(stream, ALPHA, eta, calib["tau0_fixed"])\n                rate = admitted_rolling_rate(dec, stream["would_violate"], WINDOW)\n                bi = min(burn_in, max(len(rate) - 1, 0))\n                m, s = mad_and_spike(rate, bi)\n                mads.append(m)\n                spikes.append(s)\n            mads_v = [m for m in mads if not np.isnan(m)]\n            spikes_v = [s for s in spikes if not np.isnan(s)]\n            result[regime][str(eta)] = {\n                "mad_mean_over_seeds": safe_float(np.mean(mads_v)) if mads_v else None,\n                "max_spike_mean_over_seeds": safe_float(np.mean(spikes_v)) if spikes_v else None,\n            }\n        logger.info(f"Eta sensitivity done for regime={regime}")\n    return result\n\n\neta_sens = eta_sensitivity(regime_arrays, calib, global_median_inv_slo)'}
```

### [81] TOOL RESULT — NotebookEdit · 2026-08-25 19:36:58 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [82] ASSISTANT · 2026-08-25 19:37:04 UTC

```
Now the overall verdict computation:
```

### [83] TOOL CALL — NotebookEdit · 2026-08-25 19:37:04 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '29de0efd', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Overall verdict\\n\\nCombines the tolerance pass/fail flags, the Holm-corrected significant-pairs fraction, and the matched-value disconfirmation check into a single `CONFIRMED` / `PARTIALLY_CONFIRMED` / `DISCONFIRMED` verdict, exactly as the original script does.'}
```

### [84] TOOL RESULT — NotebookEdit · 2026-08-25 19:37:04 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [85] TOOL CALL — NotebookEdit · 2026-08-25 19:37:14 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '5be1cd30', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'tolerance_all_pass = all(per_policy_regime["conformal_aci"][r]["tolerance_pass_3pp"] for r in REGIMES)\nsig_pairs_pass = [r for r in pair_records if r["conformal_significantly_better"]]\nsig_frac = len(sig_pairs_pass) / len(pair_records) if pair_records else 0.0\nany_value_disconfirm = any(v["disconfirmed_over_50pct_loss"] for k, v in value_gap.items() if k in BASELINES)\n\nif tolerance_all_pass and sig_frac >= 0.75 and not any_value_disconfirm:\n    overall_verdict = "CONFIRMED"\n    justification = (\n        f"On the REAL Azure-trace dataset, conformal-ACI\'s MAD stayed within the pre-registered "\n        f"{TOL_PP*100:.0f}pp tolerance of alpha in all {len(REGIMES)} regimes; it was Holm-corrected "\n        f"significantly better than baselines in {len(sig_pairs_pass)}/{len(pair_records)} (regime,baseline) "\n        f"pairs (>=75% threshold); no baseline\'s matched-value gap exceeded the 50% disconfirming threshold."\n    )\nelif not tolerance_all_pass and sig_frac < 0.25:\n    overall_verdict = "DISCONFIRMED"\n    justification = (\n        f"On the real-trace data, conformal-ACI failed the {TOL_PP*100:.0f}pp tolerance criterion in at "\n        f"least one regime AND was Holm-corrected significantly better than baselines in fewer than 25% "\n        f"of pairs ({len(sig_pairs_pass)}/{len(pair_records)})."\n    )\nelif any_value_disconfirm:\n    overall_verdict = "DISCONFIRMED"\n    disconf_names = [k for k, v in value_gap.items() if k in BASELINES and v["disconfirmed_over_50pct_loss"]]\n    justification = f"Matched-violation-rate value comparison shows conformal-ACI losing >50% value vs {disconf_names}, CI lower bound also >50%."\nelse:\n    overall_verdict = "PARTIALLY_CONFIRMED"\n    justification = (\n        f"Tolerance pass across all regimes: {tolerance_all_pass}. Significant-better fraction: {sig_frac:.2f} "\n        f"of {len(pair_records)} pairs. No baseline value comparison crossed the 50% disconfirming threshold."\n    )\n\nlogger.info(f"OVERALL VERDICT: {overall_verdict}")\nlogger.info(justification)'}
```

### [86] TOOL RESULT — NotebookEdit · 2026-08-25 19:37:16 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [87] ASSISTANT · 2026-08-25 19:37:22 UTC

```
Now the final visualization/results cell:
```

### [88] TOOL CALL — NotebookEdit · 2026-08-25 19:37:22 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '3dacf725', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Results\\n\\nA readable summary table of the per-(policy, regime) MAD/spike numbers, plus the rolling violation-rate trajectories and the eta-sensitivity curves — the same two figure types the original script writes to `figures/`.'}
```

### [89] TOOL RESULT — NotebookEdit · 2026-08-25 19:37:22 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [90] TOOL CALL — NotebookEdit · 2026-08-25 19:37:36 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '61612249', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'print(f"OVERALL VERDICT: {overall_verdict}\\n")\nprint(justification, "\\n")\n\nheader = f"{\'policy\':<16}{\'regime\':<15}{\'MAD\':>8}{\'max_spike\':>11}{\'tol_pass_3pp\':>14}"\nprint(header)\nprint("-" * len(header))\nfor pname in ALL_POLICIES:\n    for regime in REGIMES:\n        e = per_policy_regime[pname][regime]\n        mad = "nan" if e["mad_point"] is None else f"{e[\'mad_point\']:.4f}"\n        spike = "nan" if e["max_spike_point"] is None else f"{e[\'max_spike_point\']:.4f}"\n        print(f"{pname:<16}{regime:<15}{mad:>8}{spike:>11}{str(e[\'tolerance_pass_3pp\']):>14}")\n\nprint("\\nHolm-corrected paired significance (conformal_aci vs baseline):")\nfor r in pair_records:\n    p_holm = "n/a" if r["p_holm"] is None else f"{r[\'p_holm\']:.3f}"\n    print(f"  {r[\'regime\']:<15}{r[\'baseline\']:<16} p_holm={p_holm:<8} sig_better={r.get(\'conformal_significantly_better\')}")\n\n# --- Rolling violation-rate trajectories, one panel per regime ---\ncolors = {\n    "conformal_aci": "tab:blue",\n    "fixed_threshold": "tab:orange",\n    "index_based": "tab:green",\n    "rl_frozen": "tab:red",\n    "oracle_hindsight": "tab:gray",\n}\nband = (ALPHA - TOL_PP, ALPHA + TOL_PP)\nfig, axes = plt.subplots(len(REGIMES), 1, figsize=(9, 3.2 * len(REGIMES)))\nfor ax, regime in zip(axes, REGIMES):\n    ax.axhspan(band[0], band[1], color="lightgray", alpha=0.5, label=f"+/-{TOL_PP*100:.0f}pp tolerance band")\n    ax.axhline(ALPHA, color="black", linestyle="--", linewidth=1, label=f"alpha={ALPHA}")\n    for pname in ALL_POLICIES:\n        series = rolling_series[regime][pname]\n        if len(series):\n            ax.plot(series, label=pname, color=colors[pname], linewidth=1.3, alpha=0.9, marker="o", markersize=3)\n    ax.set_xlabel("admitted-request index")\n    ax.set_ylabel("rolling violation rate")\n    ax.set_title(f"regime={regime}")\n    ax.set_ylim(-0.05, 1.05)\nax.legend(loc="upper right", fontsize=7, ncol=2)\nfig.suptitle(f"Rolling SLO-violation rate vs alpha (window={WINDOW} admitted requests, demo scale)")\nfig.tight_layout()\nplt.show()\n\n# --- Eta sensitivity ---\nfig, axes = plt.subplots(1, 2, figsize=(12, 4.5))\nfor regime in eta_sens:\n    etas = sorted(eta_sens[regime].keys(), key=float)\n    mads = [eta_sens[regime][e]["mad_mean_over_seeds"] for e in etas]\n    spikes = [eta_sens[regime][e]["max_spike_mean_over_seeds"] for e in etas]\n    axes[0].plot([float(e) for e in etas], mads, marker="o", label=regime)\n    axes[1].plot([float(e) for e in etas], spikes, marker="o", label=regime)\naxes[0].axhline(TOL_PP, color="red", linestyle=":", label=f"{TOL_PP*100:.0f}pp tolerance")\naxes[0].set_xlabel("eta"); axes[0].set_ylabel("MAD (post burn-in)"); axes[0].set_title("MAD vs eta"); axes[0].legend(fontsize=7)\naxes[1].set_xlabel("eta"); axes[1].set_ylabel("max transient spike"); axes[1].set_title("Max spike vs eta"); axes[1].legend(fontsize=7)\nfig.tight_layout()\nplt.show()'}
```

### [91] TOOL RESULT — NotebookEdit · 2026-08-25 19:37:36 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [92] ASSISTANT · 2026-08-25 19:37:42 UTC

```
Now let's test-run this in the clean env as specified.
```

### [93] TOOL CALL — Bash · 2026-08-25 19:37:42 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && ls -la mini_demo_data.json && /usr/local/bin/python3.12 -m venv .nb_env 2>&1 | tail -5 && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -20
```

### [94] TOOL RESULT — Bash · 2026-08-25 19:39:42 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bxgtul0px", "timedOutAfterMs": 120000, "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [95] ASSISTANT · 2026-08-25 19:39:46 UTC

```
Will wait for it to finish in background.
```

### [96] TOOL CALL — Bash · 2026-08-25 19:39:46 UTC

```
sleep 60; tail -30 /tmp/claude-0/-ai-inventor-aii-data-runs-run-GtJcfaBZUMxZ-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-2-art-k4NZEyG-q-yz/649bcbdc-8608-4486-83ce-026c046b819c/tasks/bxgtul0px.output
```

### [97] TOOL RESULT — Bash [ERROR] · 2026-08-25 19:39:46 UTC

```
Error: Blocked: sleep 60 followed by: tail -30 /tmp/claude-0/-ai-inventor-aii-data-runs-run-GtJcfaBZUMxZ-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-2-art-k4NZEyG-q-yz/649bcbdc-8608-4486-83ce-026c046b819c/tasks/bxgtul0px.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.
```

### [98] TOOL CALL — ToolSearch · 2026-08-25 19:39:48 UTC

```
{'query': 'select:Monitor'}
```

### [99] TOOL RESULT — ToolSearch · 2026-08-25 19:39:48 UTC

```
{"matches": ["Monitor"], "query": "select:Monitor", "total_deferred_tools": 18}
```

### [100] TOOL CALL — Monitor · 2026-08-25 19:39:56 UTC

```
{'description': 'wait for pip install of jupyter/ipykernel to finish', 'command': 'until grep -qE "\\\\$" /tmp/claude-0/-ai-inventor-aii-data-runs-run-GtJcfaBZUMxZ-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-2-art-k4NZEyG-q-yz/649bcbdc-8608-4486-83ce-026c046b819c/tasks/bxgtul0px.output 2>/dev/null; do sleep 3; done; echo DONE; tail -20 /tmp/claude-0/-ai-inventor-aii-data-runs-run-GtJcfaBZUMxZ-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-2-art-k4NZEyG-q-yz/649bcbdc-8608-4486-83ce-026c046b819c/tasks/bxgtul0px.output', 'timeout_ms': 180000, 'persistent': False}
```

### [101] TOOL RESULT — Monitor · 2026-08-25 19:39:56 UTC

```
{"taskId": "bqy0ymhin", "timeoutMs": 180000, "persistent": false}
```

### [102] TOOL CALL — ToolSearch · 2026-08-25 19:40:00 UTC

```
{'query': 'select:TaskOutput,TaskStop'}
```

### [103] TOOL RESULT — ToolSearch · 2026-08-25 19:40:00 UTC

```
{"matches": ["TaskOutput", "TaskStop"], "query": "select:TaskOutput,TaskStop", "total_deferred_tools": 18}
```

### [104] TOOL CALL — TaskOutput · 2026-08-25 19:42:02 UTC

```
{'task_id': 'bxgtul0px', 'block': True, 'timeout': 120000}
```

### [105] TOOL RESULT — TaskOutput · 2026-08-25 19:42:02 UTC

```
{"retrieval_status": "timeout", "task": {"task_id": "bxgtul0px", "task_type": "local_bash", "status": "running", "description": "cd \"/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz\" && ls -la mini_demo_data.json && /usr/local/bin/python3.12 -m venv .nb_env 2>&1 | tail -5 && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -20", "output": "-rw-rw-rw- 1 root root 94552 Aug 25 19:32 mini_demo_data.json\n", "exitCode": null}}
```

### [106] ASSISTANT · 2026-08-25 19:45:08 UTC

```
Still installing. Let's wait longer.
```

### [107] TOOL CALL — TaskOutput · 2026-08-25 19:45:08 UTC

```
{'task_id': 'bxgtul0px', 'block': True, 'timeout': 180000}
```

### [108] TOOL RESULT — TaskOutput · 2026-08-25 19:45:08 UTC

```
{"retrieval_status": "timeout", "task": {"task_id": "bxgtul0px", "task_type": "local_bash", "status": "running", "description": "cd \"/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz\" && ls -la mini_demo_data.json && /usr/local/bin/python3.12 -m venv .nb_env 2>&1 | tail -5 && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -20", "output": "-rw-rw-rw- 1 root root 94552 Aug 25 19:32 mini_demo_data.json\n", "exitCode": null}}
```

### [109] TOOL CALL — TaskOutput · 2026-08-25 19:48:10 UTC

```
{'task_id': 'bxgtul0px', 'block': True, 'timeout': 180000}
```

### [110] TOOL RESULT — TaskOutput · 2026-08-25 19:48:10 UTC

```
{"retrieval_status": "timeout", "task": {"task_id": "bxgtul0px", "task_type": "local_bash", "status": "running", "description": "cd \"/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz\" && ls -la mini_demo_data.json && /usr/local/bin/python3.12 -m venv .nb_env 2>&1 | tail -5 && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -20", "output": "-rw-rw-rw- 1 root root 94552 Aug 25 19:32 mini_demo_data.json\n", "exitCode": null}}
```

### [111] ASSISTANT · 2026-08-25 19:48:14 UTC

```
This is taking unusually long. Let me check if the process is even alive.
```

### [112] TOOL CALL — Bash · 2026-08-25 19:48:14 UTC

```
ps aux | grep -E "pip|venv" | grep -v grep
```

### [113] TOOL RESULT — Bash · 2026-08-25 19:48:14 UTC

```
{"stdout": "root         290  0.0  0.0   4492  3264 ?        Ss   19:37   0:00 /bin/bash -c source /root/.claude/shell-snapshots/snapshot-bash-1787686346181-9c4cj9.sh 2>/dev/null || true && shopt -u extglob 2>/dev/null || true && { \\builtin unalias -- 'unsetenv'; \\builtin unset -f -- 'unsetenv'; } >/dev/null 2>&1 || true && eval 'cd \"/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz\" && ls -la mini_demo_data.json && /usr/local/bin/python3.12 -m venv .nb_env 2>&1 | tail -5 && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -20' < /dev/null && pwd -P >| /tmp/claude-9ecd-cwd\nroot         301  4.4  0.0 101068 96732 ?        S    19:38   0:24 /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/.nb_env/bin/python3.12 .nb_env/bin/pip install -q pip jupyter ipykernel", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [114] ASSISTANT · 2026-08-25 19:50:42 UTC

```
It's alive, just slow. Let's keep waiting.
```

### [115] TOOL CALL — TaskOutput · 2026-08-25 19:50:42 UTC

```
{'task_id': 'bxgtul0px', 'block': True, 'timeout': 300000}
```

### [116] TOOL RESULT — TaskOutput · 2026-08-25 19:50:42 UTC

```
{"retrieval_status": "success", "task": {"task_id": "bxgtul0px", "task_type": "local_bash", "status": "completed", "description": "cd \"/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz\" && ls -la mini_demo_data.json && /usr/local/bin/python3.12 -m venv .nb_env 2>&1 | tail -5 && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -20", "output": "-rw-rw-rw- 1 root root 94552 Aug 25 19:32 mini_demo_data.json\n\n[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: python3.12 -m pip install --upgrade pip\n\n[exited with code 0]\n", "exitCode": 0}}
```

### [117] ASSISTANT · 2026-08-25 19:50:46 UTC

```
Now let's run nbconvert execute in background.
```

### [118] TOOL CALL — Bash · 2026-08-25 19:50:46 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && nohup .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo_test.ipynb > nbrun.log 2>&1 &
echo "PID: $!"
```

### [119] TOOL RESULT — Bash · 2026-08-25 19:50:46 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bdb93h80c", "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [120] TOOL CALL — Bash · 2026-08-25 19:50:50 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && cat nbrun.log 2>&1; ps aux | grep nbconvert | grep -v grep
```

### [121] TOOL RESULT — Bash · 2026-08-25 19:50:50 UTC

```
{"stdout": "root         547  0.0  0.0   4492  1956 ?        S    19:50   0:00 /bin/bash -c source /root/.claude/shell-snapshots/snapshot-bash-1787686346181-9c4cj9.sh 2>/dev/null || true && shopt -u extglob 2>/dev/null || true && { \\builtin unalias -- 'unsetenv'; \\builtin unset -f -- 'unsetenv'; } >/dev/null 2>&1 || true && eval 'cd \"/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz\" && nohup .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo_test.ipynb > nbrun.log 2>&1 & echo \"PID: $!\"' < /dev/null && pwd -P >| /tmp/claude-d308-cwd\nroot         550 13.7  0.0  51268 39648 ?        S    19:50   0:00 /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/.nb_env/bin/python3.12 .nb_env/bin/jupyter-nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo_test.ipynb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [122] ASSISTANT · 2026-08-25 19:50:54 UTC

```
It's actually running. Let's monitor it with a proper Monitor loop watching the process.
```

### [123] TOOL CALL — Monitor · 2026-08-25 19:50:54 UTC

```
{'description': 'wait for nbconvert notebook execution to finish', 'command': 'while pgrep -f "jupyter-nbconvert.*code_demo.ipynb" >/dev/null; do sleep 5; done; echo "PROCESS ENDED"; tail -60 "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/nbrun.log"', 'timeout_ms': 700000, 'persistent': False}
```

### [124] TOOL RESULT — Monitor · 2026-08-25 19:50:54 UTC

```
{"taskId": "b2m23pbzl", "timeoutMs": 700000, "persistent": false}
```

### [125] ASSISTANT · 2026-08-25 19:50:58 UTC

```
While waiting, let me check the mini_demo_data.json size to make sure it's not too large.
```

### [126] TOOL CALL — Bash · 2026-08-25 19:50:58 UTC

```
ls -la "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/mini_demo_data.json"
```

### [127] TOOL RESULT — Bash · 2026-08-25 19:50:58 UTC

```
{"stdout": "-rw-rw-rw- 1 root root 94552 Aug 25 19:32 /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [128] ASSISTANT · 2026-08-25 19:56:02 UTC

```
Good size (~92KB). Now wait for the monitor notification.
```

### [129] TOOL CALL — TaskOutput · 2026-08-25 19:56:02 UTC

```
{'task_id': 'b2m23pbzl', 'block': True, 'timeout': 300000}
```

### [130] TOOL RESULT — TaskOutput · 2026-08-25 19:56:02 UTC

```
{"retrieval_status": "timeout", "task": {"task_id": "b2m23pbzl", "task_type": "local_bash", "status": "running", "description": "wait for nbconvert notebook execution to finish", "output": "Output truncated (0KB total). Full output saved to: /tmp/claude-0/-ai-inventor-aii-data-runs-run-GtJcfaBZUMxZ-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-2-art-k4NZEyG-q-yz/649bcbdc-8608-4486-83ce-026c046b819c/tasks/b2m23pbzl.output", "exitCode": null}}
```

### [131] TOOL CALL — TaskOutput · 2026-08-25 20:02:35 UTC

```
{'task_id': 'b2m23pbzl', 'block': True, 'timeout': 400000}
```

### [132] TOOL RESULT — TaskOutput · 2026-08-25 20:02:35 UTC

```
{"retrieval_status": "success", "task": {"task_id": "b2m23pbzl", "task_type": "local_bash", "status": "killed", "description": "wait for nbconvert notebook execution to finish", "output": "\n[killed]\n", "exitCode": null}}
```

### [133] TOOL CALL — Bash · 2026-08-25 20:02:39 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && ps aux | grep nbconvert | grep -v grep; echo "---log---"; tail -80 nbrun.log; ls -la code_demo_test.ipynb 2>&1
```

### [134] TOOL RESULT — Bash · 2026-08-25 20:02:41 UTC

```
{"stdout": "---log---\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 65390 bytes to code_demo_test.ipynb\n-rw-rw-rw- 1 root root 65408 Aug 25 19:55 code_demo_test.ipynb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [135] ASSISTANT · 2026-08-25 20:02:45 UTC

```
It completed successfully. Let's inspect the executed notebook for errors and outputs.
```

### [136] TOOL CALL — Bash · 2026-08-25 20:02:45 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && python3 -c "
import json
nb = json.load(open('code_demo_test.ipynb'))
for i, c in enumerate(nb['cells']):
    if c['cell_type'] != 'code': continue
    for o in c.get('outputs', []):
        if o.get('output_type') == 'error':
            print('ERROR in cell', i)
            print('\n'.join(o.get('traceback', [])))
print('done scanning')
"
```

### [137] TOOL RESULT — Bash · 2026-08-25 20:02:45 UTC

```
{"stdout": "done scanning", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [138] ASSISTANT · 2026-08-25 20:02:49 UTC

```
No errors. Let's peek at the final results output to sanity-check.
```

### [139] TOOL CALL — Bash · 2026-08-25 20:02:49 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && python3 -c "
import json
nb = json.load(open('code_demo_test.ipynb'))
for c in nb['cells']:
    if c['cell_type']!='code': continue
    src = ''.join(c['source'])
    if 'OVERALL VERDICT' in src and 'print(' in src:
        for o in c.get('outputs', []):
            if 'text' in o:
                print(''.join(o['text'])[:2000])
"
```

### [140] TOOL RESULT — Bash · 2026-08-25 20:02:49 UTC

```
{"stdout": "OVERALL VERDICT: DISCONFIRMED\n\nOn the real-trace data, conformal-ACI failed the 3pp tolerance criterion in at least one regime AND was Holm-corrected significantly better than baselines in fewer than 25% of pairs (0/15). \n\npolicy          regime              MAD  max_spike  tol_pass_3pp\n----------------------------------------------------------------\nconformal_aci   stationary       0.1000     0.1000         False\nconformal_aci   burst            0.1000     0.1000         False\nconformal_aci   drift            0.1256     0.5000         False\nconformal_aci   regime_switch    0.1395     0.9000         False\nconformal_aci   adversarial      0.1000     0.1000         False\nfixed_threshold stationary       0.1000     0.1000         False\nfixed_threshold burst            0.1000     0.1000         False\nfixed_threshold drift            0.1256     0.5000         False\nfixed_threshold regime_switch    0.1395     0.9000         False\nfixed_threshold adversarial      0.1000     0.1000         False\nindex_based     stationary       0.1000     0.1000         False\nindex_based     burst            0.1000     0.1000         False\nindex_based     drift            0.1178     0.3000         False\nindex_based     regime_switch    0.1561     0.9000         False\nindex_based     adversarial      0.1000     0.1000         False\nrl_frozen       stationary       0.1000     0.1000         False\nrl_frozen       burst               nan        nan         False\nrl_frozen       drift            0.1000     0.1000         False\nrl_frozen       regime_switch       nan        nan         False\nrl_frozen       adversarial         nan        nan         False\noracle_hindsightstationary       0.1000     0.1000         False\noracle_hindsightburst            0.1000     0.1000         False\noracle_hindsightdrift            0.1000     0.1000         False\noracle_hindsightregime_switch    0.1000     0.1000         False\noracle_hindsightadversarial      0.1000     0.1000         False\n\nHolm-corrected paired", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [141] TOOL CALL — Read · 2026-08-25 20:02:59 UTC

```
/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb
```

### [142] TOOL RESULT — Read · 2026-08-25 20:02:59 UTC

```
{"type": "notebook", "file": {"filePath": "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb", "cells": [{"cellType": "markdown", "source": "# Real-Trace Verdict for Admission Control\\n\\nThis notebook is a runnable demo of `eval.py`, which computes a pre-registered statistical verdict for **conformal admission control (ACI)** against four baseline admission policies, evaluated on **real Az... [truncated, 44526 chars total]
```

### [143] ASSISTANT · 2026-08-25 20:03:09 UTC

```
The notebook runs cleanly end-to-end already. Let's do one scaling round: bump N_SEEDS to 5 and N_BOOTSTRAP to 1000 (cheap since data is tiny), matching original spec closer.
```

### [144] TOOL CALL — NotebookEdit · 2026-08-25 20:03:09 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': '8d51313a', 'new_source': 'ALPHA = 0.10\nWINDOW = 5           # rolling window, in ADMITTED requests (original: 500)\nBURN_IN_MIN = 2      # (original: 500)\nBURN_IN_FRAC = 0.05\nTOL_PP = 0.03\nN_SEEDS = 5          # >=5 required for a genuine over-seed bootstrap (matches original spec)\nN_BOOTSTRAP = 1000   # whole-seed resample draws (original: 10_000)\nCALIB_SEED = 777\nREGIMES = ["stationary", "burst", "drift", "regime_switch", "adversarial"]\nBASELINES = ["fixed_threshold", "index_based", "rl_frozen"]\nALL_POLICIES = ["conformal_aci"] + BASELINES + ["oracle_hindsight"]\nRL_LOAD_WEIGHT = 0.6\nETA_GRID = [0.01, 0.02, 0.05, 0.10, 0.20]  # full original grid (cheap at this data scale)\nETA_PRIMARY = 0.05\nLOAD_WINDOW = 5      # requests, for the local-arrival-rate load proxy (original: 50)\nRNG_GLOBAL = np.random.default_rng(20260825)'}
```

### [145] TOOL RESULT — NotebookEdit · 2026-08-25 20:03:09 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [146] ASSISTANT · 2026-08-25 20:03:17 UTC

```
Also update the config markdown reference to ETA_GRID subset text since now it's full grid:
```

### [147] TOOL CALL — NotebookEdit · 2026-08-25 20:03:17 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/code_demo.ipynb', 'cell_id': 'a5404677', 'new_source': "## Config\\n\\nAll tunable parameters from the original `eval.py`, collected in one place. `WINDOW`, `BURN_IN_MIN`, and `LOAD_WINDOW` are shrunk to the **minimum that still produces meaningful output** on this notebook's 100-row (20 per regime) demo subset — the original full-scale values (`WINDOW=500`, `BURN_IN_MIN=500`, `LOAD_WINDOW=50`) are commented alongside each line for reference and are what the real 210,000-row run used. `N_SEEDS`, `N_BOOTSTRAP`, and `ETA_GRID` are cheap regardless of data size, so they are kept at (or close to) their original values."}
```

### [148] TOOL RESULT — NotebookEdit · 2026-08-25 20:03:17 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [149] ASSISTANT · 2026-08-25 20:03:23 UTC

```
Now re-run the test.
```

### [150] TOOL CALL — Bash · 2026-08-25 20:03:23 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && nohup .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo_test.ipynb > nbrun2.log 2>&1 &
echo started
```

### [151] TOOL RESULT — Bash · 2026-08-25 20:03:23 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "btlcmuxav", "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [152] TOOL CALL — Monitor · 2026-08-25 20:03:29 UTC

```
{'description': 'wait for second nbconvert execution round to finish', 'command': 'while pgrep -f "jupyter-nbconvert.*code_demo.ipynb" >/dev/null; do sleep 5; done; echo "PROCESS ENDED"; tail -20 "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz/nbrun2.log"', 'timeout_ms': 300000, 'persistent': False}
```

### [153] TOOL RESULT — Monitor · 2026-08-25 20:03:29 UTC

```
{"taskId": "bnwlyc85a", "timeoutMs": 300000, "persistent": false}
```

### [154] TOOL CALL — TaskOutput · 2026-08-25 20:08:29 UTC

```
{'task_id': 'bnwlyc85a', 'block': True, 'timeout': 300000}
```

### [155] TOOL RESULT — TaskOutput · 2026-08-25 20:08:29 UTC

```
{"retrieval_status": "success", "task": {"task_id": "bnwlyc85a", "task_type": "local_bash", "status": "killed", "description": "wait for second nbconvert execution round to finish", "output": "\n[killed]\n", "exitCode": null}}
```

### [156] TOOL CALL — Bash · 2026-08-25 20:08:33 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && ps aux | grep nbconvert | grep -v grep; echo "---"; cat nbrun2.log; ls -la code_demo_test.ipynb
```

### [157] TOOL RESULT — Bash · 2026-08-25 20:08:33 UTC

```
{"stdout": "---\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 65539 bytes to code_demo_test.ipynb\n-rw-rw-rw- 1 root root 65557 Aug 25 20:04 code_demo_test.ipynb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [158] ASSISTANT · 2026-08-25 20:08:37 UTC

```
Completed successfully. Let's check for errors and confirm.
```

### [159] TOOL CALL — Bash · 2026-08-25 20:08:37 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && python3 -c "
import json
nb = json.load(open('code_demo_test.ipynb'))
errs=0
for i, c in enumerate(nb['cells']):
    if c['cell_type'] != 'code': continue
    for o in c.get('outputs', []):
        if o.get('output_type') == 'error':
            errs+=1
            print('ERROR in cell', i)
            print('\n'.join(o.get('traceback', [])))
print('errors:', errs)
" 
rm -rf .nb_env code_demo_test.ipynb nbrun.log nbrun2.log
ls -la
```

### [160] TOOL RESULT — Bash · 2026-08-25 20:09:37 UTC

```
{"stdout": "errors: 0\ntotal 5554\ndrwxrwxrwx 2 root root 2000160 Aug 25 20:09 .\ndrwxrwxrwx 4 root root 2000272 Aug 25 19:30 ..\n-rw-rw-rw- 1 root root 1545634 Aug 25 20:09 .repl_agent.ptylog\n-rw-rw-rw- 1 root root   45893 Aug 25 20:03 code_demo.ipynb\n-rw-rw-rw- 1 root root   94552 Aug 25 19:32 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [161] ASSISTANT · 2026-08-25 20:09:43 UTC

```
No errors, cleaned up test env. Now verify the final requirements and write the struct output JSON.
```

### [162] TOOL CALL — Bash · 2026-08-25 20:09:43 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && grep -c "GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\"" code_demo.ipynb
python3 -c "import json; json.load(open('mini_demo_data.json')); print('mini json OK')"
cat > .terminal_claude_agent_struct_out.json << 'EOF'
{
  "out_expected_files": {
    "notebook": "code_demo.ipynb",
    "mini_data_file": "mini_demo_data.json"
  }
}
EOF
cat .terminal_claude_agent_struct_out.json
```

### [163] TOOL RESULT — Bash · 2026-08-25 20:09:43 UTC

```
{"stdout": "0\nmini json OK\n{\n  \"out_expected_files\": {\n    \"notebook\": \"code_demo.ipynb\",\n    \"mini_data_file\": \"mini_demo_data.json\"\n  }\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [164] TOOL CALL — Bash · 2026-08-25 20:09:47 UTC

```
cd "/ai-inventor/aii_data/runs/run_GtJcfaBZUMxZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_k4NZEyG_q_yz" && grep -o "GITHUB_DATA_URL[^,]*" code_demo.ipynb | head -1
```

### [165] TOOL RESULT — Bash · 2026-08-25 20:09:47 UTC

```
{"stdout": "GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-db8806-conformal-admission-control-distribution/main/round-2/evaluation-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [166] ASSISTANT · 2026-08-25 20:09:50 UTC

```
Good, it's present (my earlier grep had unescaped quotes issue). All verification checks pass: notebook exists, uses GitHub URL with local fallback, mini_demo_data.json exists and is valid JSON, notebook executes with 0 errors. Task complete.

The notebook (`code_demo.ipynb`) and curated data (`mini_demo_data.json`, 100 rows across all 5 regimes) are done and verified — it test-ran cleanly in a fresh Colab-like environment with zero errors, using the original `eval.py` code split into annotated cells with only config values shrunk (window/burn-in/load-window) to fit the small demo data.
```
