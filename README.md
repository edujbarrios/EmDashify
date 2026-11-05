# EmDashify — Em Dashes Made Easy

[![PyPI v0.3.0](https://raw.githubusercontent.com/edujbarrios/EmDashify/main/assets/badges/pypi.svg)](https://pypi.org/project/emdashify/)
[![Python 3.10+](https://raw.githubusercontent.com/edujbarrios/EmDashify/main/assets/badges/python.svg)](https://pypi.org/project/emdashify/)
[![Tests](https://img.shields.io/github/actions/workflow/status/edujbarrios/EmDashify/tests.yml?branch=main&label=tests&logo=githubactions)](https://github.com/edujbarrios/EmDashify/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-BSD--3--Clause--Attribution-blue)](https://github.com/edujbarrios/EmDashify/blob/main/LICENSE)

**The Python library you think you'll never need—until you use it more than the ones you do.**

## Why?

ChatGPT, Claude, and other large language models often use the em dash (`—`) when answering users. It's become especially noticeable in AI-generated responses: [Pew Research Center](https://www.pewresearch.org/data-labs/2026/08/20/how-much-of-the-internet-is-written-with-ai/) found that em dashes appeared **about twice as often** in the English-language web text it studied as in 2023. Of course, the em dash predates AI—it's ordinary punctuation, not proof that a text was AI-written.

Yet most QWERTY keyboards have a `-` key, **not a dedicated `—` key**. EmDashify lets you type `--` and turn it into a proper em dash in text, Markdown, or Word documents. No AI needed. Just punctuation.

## Quick start

```bash
pip install emdashify
emdashify "Hello -- world"
# Hello—world
```

```python
from emdashify import convert

convert("Hello -- world")                  # 'Hello—world'
convert("hello--world")                    # 'hello—world'
convert("Hello -- world", compact=False)   # 'Hello — world'
```

## Word documents (.docx)

Convert an entire Word document, including paragraphs, tables, headers and footers, **without flattening text formatting**. Install the optional Word extra:

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

**Compact by default:** both `word--word` and `word -- word` become `word—word`. Flags (`--help`), dates, and `---` stay unchanged; Markdown code blocks are protected. Use `--spaced` in the CLI (or `compact=False` in Python) to retain the former spaced style.

Requires Python 3.10+. For development or publishing, see [release instructions](https://github.com/edujbarrios/EmDashify/blob/main/docs/RELEASING.md).

## License

[BSD-3-Clause-Attribution](https://github.com/edujbarrios/EmDashify/blob/main/LICENSE). Redistributing EmDashify requires retaining license notices and this acknowledgment:

> This product includes software developed by edujbarrios (https://github.com/edujbarrios/EmDashify).
