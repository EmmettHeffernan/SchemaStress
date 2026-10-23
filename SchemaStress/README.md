# SchemaStress
Local-first, evidence-linked regression testing for structured AI extraction.

## Status
Early prototype. Synthetic cases are fixtures, not a validated benchmark. Demo outputs intentionally inject errors; they are not model performance.

## Install and test
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest -q
```

## Deterministic demo
```bash
schemastress demo
schemastress demo --fail-below 1.0
```
The first command writes JSON and Markdown reports under `reports/demo`. The second should exit non-zero because failures are intentionally injected.

## Promptfoo baseline
- `promptfooconfig.yaml`: local Ollama model evaluation; requires Promptfoo, Ollama, and the configured model.
- `promptfooconfig.deterministic.yaml`: real Promptfoo CLI run against a deterministic fixture provider. It uses the exact seeded outputs from `schemastress demo`, so it tests assertion/reporting parity without model variability or API cost.

Run the deterministic Promptfoo baseline from the repository root:
```bash
npx promptfoo@latest eval -c promptfooconfig.deterministic.yaml --no-cache
```
This still requires installing Promptfoo (internet access or a preinstalled package), but it does not require a model or API key. The CLI could not be installed in the current execution environment because outbound DNS/network access is blocked. `python scripts/check_parity.py` independently verifies that the fixed provider returns the same seeded outputs used by SchemaStress; it is not a substitute for the actual Promptfoo CLI run. See `docs/promptfoo-comparison.md`.

## Promptfoo comparison (preliminary)
See [`docs/promptfoo-comparison.md`](docs/promptfoo-comparison.md) for the deterministic parity analysis and caveats. `promptfooconfig.yaml` now contains all 12 synthetic cases with schema and exact-value assertions. The config parses locally, but a live `promptfoo eval` with Ollama has **not** been run in this environment.


## Running the actual Promptfoo CLI

If the current environment cannot download npm packages, see [`docs/promptfoo-workaround.md`](docs/promptfoo-workaround.md). A GitHub Actions workflow is included to run the real CLI on a hosted runner.
