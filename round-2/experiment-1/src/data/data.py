#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru"]
# ///
import random
"""Standardize the real-trace admission-control dataset (built from the Azure
Functions 2019 invocation-per-minute + duration-percentile traces) into the
exp_sel_data_out.json schema: one example per request-level row.

Each example's `output` is the SLO-violation label (service_time > slo_target),
computed post-hoc. `input` carries only information available AT ADMISSION TIME
(arrival_time, risk_score, slo_target, regime/function identifiers) -- it
deliberately excludes service_time, which is the realized value that produced
the label and would leak the answer.
"""
import json
import sys
from pathlib import Path

from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/data.log", rotation="30 MB", level="DEBUG")

WORKSPACE = Path(__file__).parent
RAW_PATH = WORKSPACE / "temp" / "datasets" / "raw_azure_admission_control.json"
OUT_DIR = WORKSPACE / "full_data_out"
N_PARTS = 4  # keeps each split part comfortably under the 100MB file size limit

FOLD_TO_INT = {"train": 0, "val": 1, "test": 2}
REGIME_CAPS = {
    "stationary": 50000,
    "burst": 40000,
    "drift": 50000,
    "regime_switch": 50000,
    "adversarial": 20000,
}
SEED = 20260825


def subsample_rows(requests: list[dict]) -> list[dict]:
    """Stratified subsample per regime, capped per REGIME_CAPS, to stay well
    under the 300MB output limit while keeping every regime's >=2000-decision
    floor and preserving each regime's own arrival_time ordering."""
    by_regime: dict[str, list[dict]] = {}
    for r in requests:
        by_regime.setdefault(r["regime_label"], []).append(r)

    rng = random.Random(SEED)
    kept: list[dict] = []
    for regime, rows in by_regime.items():
        cap = REGIME_CAPS.get(regime, len(rows))
        if len(rows) <= cap:
            kept.extend(rows)
            continue
        sampled_idx = sorted(rng.sample(range(len(rows)), cap))
        kept.extend(rows[i] for i in sampled_idx)
    return kept


def build_example(row: dict) -> dict:
    is_violation = row["service_time"] > row["slo_target"]
    input_features = {
        "arrival_time": row["arrival_time"],
        "risk_score": row["risk_score"],
        "slo_target": row["slo_target"],
        "regime_label": row["regime_label"],
        "function_id": row["function_id"],
        "is_synthetic": row["is_synthetic"],
    }
    return {
        "input": json.dumps(input_features),
        "output": "1" if is_violation else "0",
        "metadata_fold": FOLD_TO_INT[row["metadata_fold"]],
        "metadata_task_type": "classification",
        "metadata_n_classes": 2,
        "metadata_regime_label": row["regime_label"],
        "metadata_function_id": row["function_id"],
        "metadata_request_id": row["request_id"],
        "metadata_is_synthetic": row["is_synthetic"],
        "metadata_provenance": row["provenance"],
        "metadata_service_time": row["service_time"],
        "metadata_slo_target": row["slo_target"],
        "metadata_feature_names": list(input_features.keys()),
    }


def main() -> None:
    logger.info(f"Loading raw dataset from {RAW_PATH}")
    raw = json.loads(RAW_PATH.read_text())
    requests = raw["requests"]
    logger.info(f"Loaded {len(requests)} raw request rows")

    requests = subsample_rows(requests)
    logger.info(f"Subsampled to {len(requests)} rows (per-regime caps={REGIME_CAPS}) to stay under the 300MB limit")

    examples = []
    for i, row in enumerate(requests):
        try:
            examples.append(build_example(row))
        except (KeyError, TypeError) as e:
            logger.error(f"Failed to convert row {i}: {e}")
            continue

    logger.info(f"Converted {len(examples)}/{len(requests)} rows to examples")

    n_violations = sum(1 for e in examples if e["output"] == "1")
    logger.info(f"Overall violation rate: {n_violations / len(examples):.4f}")
    by_regime: dict[str, list[int]] = {}
    for e in examples:
        by_regime.setdefault(e["metadata_regime_label"], []).append(1 if e["output"] == "1" else 0)
    for regime, labels in by_regime.items():
        logger.info(f"  regime={regime}: n={len(labels)} violation_rate={sum(labels) / len(labels):.4f}")

    metadata = {
        "source": "Azure Functions 2019 trace (Shahrad et al., USENIX ATC 2020) + one synthetic adversarial "
                   "regime; see raw_azure_admission_control.json's schema_doc/provenance_summary for full "
                   "construction details and exact SLO/risk-score formulas",
        "description": "Request-level admission-control decisions across 5 traffic regimes "
                       "(stationary/burst/drift/regime_switch/adversarial) for a conformal admission-control "
                       "policy. output=1 iff the request's realized service_time exceeded its function's "
                       "documented slo_target (p99 of that function's real duration distribution). "
                       "This dataset is split into multiple part files (see full_data_out/) to stay under the "
                       "100MB per-file limit; concatenate all parts' examples to reconstruct the full dataset.",
    }
    dataset_name = "azure_functions_2019_admission_control_traces"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    n_parts = min(N_PARTS, len(examples)) or 1
    chunk_size = -(-len(examples) // n_parts)  # ceil division
    for part_idx in range(n_parts):
        chunk = examples[part_idx * chunk_size : (part_idx + 1) * chunk_size]
        if not chunk:
            continue
        part_out = {
            "metadata": metadata,
            "datasets": [{"dataset": dataset_name, "examples": chunk}],
        }
        part_path = OUT_DIR / f"full_data_out_{part_idx + 1}.json"
        part_path.write_text(json.dumps(part_out))
        logger.info(
            f"Wrote {part_path} ({len(chunk)} examples, {part_path.stat().st_size / 1e6:.1f} MB)"
        )


if __name__ == "__main__":
    main()
