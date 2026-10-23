# SchemaStress Research Review
**Snapshot:** 2026-10-22. **Status:** preliminary; direct tool comparison still required.

## Findings
- [JSONSchemaBench](https://arxiv.org/abs/2501.10868): constrained decoding, schema coverage, efficiency and output quality. Do not rebuild a generic schema benchmark.
- [LLMStructBench](https://arxiv.org/abs/2602.14743): structured extraction with validity and semantic accuracy. Keep those metrics separate.
- [TrustDABench](https://arxiv.org/abs/2608.24145): perturbation robustness and insufficient/conflicting evidence. These are not novel alone.
- [CONSTRUCT](https://arxiv.org/abs/2603.18014): structured-output trustworthiness and field-level risk. Field diagnostics alone are not a novelty claim.
- [Promptfoo JSON evaluation](https://www.promptfoo.dev/docs/guides/evaluate-json/): JSON/schema checks and custom assertions. Must compare directly.
- [Ollama structured outputs](https://ollama.com/blog/structured-outputs): candidate local inference adapter.

## Hypothesis
An evidence-linked regression report can connect each failed field to a stable test ID, source evidence, expected and actual values, failure category, and run configuration. The possible value is diagnostic traceability, not new metrics.

## Baseline status
A Promptfoo starter config is included. It has **not** been run here because Promptfoo/Ollama availability is not established. Do not call this a completed live comparison.

## Gate 0 decision
Proceed with a deterministic prototype. Run equivalent cases in Promptfoo and SchemaStress before claiming differentiation. If Promptfoo provides equivalent diagnostics easily, position SchemaStress as an engineering demonstration or narrow the gap.

## Limitations
The starter dataset is synthetic and small; labels/evidence need audit; no live model evaluation was run; no novelty or real-world generalization is claimed.
