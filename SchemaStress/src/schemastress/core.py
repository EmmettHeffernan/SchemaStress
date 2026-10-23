import json
from pathlib import Path
from jsonschema import Draft202012Validator

def load_cases(path):
    cases=[]
    for n,line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try: c=json.loads(line)
        except json.JSONDecodeError as e: raise ValueError(f"{path}:{n}: invalid JSONL: {e}") from e
        for k in ("case_id","category","source_text","expected","evidence"):
            if k not in c: raise ValueError(f"{path}:{n}: missing {k}")
        cases.append(c)
    ids=[c["case_id"] for c in cases]
    if len(ids)!=len(set(ids)): raise ValueError("case_id values must be unique")
    return cases

def validate_output(output,schema):
    if isinstance(output,str):
        try: parsed=json.loads(output)
        except json.JSONDecodeError as e: return {"parse_success":False,"schema_valid":False,"parsed":None,"errors":[f"invalid JSON line {e.lineno}, column {e.colno}: {e.msg}"]}
    else: parsed=output
    errors=sorted(Draft202012Validator(schema).iter_errors(parsed),key=lambda e:list(map(str,e.absolute_path)))
    return {"parse_success":True,"schema_valid":not errors,"parsed":parsed,"errors":[f"{'/'.join(map(str,e.absolute_path)) or '<root>'}: {e.message}" for e in errors]}

def score_case(case,output,schema):
    v=validate_output(output,schema); parsed=v["parsed"] if isinstance(v["parsed"],dict) else {}; expected=case["expected"]
    fields={}
    for f in sorted(set(expected)|set(parsed)):
        exp=expected.get(f,"<MISSING>"); actual=parsed.get(f,"<MISSING>")
        fields[f]={"expected":exp,"actual":actual,"correct":exp==actual,"evidence":case.get("evidence",{}).get(f)}
    n=max(1,len(expected)); correct=sum(fields[f]["correct"] for f in expected)
    return {"case_id":case["case_id"],"category":case["category"],"parse_success":v["parse_success"],"schema_valid":v["schema_valid"],"field_accuracy":correct/n,"all_expected_fields_correct":correct==len(expected),"errors":v["errors"],"fields":fields}

def summarize(results):
    n=len(results); fields=[f for r in results for f in r["fields"].values()]
    return {"cases":n,"parse_success_rate":sum(r["parse_success"] for r in results)/n if n else 0,"schema_compliance_rate":sum(r["schema_valid"] for r in results)/n if n else 0,"field_accuracy":sum(f["correct"] for f in fields)/len(fields) if fields else 0,"case_exact_match_rate":sum(r["all_expected_fields_correct"] for r in results)/n if n else 0}

def evaluate(cases,outputs,schema):
    results=[]
    for c in cases:
        if c["case_id"] not in outputs: raise ValueError(f"missing output for case {c['case_id']}")
        results.append(score_case(c,outputs[c["case_id"]],schema))
    return {"summary":summarize(results),"results":results}

def render_markdown(report):
    s=report["summary"]; lines=["# SchemaStress Evaluation Report","","| Metric | Result |","|---|---:|",f"| Cases | {s['cases']} |",f"| JSON parse success | {s['parse_success_rate']:.1%} |",f"| Schema compliance | {s['schema_compliance_rate']:.1%} |",f"| Field accuracy | {s['field_accuracy']:.1%} |",f"| Exact case match | {s['case_exact_match_rate']:.1%} |","","## Per-case diagnostics"]
    for r in report["results"]:
        lines += ["",f"### {r['case_id']} — {r['category']}",f"- Parse success: `{r['parse_success']}`",f"- Schema valid: `{r['schema_valid']}`",f"- Field accuracy: `{r['field_accuracy']:.1%}`"]
        lines += [f"- Error: {e}" for e in r["errors"]]
        for k,f in r["fields"].items():
            if not f["correct"]: lines.append(f"- Mismatch `{k}`: expected `{f['expected']}`, got `{f['actual']}`; evidence: {f['evidence']!r}")
    return "\n".join(lines)+"\n"
