# EmDashify — `--` → `—`

**Probably the most unnecessary Python library you'll use more than you expect.**

Two hyphens. One em dash. Zero AI.

## Why does this exist?

The em dash (`—`) has become the punctuation celebrity of the LLM era. ChatGPT and other language models use it often, and [Pew Research Center](https://www.pewresearch.org/data-labs/2026/08/20/how-much-of-the-internet-is-written-with-ai/) found that em dashes appeared roughly twice as often in the web text it studied as they did in 2023. But the em dash existed long before AI, and **using one does not prove a text was AI-generated**.

Meanwhile, most QWERTY keyboards have a `-` key but **no dedicated `—` key**. You can use an operating-system shortcut, but it differs across systems and is easy to forget.

**EmDashify solves the small, practical part:** write `--` in your text, then convert it to `—` from Python, your terminal, or a file. No language model, no runtime dependencies, and no keyboard monitoring.

## Install

```bash
pip install emdashify
```

Requires Python 3.10+. Until the first PyPI release, install it from a local checkout with `python -m pip install -e .`.

## Usage

**Python**

```python
from emdashify import convert

convert("Hello -- world")            # 'Hello — world'
convert("hello--world", compact=True) # 'hello—world'
```

**Terminal**

```bash
emdashify "Hello -- world"
# Hello — world

printf 'Hello -- world\n' | emdashify
# Hello — world
```

**Markdown and text files**

```bash
emdashify --file notes.md --diff
emdashify --file notes.md --output notes-fixed.md
emdashify --file notes.md --check
```

The original file is never overwritten implicitly. `--check` returns exit code `1` if any changes are needed and `0` otherwise. Python also exposes `check(text)` and `convert_file(path, output=...)`.

## Small by design, careful by default

By default, only **standalone `--` markers** become `—` (between whitespace or at text boundaries). EmDashify does not change `--help`, `---`, dates such as `2026-11-05`, single hyphens, or hyphenated words. The optional `--compact` flag (or `compact=True`) also converts `word--word` between letters.

When reading Markdown files, EmDashify protects inline code, fenced code blocks, and indented code blocks. This is a lightweight safeguard, not a full Markdown parser. It does **not** automatically replace keystrokes as you type: you choose when to run it.

## Development and release

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

The release process is documented in [docs/RELEASING.md](docs/RELEASING.md).

## License and attribution

Licensed under [BSD-3-Clause-Attribution](LICENSE). Redistribution requires retaining the license notices and this acknowledgment:

> This product includes software developed by edujbarrios (https://github.com/edujbarrios/EmDashify).

Private use without redistribution does not require public attribution.
