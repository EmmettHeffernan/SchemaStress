import argparse,json,sys
from pathlib import Path
from .core import load_cases,evaluate,render_markdown
def main():
 p=argparse.ArgumentParser(prog="schemastress"); sub=p.add_subparsers(dest="command",required=True); d=sub.add_parser("demo"); d.add_argument("--cases",default="datasets/cases.jsonl"); d.add_argument("--schema",default="datasets/incident.schema.json"); d.add_argument("--out",default="reports/demo"); d.add_argument("--fail-below",type=float,default=None); a=p.parse_args()
 cases=load_cases(a.cases); schema=json.loads(Path(a.schema).read_text()); outputs={c["case_id"]:c["expected"] for c in cases}; outputs[cases[1]["case_id"]]='{"incident_id":'; outputs[cases[3]["case_id"]]={**cases[3]["expected"],"severity":"critical"}; report=evaluate(cases,outputs,schema)
 out=Path(a.out); out.mkdir(parents=True,exist_ok=True); (out/"report.json").write_text(json.dumps(report,indent=2)+"\n"); (out/"report.md").write_text(render_markdown(report)); print(json.dumps(report["summary"],indent=2)); print(f"Reports written to {out.resolve()}")
 if a.fail_below is not None and report["summary"]["field_accuracy"]<a.fail_below: print(f"Regression gate failed: field accuracy below {a.fail_below:.1%}",file=sys.stderr); return 1
 return 0
if __name__=="__main__": raise SystemExit(main())
