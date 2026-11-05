# EmDashify — two hyphens, one em dash

**Type `--`. Get `—`. No AI required.**

The em dash (`—`, U+2014) has become surprisingly visible in the age of LLMs. ChatGPT and other language models use it frequently; [Pew Research Center found](https://www.pewresearch.org/data-labs/2026/08/20/how-much-of-the-internet-is-written-with-ai/) that em dashes appeared about twice as often in the web text it studied as in 2023. The symbol is much older than AI, though — **using one does not mean a text was AI-generated**.

Here is the actual problem: **most QWERTY keyboards have a `-` key, but no dedicated `—` key.** Operating-system shortcuts exist, but they vary and are awkward to remember when you just want to write.

**EmDashify lets you write two ordinary hyphens and convert them into a proper em dash** in Python, your terminal, or a document. No model, no automatic rewriting, no runtime dependencies.

## Install

After the first PyPI release:

```bash
pip install emdashify
```

Until then, install from the repository for development:

```bash
git clone https://github.com/edujbarrios/EmDashify.git
cd EmDashify
python -m pip install -e .
```

Requires Python 3.10 or later.

## Use it

**Python**

```python
from emdashify import convert

convert("Writing -- without hunting for a symbol")
# 'Writing — without hunting for a symbol'

convert("word--word", compact=True)
# 'word—word'
```

**Terminal**

```bash
emdashify "Writing -- without hunting for a symbol"
# Writing — without hunting for a symbol

printf 'Hello -- world\n' | emdashify
# Hello — world
```

**Files** (the original is never overwritten implicitly)

```bash
emdashify --file README.md --diff
emdashify --file notes.md --output notes-fixed.md
emdashify --file notes.md --check
```

`--check` exits with `1` if changes are needed, otherwise `0`. In Python, `check(text)` and `convert_file(path, output=...)` are also available.

## Predictable by design

By default, EmDashify only replaces **standalone `--` markers** (separated by whitespace or at the start/end of text). It leaves `--help`, `---`, dates, single hyphens, and hyphenated words unchanged. `--compact` / `compact=True` additionally converts `word--word` when both sides are letters.

For `.md` files, it also avoids changing fenced code blocks, indented code, and inline backtick spans. This is a lightweight Markdown safeguard, not a complete parser or a grammar checker. EmDashify **does not intercept keystrokes**: you explicitly run it on text you choose.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

For packaging and release instructions, see [RELEASING.md](https://github.com/edujbarrios/EmDashify/blob/main/docs/RELEASING.md).

## License and attribution

[BSD-3-Clause-Attribution](LICENSE). You may use, modify, and redistribute EmDashify under its terms. Redistributions must preserve the license notices **and** this acknowledgment:

> This product includes software developed by edujbarrios (https://github.com/edujbarrios/EmDashify).

Private use without redistribution does not require publicly displaying credit.
