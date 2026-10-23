# SchemaStress vs Promptfoo: preliminary comparison

**Status: deterministic parity analysis completed; a real Promptfoo CLI run remains blocked in this environment. A runnable offline Promptfoo config has now been added.**

## Question
Does SchemaStress demonstrate a capability that Promptfoo cannot provide for structured extraction?

## What was compared
- The same 12 synthetic incident cases and same expected records.
- The same deliberately injected outputs used by the SchemaStress demo: one malformed JSON output (INC-002) and one valid JSON object with a wrong severity (INC-004); other outputs match their fixture labels.
- SchemaStress was run using its implementation. Promptfoo's documented equivalent assertions (`is-json` with a JSON Schema plus a JavaScript exact-value assertion) were independently evaluated against the exact same deterministic outputs.

This is **not** a claim that Promptfoo itself ran. Its CLI/package and an Ollama model endpoint were unavailable in the execution environment, and network access prevented installing them. To make the comparison independently reproducible, `promptfooconfig.deterministic.yaml` and `deterministic_provider.py` now run the exact same seeded outputs through the actual Promptfoo CLI once Promptfoo is installed; no model is needed for that parity run. The separate `promptfooconfig.yaml` remains the live Ollama model config.

## Results

| Metric | SchemaStress | Promptfoo-equivalent assertions |
|---|---:|---:|
| Cases | 12 | 12 |
| JSON parse pass | 91.7% | 91.7% |
| Schema compliance | 91.7% | 91.7% |
| Exact expected-value match | 83.3% | 83.3% |
| Whole case passes all checks | 83.3% | 83.3% |
| Field-level accuracy | 89.6% | Not directly emitted by these baseline assertions; custom JS or post-processing can calculate it |

The parity is expected: the assertions were designed to express the same deterministic checks. The figures are **fixture/demo metrics, not model performance**.

## Capability comparison

| Capability | SchemaStress prototype | Promptfoo documented capability | Assessment
|---|---|---|
| JSON parse validation | Built in | `is-json` assertion | Parity
| JSON Schema validation | Built in using `jsonschema` | `is-json` can validate against a schema | Parity
| Exact field-value assertions | Built in scoring | JavaScript assertions can check parsed fields | Parity in capability; different setup ergonomics
| Aggregate field accuracy and exact-case match | Built in report | Requires custom assertions/metrics or post-processing to express these exact aggregates | SchemaStress convenience, not unique capability
| Field-level expected/actual diagnostics | Built in in Markdown/JSON report | Can be implemented with JavaScript assertions, custom scripts, and/or result processing; not established as impossible in Promptfoo | Possible ergonomic difference only
| Evidence snippet shown beside mismatch | Evidence is attached to each fixture field and displayed in failure report | Requires carrying evidence in test metadata/vars and custom reporting/processing | Potentially useful default workflow, not a proven exclusive capability
| Regression threshold exit code | CLI supports `--fail-below` | Promptfoo supports assertions/thresholds and CI workflows; equivalent gate needs configuration | No defensible differentiation yet
| Model/provider matrix, prompt iteration, evaluation UI, broader assertion ecosystem | Not implemented | Core Promptfoo strengths | Promptfoo advantage
| No model required for deterministic scoring | Yes | Promptfoo can also evaluate precomputed outputs using standalone assertion mode, if installed | Not unique

## Finding
**The current prototype does not establish a defensible technical moat over Promptfoo.** Promptfoo's documented `is-json` plus JavaScript assertions cover the core validation and exact-value checks. SchemaStress currently packages a narrower workflow with field-level scoring and evidence-oriented report formatting. That can be a useful engineering artifact, but convenience alone is a weak differentiator unless a real user values it enough to switch or adopt it alongside Promptfoo.

## Recommended next experiment
1. Install/run Promptfoo and Ollama on a reachable machine; use the included 12-case `promptfooconfig.yaml` so the same prompt and cases are evaluated by a real model.
2. Save raw model outputs from both runs; use identical provider, model, prompt, schema, temperature, and decoding settings.
3. Compare not only pass rates but time-to-diagnose: can a developer trace each failed field to evidence, expected/actual values, and the specific case without writing custom glue?
4. Ask 3–5 developers to diagnose the same seeded failures with each report. Measure task completion time and error identification accuracy. If the evidence report does not materially improve diagnosis, narrow the project to a clean portfolio demonstration or pivot.

## Sources
- Promptfoo, [Evaluating JSON Outputs](https://www.promptfoo.dev/docs/guides/evaluate-json/): `is-json` supports JSON Schema validation; JavaScript assertions can inspect exact fields.
- Promptfoo, [Assertions and Metrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/): supports running assertions against precomputed model outputs.
- Promptfoo, [Custom Python Provider](https://www.promptfoo.dev/docs/providers/python/): documents `file://` Python providers for deterministic or custom evaluation logic.


## Reproducible Promptfoo execution

Run this from the repository root on any machine with Node.js and internet access (or Promptfoo already installed):

```bash
npx promptfoo@latest eval -c promptfooconfig.deterministic.yaml --no-cache
```

The custom provider returns fixture outputs only: INC-002 is malformed JSON and INC-004 has an incorrect severity. This isolates assertion behavior from model quality and randomness. It does not establish live model performance. `python scripts/check_parity.py` confirms the fixture provider reproduces the exact 12-case deterministic outputs and expected aggregate scores, but explicitly does not claim that Promptfoo ran. After this parity run, use `promptfooconfig.yaml` to evaluate the configured Ollama model, then compare its raw outputs with SchemaStress scoring.
