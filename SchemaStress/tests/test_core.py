import json
from pathlib import Path
from schemastress.core import load_cases,validate_output,score_case,summarize
R=Path(__file__).parents[1]; S=json.loads((R/"datasets/incident.schema.json").read_text())
def test_unique_dataset():
 c=load_cases(R/"datasets/cases.jsonl"); assert len(c)==12 and len({x["case_id"] for x in c})==12
def test_valid_json_schema():
 r=validate_output({"incident_id":"INC-1","service":"api","severity":"high","customer_impact":None},S); assert r["parse_success"] and r["schema_valid"]
def test_bad_json():
 r=validate_output('{"incident_id":',S); assert not r["parse_success"] and r["errors"]
def test_extra_field_invalid():
 r=validate_output({"incident_id":"INC-1","service":"api","severity":"low","customer_impact":None,"extra":1},S); assert r["parse_success"] and not r["schema_valid"]
def test_wrong_field_evidence():
 c=load_cases(R/"datasets/cases.jsonl")[0]; r=score_case(c,{**c["expected"],"service":"wrong"},S); assert r["field_accuracy"]<1 and r["fields"]["service"]["evidence"]=="Service: payments-api"
def test_summary():
 s=summarize([{"parse_success":True,"schema_valid":True,"field_accuracy":1,"all_expected_fields_correct":True,"fields":{"a":{"correct":True}}},{"parse_success":False,"schema_valid":False,"field_accuracy":0,"all_expected_fields_correct":False,"fields":{"a":{"correct":False}}}]); assert s["parse_success_rate"]==.5 and s["schema_compliance_rate"]==.5 and s["field_accuracy"]==.5
