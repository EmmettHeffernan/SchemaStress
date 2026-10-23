"""Deterministic provider for fair, model-free Promptfoo parity checks.

Returns the same seeded outputs as `schemastress demo`; this is NOT an LLM.
Promptfoo passes vars.case_id via context so each test maps to its fixed output.
"""
import json
from pathlib import Path


def call_api(prompt, options, context):
    config = options.get("config", {})
    base = Path(config.get("basePath", "."))
    cases_path = base / config.get("cases_path", "datasets/cases.jsonl")
    cases = [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    case_id = context.get("vars", {}).get("case_id")
    case = next((item for item in cases if item["case_id"] == case_id), None)
    if case is None:
        return {"error": f"Unknown or missing case_id: {case_id!r}"}
    output = dict(case["expected"])
    if case_id == "INC-002":
        return {"output": '{"incident_id":'}
    if case_id == "INC-004":
        output["severity"] = "critical"
    return {"output": json.dumps(output, separators=(",", ":"))}
