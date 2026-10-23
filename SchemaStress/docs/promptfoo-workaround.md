# Workaround for running the real Promptfoo CLI

The ChatGPT execution container currently has no outbound DNS/network access, so it cannot download the Promptfoo npm package. The deterministic Python parity check is **not** a substitute for an actual Promptfoo CLI run.

## Option A — run on a machine with npm access

From the repository root, with Node.js 22 and Python installed:

```bash
python -m pip install -e ".[dev]"
pytest -q
python scripts/check_parity.py
npx --yes promptfoo@latest eval -c promptfooconfig.deterministic.yaml --no-cache --output promptfoo-results.json
```

This deterministic evaluation uses no paid model API. It tests Promptfoo's actual assertion engine against seeded fixture outputs, not LLM quality.

## Option B — use GitHub Actions

The repository includes `.github/workflows/promptfoo-comparison.yml`. After the project is pushed to a GitHub repository, open **Actions → Promptfoo deterministic comparison → Run workflow**. GitHub's hosted runner can install Promptfoo using npm, run the tests and evaluation, and attach result files as a workflow artifact.

The workflow is deliberately manual-capable and only runs automatically on relevant project-file changes. It does not need secrets or a model API key.

## Important interpretation

- `scripts/check_parity.py` computes expected parity from shared fixtures; it does not execute Promptfoo.
- The GitHub Actions `npx promptfoo ... eval` step is the real Promptfoo run.
- Since the provider intentionally injects two failures, the evaluation is a plumbing/diagnostics test, not a benchmark of model capability.
- If Promptfoo rejects the YAML, provider path, or assertion syntax, use the workflow logs to fix that integration before drawing conclusions.
