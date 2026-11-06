"""Regression tests for backup-protected, opt-in file editing."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from emdashify import convert_in_place

try:
    from docx import Document
except ImportError:
    Document = None


class InPlaceTests(unittest.TestCase):
    @staticmethod
    def cli(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "emdashify", *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_text_in_place_keeps_original_bytes_and_newlines(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "notes.txt")
            original = b"Hello -- world\r\nKeep --help and ---\r\n"
            path.write_bytes(original)
            self.assertTrue(convert_in_place(path))
            self.assertEqual(path.read_bytes(), "Hello—world\r\nKeep --help and ---\r\n".encode())
            self.assertEqual(Path(str(path) + ".bak").read_bytes(), original)

    def test_markdown_ignores_code_and_keeps_backup(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "notes.md")
            original = "Hello -- world\n`--`\n```sh\necho -- help\n```\n"
            path.write_text(original, encoding="utf-8")
            self.assertTrue(convert_in_place(path))
            self.assertEqual(
                path.read_text(encoding="utf-8"),
                "Hello—world\n`--`\n```sh\necho -- help\n```\n",
            )
            self.assertEqual(Path(str(path) + ".bak").read_text(encoding="utf-8"), original)

    def test_unchanged_file_creates_no_backup(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "notes.txt")
            path.write_text("No dashes to convert", encoding="utf-8")
            self.assertFalse(convert_in_place(path))
            self.assertFalse(Path(str(path) + ".bak").exists())

    def test_existing_backup_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "notes.txt")
            backup = Path(str(path) + ".bak")
            path.write_text("Hello -- world", encoding="utf-8")
            backup.write_text("PREVIOUS BACKUP", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                convert_in_place(path)
            self.assertEqual(path.read_text(encoding="utf-8"), "Hello -- world")
            self.assertEqual(backup.read_text(encoding="utf-8"), "PREVIOUS BACKUP")
            self.assertEqual(list(Path(root).glob(".notes.txt.*")), [])

    def test_spaced_opt_out(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "notes.txt")
            path.write_text("Hello -- world and word--word", encoding="utf-8")
            self.assertTrue(convert_in_place(path, compact=False))
            self.assertEqual(path.read_text(encoding="utf-8"), "Hello — world and word--word")

    def test_refuse_symlinks(self):
        with tempfile.TemporaryDirectory() as root:
            target = Path(root, "target.txt")
            source = Path(root, "shortcut.txt")
            target.write_text("Hello -- world", encoding="utf-8")
            try:
                source.symlink_to(target)
            except (NotImplementedError, OSError):
                self.skipTest("Symlinks unavailable")
            with self.assertRaisesRegex(ValueError, "symlinks"):
                convert_in_place(source)
            self.assertEqual(target.read_text(encoding="utf-8"), "Hello -- world")

    def test_permissions_are_preserved(self):
        if os.name == "nt":
            self.skipTest("Permission modes are platform-specific")
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "notes.txt")
            path.write_text("Hello -- world", encoding="utf-8")
            path.chmod(0o640)
            self.assertTrue(convert_in_place(path))
            self.assertEqual(path.stat().st_mode & 0o777, 0o640)

    def test_cli_in_place(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "notes.txt")
            path.write_text("Hello -- world", encoding="utf-8")
            result = self.cli("--file", str(path), "--in-place")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("backup:", result.stderr)
            self.assertEqual(path.read_text(encoding="utf-8"), "Hello—world")
            self.assertEqual(Path(str(path) + ".bak").read_text(encoding="utf-8"), "Hello -- world")
            second = self.cli("--file", str(path), "--in-place")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("no changes needed", second.stderr)

    def test_cli_rejects_unsafe_combinations(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "notes.txt")
            path.write_text("Hello -- world", encoding="utf-8")
            for args in [
                ("--in-place",),
                ("--file", str(path), "--in-place", "--output", str(path)),
                ("--file", str(path), "--in-place", "--check"),
                ("--file", str(path), "--in-place", "--diff"),
                ("--file", str(path), "--output", str(path)),
            ]:
                with self.subTest(args=args):
                    result = self.cli(*args)
                    self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(path.read_text(encoding="utf-8"), "Hello -- world")

    @unittest.skipUnless(Document is not None, "Install emdashify[word] for Word tests")
    def test_word_in_place_preserves_styles_and_backup(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "document.docx")
            document = Document()
            paragraph = document.add_paragraph()
            paragraph.add_run("Before ")
            paragraph.add_run("-").bold = True
            paragraph.add_run("- after").italic = True
            document.add_table(rows=1, cols=1).cell(0, 0).text = "Table -- here"
            document.save(path)
            original = path.read_bytes()
            self.assertTrue(convert_in_place(path))
            self.assertEqual(Path(str(path) + ".bak").read_bytes(), original)
            result = Document(path)
            self.assertEqual(result.paragraphs[0].text, "Before—after")
            self.assertTrue(result.paragraphs[0].runs[1].bold)
            self.assertTrue(result.paragraphs[0].runs[2].italic)
            self.assertEqual(result.tables[0].cell(0, 0).text, "Table—here")
            self.assertFalse(convert_in_place(path))

    @unittest.skipUnless(Document is not None, "Install emdashify[word] for Word tests")
    def test_cli_word_in_place(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "document.docx")
            document = Document()
            document.add_paragraph("Before -- after")
            document.save(path)
            result = self.cli("--file", str(path), "--in-place")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(Document(path).paragraphs[0].text, "Before—after")
            self.assertEqual(Document(str(path) + ".bak").paragraphs[0].text, "Before -- after")


if __name__ == "__main__":
    unittest.main()
