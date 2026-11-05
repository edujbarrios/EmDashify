# Changelog

All notable changes to this project will be documented here.

## [0.1.0] - Unreleased

- Explain EmDashify's motivation and usage in the README.
- Add a release workflow with trusted PyPI publishing and package checks.

- Replace the MIT license with BSD-3-Clause-Attribution, requiring an author acknowledgment in redistributions.

- Add `convert`, `check`, and `convert_file` with no runtime dependencies.
- Convert standalone double hyphens (`--`) to em dashes (`—`).
- Add optional compact mode for `word--word`.
- Preserve fenced code blocks, indented code, and inline code spans in Markdown mode.
- Add a CLI for direct text, stdin, and UTF-8 files with `--check`, `--diff`, and `--output`.
- Include type information, tests, and a CI workflow.
