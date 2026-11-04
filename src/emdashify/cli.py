"""Command-line interface for EmDashify."""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

from . import __version__
from .core import convert


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="emdashify",
        description="Convert explicit -- markers to an em dash (—).",
        epilog="Use --file for documents. Files are never changed unless --output is supplied.",
    )
    parser.add_argument("text", nargs="?", help="Text to convert; read standard input if omitted")
    parser.add_argument("--file", type=Path, metavar="PATH", help="Read a UTF-8 file")
    parser.add_argument("--output", type=Path, metavar="PATH", help="Write converted text to a file")
    parser.add_argument(
        "--compact", action="store_true", help="Also convert word--word (letters on each side)"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--markdown", action="store_true", help="Protect Markdown code spans and blocks")
    mode.add_argument("--plain", action="store_true", help="Treat input as plain text, even for .md files")
    parser.add_argument("--check", action="store_true", help="Exit 1 when conversion is needed; do not write")
    parser.add_argument("--diff", action="store_true", help="Show a unified diff instead of converted text")
    parser.add_argument("--version", action="version", version=f"emdashify {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI; return 0 on success or 1 if --check detects a change."""
    parser = _parser()
    args = parser.parse_args(argv)
    if args.file is not None and args.text is not None:
        parser.error("provide either text or --file, not both")
    if args.output is not None and args.file is None:
        parser.error("--output requires --file")
    if args.check and args.output is not None:
        parser.error("--check cannot be combined with --output")
    if args.diff and args.output is not None:
        parser.error("--diff cannot be combined with --output")
    if args.file is None and args.text is None and sys.stdin.isatty():
        parser.error("provide text, --file, or input via standard input")

    if args.file is not None:
        try:
            with args.file.open("r", encoding="utf-8", newline="") as stream:
                original = stream.read()
        except (OSError, UnicodeError) as exc:
            parser.exit(2, f"emdashify: {exc}\n")
        markdown = args.file.suffix.lower() in {".md", ".markdown", ".mdown"}
        label = str(args.file)
    elif args.text is not None:
        original = args.text
        markdown = False
        label = "text"
    else:
        original = sys.stdin.read()
        markdown = False
        label = "stdin"
    if args.markdown:
        markdown = True
    elif args.plain:
        markdown = False

    try:
        converted = convert(original, compact=args.compact, markdown=markdown)
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))

    changed = converted != original
    if args.diff:
        sys.stdout.writelines(
            difflib.unified_diff(
                original.splitlines(keepends=True),
                converted.splitlines(keepends=True),
                fromfile=label,
                tofile=f"{label} (emdashify)",
            )
        )
        return 1 if args.check and changed else 0
    if args.check:
        if changed:
            print(f"{label}: changes needed", file=sys.stderr)
            return 1
        print(f"{label}: no changes needed", file=sys.stderr)
        return 0
    if args.output is not None:
        try:
            with args.output.open("w", encoding="utf-8", newline="") as stream:
                stream.write(converted)
        except OSError as exc:
            parser.exit(2, f"emdashify: {exc}\n")
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(converted)
        if args.text is not None:
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
