"""Conservative .docx conversion, preserving Word's run-level formatting.

Requires optional ``emdashify[word]``; the plain-text API has no dependencies.
"""
from __future__ import annotations

from bisect import bisect_right
from pathlib import Path
import re
from typing import Any

from .core import EM_DASH, _BETWEEN_LETTERS, _STANDALONE

_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
_PART = re.compile(r"^/word/(?:document|header\d+|footer\d+|footnotes|endnotes|comments)\.xml$")
_STOP = {_W + name for name in ("tab", "br", "cr", "fldChar", "instrText", "drawing", "object", "delText")}
_SKIP = {_W + name for name in ("del", "ins", "moveFrom", "moveTo", "fldSimple")}


def _is_visible(node: Any, paragraph: Any) -> bool:
    parent = node.getparent()
    while parent is not None and parent is not paragraph:
        if parent.tag in _SKIP or parent.tag == _W + "p":
            return False
        parent = parent.getparent()
    return parent is paragraph


def _segments(paragraph: Any) -> list[list[Any]]:
    """Join text nodes across runs, but never cross tabs, breaks, or fields."""
    groups: list[list[Any]] = []
    current: list[Any] = []
    for node in paragraph.iter():
        if node is paragraph or node.tag not in _STOP | {_W + "t"}:
            continue
        if not _is_visible(node, paragraph):
            continue
        if node.tag in _STOP:
            if current:
                groups.append(current)
                current = []
        else:
            current.append(node)
    if current:
        groups.append(current)
    return groups


def _convert_nodes(nodes: list[Any], compact: bool) -> int:
    """Replace dash pairs, retaining the first dash's existing run styling."""
    original = "".join(node.text or "" for node in nodes)
    if "--" not in original:
        return 0
    matches = list(_STANDALONE.finditer(original))
    if compact:
        matches.extend(_BETWEEN_LETTERS.finditer(original))
    if not matches:
        return 0
    ends: list[int] = []
    chars: list[list[str]] = []
    length = 0
    for node in nodes:
        value = node.text or ""
        length += len(value)
        ends.append(length)
        chars.append(list(value))
    for match in matches:
        first, second = match.start(), match.start() + 1
        i, j = bisect_right(ends, first), bisect_right(ends, second)
        offset_i = first - (ends[i - 1] if i else 0)
        offset_j = second - (ends[j - 1] if j else 0)
        chars[i][offset_i] = EM_DASH
        chars[j][offset_j] = ""
    for node, value in zip(nodes, chars):
        updated = "".join(value)
        if updated != (node.text or ""):
            node.text = updated
            if updated[:1].isspace() or updated[-1:].isspace():
                node.set(_SPACE, "preserve")
    return len(matches)


def _convert_xml(root: Any, compact: bool) -> int:
    return sum(_convert_nodes(group, compact) for p in root.iter(_W + "p") for group in _segments(p))


def _process(path: Path, output: Path | None, compact: bool) -> int:
    # Import only when the Word API is called: the core package stays lightweight.
    try:
        from docx import Document
        from lxml import etree
    except ImportError as exc:
        raise RuntimeError('Word support requires: pip install "emdashify[word]"') from exc
    if path.suffix.lower() != ".docx":
        raise ValueError("source must be a .docx Word document")
    if output is not None:
        if output.suffix.lower() != ".docx":
            raise ValueError("output must end in .docx")
        if path.resolve() == output.resolve():
            raise ValueError("output must be different from the source file")
    document = Document(path)
    count = 0
    for part in document.part.package.parts:
        if not _PART.fullmatch(str(part.partname)):
            continue
        structured = hasattr(part, "element")
        root = part.element if structured else etree.fromstring(part.blob)
        changes = _convert_xml(root, compact)
        count += changes
        if changes and not structured:
            part._blob = etree.tostring(root, encoding="UTF-8", xml_declaration=True)
    if output is not None:
        document.save(output)
    return count


def convert_docx(path: str | Path, output: str | Path, *, compact: bool = False) -> Path:
    """Convert a complete Word document to a new .docx, preserving formatting.

    Covers body paragraphs, tables, headers/footers, textboxes, and supported
    footnotes/comments. Never overwrites the original file. Review documents
    containing tracked changes or advanced fields after conversion.
    """
    source, destination = Path(path), Path(output)
    _process(source, destination, compact)
    return destination


def check_docx(path: str | Path, *, compact: bool = False) -> bool:
    """Report whether a .docx contains convertible markers, without saving."""
    return _process(Path(path), None, compact) > 0
