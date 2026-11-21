# SchemaStress
SchemaStress evaluates incident extraction at four levels: JSON decoding, schema validation, field values and agreement across all expected fields.

[Open the fixture dashboard source](site/index.html) or open that file from a local checkout for an interactive preview. The 12 synthetic development cases contain two deliberately seeded errors. Their scores describe the evaluator's controls. No Qwen measurements are included.

## Reproduce the dashboard
From the repository root with Python 3.11 or newer:
```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e './SchemaStress[dev]'
(cd SchemaStress && python -m pytest -q && schemastress demo && python scripts/check_parity.py)
python scripts/build_site.py --check
```
The parity script runs the deterministic Python provider. A Promptfoo CLI result would require separate evidence. The original project, data, reports and research notes remain under [SchemaStress/](SchemaStress/).

Run `python scripts/build_site.py` to refresh the static projection after reviewing a fixture report change. [CI](.github/workflows/ci-pages.yml) checks fixture reproduction and the dashboard on pull requests. Publishing requires separate owner approval, an appropriately configured GitHub Pages source, and an explicit manual run on main with publish selected.

[Next milestone: offline Qwen runner handoff](SchemaStress/docs/qwen-runner-handoff.md)
