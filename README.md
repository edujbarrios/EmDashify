# EmDashify — `--` → `—`

**The most unnecessary Python library you'll actually use.**

LLMs made the em dash (`—`) hard to ignore. Most QWERTY keyboards still don't have a key for it.

**EmDashify** turns two ordinary hyphens into an em dash in your text, Markdown, or terminal. No AI. No dependencies. Just punctuation.

## Quick start

```bash
pip install emdashify
emdashify "Hello -- world"
# Hello — world
```

```python
from emdashify import convert

convert("Hello -- world")             # "Hello — world"
convert("hello--world", compact=True) # "hello—world"
```

> Before the first PyPI release, install from a local checkout with `python -m pip install -e .`. Requires Python 3.10+.

## Files

```bash
emdashify --file notes.md --diff
emdashify --file notes.md --output notes-fixed.md
emdashify --file notes.md --check
```

**Safe by default:** only standalone `--` markers are converted. Flags such as `--help`, dates, and `---` stay unchanged. For Markdown files, common code spans and blocks are protected. Files are never overwritten implicitly.

`--compact` also converts `word--word`. Use `check(text)` and `convert_file(path)` from Python when needed.

## License

[BSD-3-Clause-Attribution](LICENSE). Redistributions must retain the license notices and this acknowledgment:

> This product includes software developed by edujbarrios (https://github.com/edujbarrios/EmDashify).

For development and publishing, see [RELEASING.md](docs/RELEASING.md).
