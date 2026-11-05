"""Regression tests for EmDashify's conversion rules."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from emdashify import EM_DASH, check, convert, convert_file


class ConversionTests(unittest.TestCase):
    def test_unicode_character(self) -> None:
        self.assertEqual(EM_DASH, "\u2014")

    def test_standalone_marker(self) -> None:
        self.assertEqual(convert("Hello -- world"), "Hello—world")

    def test_marker_alone(self) -> None:
        self.assertEqual(convert("--"), "—")

    def test_marker_at_start(self) -> None:
        self.assertEqual(convert("-- hello"), "—hello")

    def test_marker_at_end(self) -> None:
        self.assertEqual(convert("hello --"), "hello—")

    def test_multiple_markers(self) -> None:
        self.assertEqual(convert("a -- b -- c"), "a—b—c")

    def test_newline_delimiters(self) -> None:
        self.assertEqual(convert("a\n--\nb"), "a\n—\nb")

    def test_preserve_crlf(self) -> None:
        self.assertEqual(convert("hello -- world\r\n"), "hello—world\r\n")

    def test_compact_strips_only_horizontal_spacing(self) -> None:
        self.assertEqual(convert("Hello   --   world"), "Hello—world")

    def test_spaced_mode_preserves_whitespace(self) -> None:
        self.assertEqual(convert("Hello -- world", compact=False), "Hello — world")
        self.assertEqual(convert("hello--world", compact=False), "hello--world")
        self.assertEqual(convert("Hello   --   world", compact=False), "Hello   —   world")

    def test_dont_eat_newlines(self) -> None:
        self.assertEqual(convert("Hello --\nworld"), "Hello—\nworld")

    def test_repeated_markers(self) -> None:
        self.assertEqual(convert("one -- -- two"), "one——two")

    def test_single_dash(self) -> None:
        self.assertEqual(convert("a - b"), "a - b")

    def test_triple_dash(self) -> None:
        self.assertEqual(convert("a --- b"), "a --- b")

    def test_cli_flag(self) -> None:
        self.assertEqual(convert("--help --version"), "--help --version")

    def test_date(self) -> None:
        self.assertEqual(convert("2026-11-04"), "2026-11-04")

    def test_hyphenated_words(self) -> None:
        self.assertEqual(convert("state-of-the-art"), "state-of-the-art")

    def test_compact_by_default(self) -> None:
        self.assertEqual(convert("hello--world"), "hello—world")

    def test_compact_mode(self) -> None:
        self.assertEqual(convert("hello--world", compact=True), "hello—world")

    def test_compact_mode_unicode(self) -> None:
        self.assertEqual(convert("café--mañana", compact=True), "café—mañana")

    def test_compact_mode_preserves_flags(self) -> None:
        self.assertEqual(convert("--help", compact=True), "--help")

    def test_compact_mode_preserves_triples(self) -> None:
        self.assertEqual(convert("hello---world", compact=True), "hello---world")

    def test_compact_mode_preserves_numbers(self) -> None:
        self.assertEqual(convert("a--1 and 2--b", compact=True), "a--1 and 2--b")

    def test_idempotent(self) -> None:
        first = convert("a -- b", compact=True)
        self.assertEqual(convert(first, compact=True), first)

    def test_type_error(self) -> None:
        with self.assertRaisesRegex(TypeError, "text must be a str"):
            convert(None)  # type: ignore[arg-type]

    def test_check_when_needed(self) -> None:
        self.assertTrue(check("hello -- world"))

    def test_check_when_unchanged(self) -> None:
        self.assertFalse(check("hello — world"))


class MarkdownTests(unittest.TestCase):
    def test_fenced_backtick_code(self) -> None:
        text = "Before -- here\n```sh\necho a -- b\n```\nAfter -- here\n"
        self.assertEqual(
            convert(text, markdown=True),
            "Before—here\n```sh\necho a -- b\n```\nAfter—here\n",
        )

    def test_fenced_tilde_code(self) -> None:
        text = "~~~\nx -- y\n~~~\nhello -- world"
        self.assertEqual(convert(text, markdown=True), "~~~\nx -- y\n~~~\nhello—world")

    def test_inline_code(self) -> None:
        text = "Use `echo -- help` but a -- b"
        self.assertEqual(convert(text, markdown=True), "Use `echo -- help` but a—b")

    def test_double_backtick_inline(self) -> None:
        text = "Use ``foo ` -- bar`` then -- here"
        self.assertEqual(convert(text, markdown=True), "Use ``foo ` -- bar`` then—here")

    def test_indented_code(self) -> None:
        text = "A -- B\n    a -- b\n\tfoo -- bar\nNext -- line"
        self.assertEqual(convert(text, markdown=True), "A—B\n    a -- b\n\tfoo -- bar\nNext—line")

    def test_plain_mode_does_not_protect_code(self) -> None:
        self.assertEqual(convert("`a -- b`"), "`a—b`")

    def test_unclosed_fence(self) -> None:
        text = "start -- here\n```\na -- b\n"
        self.assertEqual(convert(text, markdown=True), "start—here\n```\na -- b\n")

    def test_closing_fence_length(self) -> None:
        text = "````\na -- b\n```\na -- c\n````\nd -- e"
        self.assertEqual(convert(text, markdown=True), "````\na -- b\n```\na -- c\n````\nd—e")

    def test_markdown_check_ignores_code(self) -> None:
        self.assertFalse(check("```bash\necho a -- b\n```", markdown=True))

    def test_markdown_compact(self) -> None:
        self.assertEqual(convert("a--b and `a--b`", compact=True, markdown=True), "a—b and `a--b`")


class FileTests(unittest.TestCase):
    def test_convert_file_without_output_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            source = Path(root, "notes.txt")
            source.write_text("hello -- world", encoding="utf-8")
            self.assertEqual(convert_file(source), "hello—world")
            self.assertEqual(source.read_text(encoding="utf-8"), "hello -- world")

    def test_convert_file_with_output(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            source = Path(root, "notes.txt")
            target = Path(root, "output.txt")
            source.write_text("hello -- world", encoding="utf-8")
            self.assertEqual(convert_file(source, output=target), "hello—world")
            self.assertEqual(target.read_text(encoding="utf-8"), "hello—world")

    def test_markdown_auto_detected(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            source = Path(root, "notes.md")
            source.write_text("`echo -- help`\nHello -- world", encoding="utf-8")
            self.assertEqual(convert_file(source), "`echo -- help`\nHello—world")

    def test_markdown_override(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            source = Path(root, "notes.md")
            source.write_text("`echo -- help`", encoding="utf-8")
            self.assertEqual(convert_file(source, markdown=False), "`echo—help`")

    def test_file_preserves_crlf(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            source = Path(root, "in.txt")
            target = Path(root, "out.txt")
            source.write_bytes(b"Hello -- world\r\nAgain -- here\r\n")
            convert_file(source, output=target)
            self.assertEqual(target.read_bytes(), "Hello—world\r\nAgain—here\r\n".encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
