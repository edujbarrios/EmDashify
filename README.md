# EmDashify — type `--`, get `—`

**The simplest way to turn two hyphens into an em dash.**

AI writing has made the em dash (`—`, Unicode U+2014) more noticeable. ChatGPT and other language models often use it, but it is a normal punctuation mark — not an AI watermark or proof that a passage was machine-generated.

You shouldn't need an AI model, a character picker, or a special keyboard shortcut just to type one. **EmDashify** turns an explicit `--` into `—` in Python strings, terminal input, and text or Markdown files.

- **Simple:** one function, `convert(text)`, and one command, `emdashify`.
- **Predictable:** only deliberate markers are replaced by default.
- **Markdown-aware:** code blocks and inline code are protected when enabled.
- **Lightweight:** zero runtime dependencies and no AI service, network access, or telemetry.

## Install for development

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/edujbarrios/EmDashify.git
cd EmDashify
python -m pip install -e .
```

EmDashify requires Python 3.10 or newer. It is **not published to PyPI yet**; `pip install emdashify` is not an installation instruction for this version.

## Python API

```python
from emdashify import convert, check, EM_DASH

convert("Writing -- without a character picker")
# 'Writing — without a character picker'

check("Writing -- without a character picker")
# True

EM_DASH
# '—'
```

By default, EmDashify converts **standalone** `--` markers at string or whitespace boundaries. It does not try to guess whether every hyphen is an em dash:

```python
convert("hello -- world")    # 'hello — world'
convert("hello--world")      # 'hello--world'
convert("--help -- 2026-11-04") # '--help — 2026-11-04'
convert("a - b")             # 'a - b'
convert("---")               # '---'
```

Need to write without spaces around the marker? Opt into `compact=True` for double hyphens **between letters**:

```python
convert("hello--world", compact=True)
# 'hello—world'
```

Even in compact mode, `--help`, `---`, and `2026-11-04` stay unchanged. EmDashify leaves surrounding whitespace as written; it is a converter, not a grammar checker.

### Markdown-aware conversion

~~~python
markdown = """A paragraph -- with a dash.

`echo --help` stays intact.

```bash
printf 'a -- b'
```
"""

print(convert(markdown, markdown=True))
~~~

The paragraph marker converts, while inline backtick spans, fenced code blocks, and indented code blocks are preserved. Markdown mode is a lightweight safeguard, **not** a full Markdown parser. Review diffs before editing important documents.

### Files

```python
from emdashify import convert_file

result = convert_file("README.md")  # Read and convert; never overwrite the source.
convert_file("notes.md", output="notes-fixed.md")
```

Files are read and written as UTF-8. Markdown mode is automatically enabled for `.md`, `.markdown`, and `.mdown` paths, and can be overridden with `markdown=False` or `markdown=True`. Line endings are preserved.

## Command line

```bash
emdashify "Hello -- world"
# Hello — world

printf 'Hello -- world\n' | emdashify
# Hello — world

emdashify --file README.md --diff
emdashify --file notes.md --output notes-fixed.md
emdashify --file notes.md --check
```

The CLI prints converted text to stdout unless you specify `--output`. It **never overwrites a file implicitly**. `--check` returns exit code `1` if any conversion would be made and `0` otherwise, making it useful in scripts and CI. `--diff` shows a unified diff; it can be combined with `--check`.

Additional options:

```bash
emdashify "word--word" --compact
emdashify --file document.txt --markdown
emdashify --file document.md --plain
python -m emdashify "Hello -- world"
```

### What changes?

| Input | Default output | Compact output |
| --- | --- | --- |
| `Hello -- world` | `Hello — world` | `Hello — world` |
| `Hello--world` | unchanged | `Hello—world` |
| `--help` | unchanged | unchanged |
| `a - b` | unchanged | unchanged |
| `---` | unchanged | unchanged |
| `2026-11-04` | unchanged | unchanged |

**Why not replace every `-`?** Because hyphens are essential in command-line flags, filenames, dates, code, and ordinary words. A converter that blindly changes them would damage the text it is meant to improve.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
emdashify --version
```

This project intentionally uses the Python standard library for tests and runtime functionality. GitHub Actions runs the same tests on Python 3.10 through 3.13.

## Philosophy

The em dash existed long before large language models, and a dash is not an AI detector. EmDashify embraces its visibility in modern AI-assisted writing while solving a small, practical keyboard problem: **two easy keystrokes in, one proper em dash out.**

No model. No magic. Just punctuation.

## License and attribution

EmDashify is licensed under the **BSD 3-Clause Attribution License**
(SPDX: `BSD-3-Clause-Attribution`). See [LICENSE](LICENSE).

You may use, modify, and redistribute EmDashify, including in commercial
projects, under the conditions in the license. When you **redistribute**
EmDashify in source or binary form, including as part of another product, you
must retain the following acknowledgment:

> This product includes software developed by edujbarrios
> (https://github.com/edujbarrios/EmDashify).

An acknowledgments page, third-party notices file, or distributed
documentation is an appropriate place for the credit. Preserve the license
and copyright notices as well. **Private use without redistribution does not
trigger a public attribution requirement.**
