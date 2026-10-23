"""Check that SchemaStress and the deterministic Promptfoo provider share fixtures.

This does not execute Promptfoo. It verifies the shared deterministic outputs and
computes SchemaStress's metrics so a later actual Promptfoo run can be compared.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("deterministic_provider", ROOT / "deterministic_provider.py")
provider = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provider)

from schemastress.core import evaluate, load_cases

cases = load_cases(ROOT / "datasets/cases.jsonl")
schema = json.loads((ROOT / "datasets/incident.schema.json").read_text(encoding="utf-8"))
outputs = {}
for case in cases:
    response = provider.call_api(
        "unused deterministic prompt",
        {"config": {"basePath": str(ROOT), "cases_path": "datasets/cases.jsonl"}},
        {"vars": {"case_id": case["case_id"]}},
    )
    if "error" in response:
        raise RuntimeError(response["error"])
    outputs[case["case_id"]] = response["output"]
report = evaluate(cases, outputs, schema)
print(json.dumps({"fixture_cases": len(cases), "schemastress_summary_on_promptfoo_provider_outputs": report["summary"], "actual_promptfoo_cli_executed": False}, indent=2))
