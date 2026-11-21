#!/usr/bin/env python3
"""Rebuild the static SchemaStress dashboard from the checked-in fixture report.

No model inference or external network access.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "SchemaStress" / "reports" / "demo" / "report.json"
DATA = ROOT / "site" / "data" / "deterministic-demo.json"
INDEX = ROOT / "site" / "index.html"
START = "<!-- EMBED_DATA_START -->"
END = "<!-- EMBED_DATA_END -->"


def projection(source: dict) -> dict:
    if not isinstance(source.get("results"), list) or not isinstance(source.get("summary"), dict):
        raise ValueError("Expected the original SchemaStress report with results and summary")
    results = []
    for case in source["results"]:
        mismatches = []
        for name, field in case["fields"].items():
            if not field["correct"]:
                mismatches.append({
                    "name": name,
                    "expected": field["expected"],
                    "actual": field["actual"],
                    "evidence": field.get("evidence"),
                })
        results.append({
            "id": case["case_id"],
            "category": case["category"],
            "parse_success": bool(case["parse_success"]),
            "schema_valid": bool(case["schema_valid"]),
            "field_accuracy": case["field_accuracy"],
            "exact_match": bool(case["all_expected_fields_correct"]),
            "errors": case["errors"],
            "mismatches": mismatches,
        })
    return {
        "provenance": "deterministic_fixture",
        "source_file": "SchemaStress/reports/demo/report.json",
        "description": "Compact projection of the existing 12-case seeded synthetic demo. No LLM executed.",
        "summary": source["summary"],
        "results": results,
    }


def embedded_html(page: str, data: dict) -> str:
    if page.count(START) != 1 or page.count(END) != 1 or page.index(START) > page.index(END):
        raise ValueError("Expected exactly one dashboard data marker pair")
    payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    embedded = START + '\n  <script id="demo-data" type="application/json">' + payload + '</script>\n  ' + END
    return re.sub(re.escape(START) + r"[\s\S]*?" + re.escape(END), lambda _: embedded, page, count=1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check that published data and HTML match the authoritative report")
    args = parser.parse_args()
    payload = projection(json.loads(SOURCE.read_text(encoding="utf-8")))
    if payload["summary"]["cases"] != len(payload["results"]):
        raise ValueError("Summary case count differs from results length")
    saved = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    original = INDEX.read_text(encoding="utf-8")
    expected_page = embedded_html(original, payload)
    if args.check:
        if DATA.read_text(encoding="utf-8") != saved or original != expected_page:
            print("Dashboard data differs from SchemaStress's recorded report; run python scripts/build_site.py", file=sys.stderr)
            return 1
        print("PASS: Dashboard data, embedded page, and source report agree")
        return 0
    DATA.write_text(saved, encoding="utf-8")
    INDEX.write_text(expected_page, encoding="utf-8")
    print("Updated site/data/deterministic-demo.json and embedded site/index.html data")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
