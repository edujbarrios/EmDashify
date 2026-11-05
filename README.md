# EmDashify — `--` → `—`

[![PyPI](https://img.shields.io/pypi/v/emdashify.svg?label=PyPI&logo=pypi)](https://pypi.org/project/emdashify/)
[![Python](https://img.shields.io/pypi/pyversions/emdashify.svg?label=Python&logo=python)](https://pypi.org/project/emdashify/)
[![Tests](https://img.shields.io/github/actions/workflow/status/edujbarrios/EmDashify/tests.yml?branch=main&label=tests&logo=githubactions)](https://github.com/edujbarrios/EmDashify/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-BSD--3--Clause--Attribution-blue)](https://github.com/edujbarrios/EmDashify/blob/main/LICENSE)

**The Python library you think you'll never need—until you use it more than the ones you do.**

## Why?

LLMs made the em dash (`—`) hard to ignore. [Pew Research Center](https://www.pewresearch.org/data-labs/2026/08/20/how-much-of-the-internet-is-written-with-ai/) found that em dashes appeared **about twice as often** in the English-language web text it studied as in 2023. An em dash is not proof of AI authorship; it's ordinary punctuation.

Yet most QWERTY keyboards have a `-` key, **not a dedicated `—` key**. EmDashify turns two easy hyphens into one proper em dash. No AI. Just punctuation.

## Quick start

```bash
pip install emdashify
emdashify "Hello -- world"
# Hello — world
```

```python
from emdashify import convert

convert("Hello -- world")             # 'Hello — world'
convert("hello--world", compact=True) # 'hello—world'
```

## Word documents (.docx)

**New in v0.2.0:** convert an entire Word document, including paragraphs, tables, headers and footers, **without flattening text formatting**. Install the optional Word extra:

```bash
pip install "emdashify[word]"
emdashify --file draft.docx --output draft-fixed.docx
emdashify --file draft.docx --check
```

```python
from emdashify import convert_docx

convert_docx("draft.docx", "draft-fixed.docx")
```

The original file is never overwritten. Word support is for `.docx`, **not legacy `.doc`**. Review complex documents with tracked changes or advanced Word fields after conversion.

## Text and Markdown files

```bash
emdashify --file notes.md --diff
emdashify --file notes.md --output notes-fixed.md
emdashify --file notes.md --check
```

**Safe by default:** only standalone `--` becomes `—`. Flags (`--help`), dates, and `---` stay unchanged; Markdown code blocks are protected. Use `--compact` for `word--word`.

Requires Python 3.10+. For development or publishing, see [release instructions](https://github.com/edujbarrios/EmDashify/blob/main/docs/RELEASING.md).

## License

[BSD-3-Clause-Attribution](https://github.com/edujbarrios/EmDashify/blob/main/LICENSE). Redistributing EmDashify requires retaining license notices and this acknowledgment:

> This product includes software developed by edujbarrios (https://github.com/edujbarrios/EmDashify).
