"""Text conversion with a conservative default and Markdown-aware mode."""

from __future__ import annotations

import re
from pathlib import Path

EM_DASH = "\u2014"

# Only standalone double hyphens, not CLI flags, URLs, dates, or triple hyphens.
_STANDALONE = re.compile(r"(?<!\S)--(?!\S)")
# Opt-in: also accept two hyphens between alphabetic words (e.g. "hello--world").
_BETWEEN_LETTERS = re.compile(r"(?<=[^\W\d_])--(?=[^\W\d_])")
_BACKTICK_RUN = re.compile(r"`+")
_FENCE = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})(?P<info>[^\r\n]*)")
_INDENTED_CODE = re.compile(r"^(?: {4}|\t)")
_MARKDOWN_EXTENSIONS = {".md", ".markdown", ".mdown"}


def _convert_segment(text: str, compact: bool) -> str:
    result = _STANDALONE.sub(EM_DASH, text)
    if compact:
        result = _BETWEEN_LETTERS.sub(EM_DASH, result)
    return result


def _convert_outside_inline_code(text: str, compact: bool) -> str:
    """Preserve Markdown code spans, including spans using multiple backticks."""
    pieces: list[str] = []
    cursor = 0
    scan = 0
    while opening := _BACKTICK_RUN.search(text, scan):
        closing = next(
            (
                candidate
                for candidate in _BACKTICK_RUN.finditer(text, opening.end())
                if len(candidate.group()) == len(opening.group())
            ),
            None,
        )
        if closing is None:
            scan = opening.end()
            continue
        pieces.append(_convert_segment(text[cursor : opening.start()], compact))
        pieces.append(text[opening.start() : closing.end()])
        cursor = closing.end()
        scan = cursor
    pieces.append(_convert_segment(text[cursor:], compact))
    return "".join(pieces)


def _convert_markdown(text: str, compact: bool) -> str:
    """Leave fenced and indented code blocks and inline backtick spans unchanged."""
    result: list[str] = []
    prose: list[str] = []
    active_fence: tuple[str, int] | None = None

    def flush_prose() -> None:
        if prose:
            result.append(_convert_outside_inline_code("".join(prose), compact))
            prose.clear()

    for line in text.splitlines(keepends=True):
        # Strip only end-of-line characters to inspect a potential fence.
        content = line.rstrip("\r\n")
        matched = _FENCE.match(content)
        if active_fence is not None:
            flush_prose()
            result.append(line)
            if matched is not None:
                marker = matched.group("marker")
                info = matched.group("info")
                if (
                    marker[0] == active_fence[0]
                    and len(marker) >= active_fence[1]
                    and not info.strip()
                ):
                    active_fence = None
            continue
        if matched is not None:
            marker = matched.group("marker")
            info = matched.group("info")
            # Backtick fences cannot include backticks in their info string.
            if marker[0] == "~" or "`" not in info:
                flush_prose()
                result.append(line)
                active_fence = (marker[0], len(marker))
                continue
        if _INDENTED_CODE.match(content):
            flush_prose()
            result.append(line)
            continue
        prose.append(line)

    flush_prose()
    return "".join(result)


def convert(text: str, *, compact: bool = False, markdown: bool = False) -> str:
    """Convert explicit double-hyphen markers to the Unicode em dash (U+2014).

    Default behavior converts only standalone ``--`` markers delimited by
    whitespace or string boundaries. It preserves spacing and leaves ``---``,
    ``--help``, hyphenated names, dates, and arithmetic unchanged.

    ``compact=True`` additionally converts ``word--word`` (letters on both
    sides). ``markdown=True`` protects fenced/indented code and backtick spans.
    No automatic language or AI-generated-text detection is performed.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if markdown:
        return _convert_markdown(text, compact)
    return _convert_segment(text, compact)


def check(text: str, *, compact: bool = False, markdown: bool = False) -> bool:
    """Return True if converting the supplied text would change it."""
    return convert(text, compact=compact, markdown=markdown) != text


def convert_file(
    path: str | Path,
    *,
    output: str | Path | None = None,
    compact: bool = False,
    markdown: bool | None = None,
) -> str:
    """Convert a UTF-8 text file and optionally write a UTF-8 output file.

    With ``output=None`` the original file is not changed. Markdown detection
    is based on the input extension unless ``markdown`` is explicitly given.
    Newline characters are preserved.
    """
    source = Path(path)
    with source.open("r", encoding="utf-8", newline="") as stream:
        original = stream.read()
    use_markdown = source.suffix.lower() in _MARKDOWN_EXTENSIONS if markdown is None else markdown
    result = convert(original, compact=compact, markdown=use_markdown)
    if output is not None:
        with Path(output).open("w", encoding="utf-8", newline="") as stream:
            stream.write(result)
    return result
