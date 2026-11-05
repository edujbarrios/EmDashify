# EmDashify — `--` → `—`

[![PyPI](https://img.shields.io/pypi/v/emdashify?label=PyPI&logo=pypi)](https://pypi.org/project/emdashify/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://pypi.org/project/emdashify/)
[![Tests](https://github.com/edujbarrios/EmDashify/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/edujbarrios/EmDashify/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-BSD--3--Clause--Attribution-blue)](LICENSE)

**The most unnecessary Python library you'll actually use.**

## Why EmDashify?

LLMs made the em dash (`—`) hard to ignore. [Pew Research Center](https://www.pewresearch.org/data-labs/2026/08/20/how-much-of-the-internet-is-written-with-ai/) found that em dashes appeared **about twice as often** in sampled English-language web text as in 2023. That doesn't make an em dash proof of AI authorship.

The problem? Most QWERTY keyboards have a `-` key, but no dedicated `—` key.

**EmDashify** converts `--` to `—` in Python, your terminal, or text files. No AI. No runtime dependencies. Just punctuation.

## Quick start

```bash
pip install emdashify
emdashify "Hello -- world"
# Hello — world
```

```python
from emdashify import convert

convert("Hello -- world")              # "Hello — world"
convert("hello--world", compact=True)  # "hello—world"
```

## Files

```bash
emdashify --file notes.md --diff
emdashify --file notes.md --output notes-fixed.md
emdashify --file notes.md --check
```

**Safe by default:** only standalone `--` markers are converted. Flags (`--help`), dates, and `---` remain unchanged. Markdown code spans and blocks are protected, and files aren't overwritten implicitly. Use `--compact` for `word--word`.

Requires Python 3.10+. See [release instructions](docs/RELEASING.md) for development and publishing.

## License

[BSD-3-Clause-Attribution](LICENSE). Redistributing the package requires preserving the license notices and this acknowledgment:

> This product includes software developed by edujbarrios (https://github.com/edujbarrios/EmDashify).
