# Contributing to EmDashify

EmDashify intentionally does one small job. Keep proposed changes focused on predictable, safe em-dash conversion rather than general grammar correction or AI authorship detection.

## Local setup

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

For any behavior change, add tests covering ordinary prose, CLI flags or code examples, Unicode, and Markdown where relevant. The default mode should remain conservative. A new rule that may alter commands or source code must be opt-in and clearly documented.

Do not add mandatory runtime dependencies without a strong justification.
