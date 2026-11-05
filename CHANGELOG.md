# Changelog

All notable changes to this project will be documented here.

## [0.2.0] - 2026-11-05

- Add conversion for complete Microsoft Word `.docx` documents, including text in tables, headers, footers, hyperlinks, and accessible text boxes; preserve run formatting.
- Add `convert_docx(path, output)` and `check_docx(path)` in Python.
- Add Word support to the CLI: `--file input.docx --output output.docx`, `--check`, and `--compact`.
- Keep Word dependencies optional via `pip install "emdashify[word]"`.
- Refresh README tagline and document Word conversion with conservative behavior.

## [0.1.0] - 2026-11-05

- Initial release for Python 3.10+ with zero runtime dependencies.
- Convert explicit standalone `--` markers into Unicode em dashes (`—`).
- Support optional compact `word--word` conversion.
- Offer Markdown-aware conversion that preserves common code spans and blocks.
- Provide `convert()`, `check()`, and `convert_file()` in Python.
- Include a CLI for text, stdin, and files with `--check`, `--diff`, and `--output`.
- Add automated tests, wheel/source-distribution checks, and Trusted Publishing to PyPI.
- License under BSD-3-Clause-Attribution, requiring an acknowledgment when redistributing the package.
