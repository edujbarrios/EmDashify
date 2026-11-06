"""Opt-in, backup-protected in-place conversion for text and Word documents."""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

from .core import _MARKDOWN_EXTENSIONS, convert


def convert_in_place(
    path: str | Path,
    *,
    compact: bool = True,
    markdown: bool | None = None,
) -> bool:
    """Convert a file in place, retaining the original as a .bak file.

    Returns True when the file changes, False when no changes are needed.
    Existing backups are never overwritten. An intermediate file in the same
    directory is used to avoid truncating the source on failed conversion.
    Symlinks are rejected to avoid unexpectedly replacing a link.
    Word .docx support requires the optional emdashify[word] extra.
    """
    source = Path(path)
    if source.is_symlink():
        raise ValueError("in-place conversion does not support symlinks")
    if not source.is_file():
        raise ValueError(f"not a regular file: {source}")

    is_word = source.suffix.lower() == ".docx"
    if is_word:
        if markdown is not None:
            raise ValueError("Markdown mode is not supported for Word documents")
        from .word import check_docx, convert_docx

        if not check_docx(source, compact=compact):
            return False
    else:
        with source.open("r", encoding="utf-8", newline="") as stream:
            original = stream.read()
        use_markdown = (
            source.suffix.lower() in _MARKDOWN_EXTENSIONS
            if markdown is None
            else markdown
        )
        converted = convert(original, compact=compact, markdown=use_markdown)
        if original == converted:
            return False

    backup = source.with_name(source.name + ".bak")
    fd, temporary_path = tempfile.mkstemp(
        dir=source.parent,
        prefix=f".{source.name}.",
        suffix=".docx" if is_word else ".tmp",
    )
    os.close(fd)
    temporary = Path(temporary_path)
    try:
        if is_word:
            convert_docx(source, temporary, compact=compact)
        else:
            with temporary.open("w", encoding="utf-8", newline="") as stream:
                stream.write(converted)

        shutil.copymode(source, temporary)
        created_backup = False
        try:
            with backup.open("xb") as backup_stream:
                created_backup = True
                with source.open("rb") as original_stream:
                    shutil.copyfileobj(original_stream, backup_stream)
            shutil.copystat(source, backup)
        except Exception:
            if created_backup:
                backup.unlink(missing_ok=True)
            raise

        os.replace(temporary, source)
    finally:
        temporary.unlink(missing_ok=True)
    return True
