import json
from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("deterministic_provider", ROOT / "deterministic_provider.py")
provider = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provider)

def test_promptfoo_config_covers_all_cases():
    cfg = yaml.safe_load((ROOT / "promptfooconfig.deterministic.yaml").read_text())
    cases = [json.loads(line) for line in (ROOT / "datasets/cases.jsonl").read_text().splitlines() if line.strip()]
    assert len(cfg["tests"]) == len(cases) == 12
    assert {t["vars"]["case_id"] for t in cfg["tests"]} == {c["case_id"] for c in cases}

def test_deterministic_provider_injects_expected_faults():
    cfg = {"config": {"basePath": str(ROOT), "cases_path": "datasets/cases.jsonl"}}
    def call(case_id):
        return provider.call_api("prompt", cfg, {"vars": {"case_id": case_id}})["output"]
    assert call("INC-002") == '{"incident_id":'
    assert json.loads(call("INC-004"))["severity"] == "critical"
    assert json.loads(call("INC-001"))["severity"] == "high"
