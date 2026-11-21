# SchemaStress dashboard

Static portfolio site with no third-party JavaScript, network APIs, database or exposed model server.

- `index.html`: self-contained data embed; works directly from the filesystem.
- `assets/`: accessible interactive case explorer and presentation styles.
- `data/deterministic-demo.json`: a derived, compact representation of the existing **synthetic** historical report. Rebuild rather than hand-edit.
- `../scripts/build_site.py`: deterministic generator from the original `SchemaStress/reports/demo/report.json`.

The page makes no numerical claim about Qwen performance. Replace the pending Qwen panel only after independently recorded local-model experiments, with explicit configuration, held-out data and separate provenance.

To preview locally, open `site/index.html` in a browser. See the root README for publication controls.
