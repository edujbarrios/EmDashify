"""End-to-end tests for the command-line interface."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CLITests(unittest.TestCase):
    @staticmethod
    def run_cli(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "emdashify", *args],
            input=stdin,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_literal_text(self) -> None:
        result = self.run_cli("Hello -- world")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "Hello — world\n")

    def test_standard_input(self) -> None:
        result = self.run_cli(stdin="Hello -- world\n")
        self.assertEqual(result.stdout, "Hello — world\n")

    def test_compact(self) -> None:
        result = self.run_cli("hello--world", "--compact")
        self.assertEqual(result.stdout, "hello—world\n")

    def test_markdown_flag(self) -> None:
        result = self.run_cli("`hello -- world`", "--markdown")
        self.assertEqual(result.stdout, "`hello -- world`\n")

    def test_check_changes(self) -> None:
        result = self.run_cli("Hello -- world", "--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("changes needed", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_check_clean(self) -> None:
        result = self.run_cli("Hello — world", "--check")
        self.assertEqual(result.returncode, 0)
        self.assertIn("no changes needed", result.stderr)

    def test_diff(self) -> None:
        result = self.run_cli("Hello -- world", "--diff")
        self.assertEqual(result.returncode, 0)
        self.assertIn("-Hello -- world", result.stdout)
        self.assertIn("+Hello — world", result.stdout)

    def test_check_with_diff(self) -> None:
        result = self.run_cli("Hello -- world", "--diff", "--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("+Hello — world", result.stdout)

    def test_file_auto_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            source = Path(root, "notes.md")
            source.write_text("Hello -- world\n`echo -- help`\n", encoding="utf-8")
            result = self.run_cli("--file", str(source))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "Hello — world\n`echo -- help`\n")

    def test_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            source = Path(root, "notes.md")
            target = Path(root, "fixed.md")
            source.write_text("Hello -- world", encoding="utf-8")
            result = self.run_cli("--file", str(source), "--output", str(target))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertEqual(target.read_text(encoding="utf-8"), "Hello — world")
            self.assertEqual(source.read_text(encoding="utf-8"), "Hello -- world")

    def test_plain_override(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            source = Path(root, "notes.md")
            source.write_text("`Hello -- world`", encoding="utf-8")
            result = self.run_cli("--file", str(source), "--plain")
            self.assertEqual(result.stdout, "`Hello — world`")

    def test_output_requires_file(self) -> None:
        result = self.run_cli("Hello -- world", "--output", "hello.txt")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--output requires --file", result.stderr)

    def test_check_disallows_output(self) -> None:
        result = self.run_cli("--file", "ignored.md", "--check", "--output", "out.md")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--check cannot be combined", result.stderr)

    def test_missing_file_reports_clean_error(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            missing = Path(root, "missing.md")
            result = self.run_cli("--file", str(missing))
            self.assertEqual(result.returncode, 2)
            self.assertIn("emdashify:", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_version(self) -> None:
        result = self.run_cli("--version")
        self.assertEqual(result.stdout, "emdashify 0.2.0\n")

    def test_positional_disallows_file(self) -> None:
        result = self.run_cli("hello", "--file", "ignored.md")
        self.assertEqual(result.returncode, 2)
        self.assertIn("either text or --file", result.stderr)


    def test_docx_cli(self) -> None:
        try:
            from docx import Document
        except ImportError:
            self.skipTest("Install word extra for document integration")
        with tempfile.TemporaryDirectory() as root:
            source, output = Path(root,"a.docx"),Path(root,"b.docx")
            doc=Document();doc.add_paragraph("One -- two");doc.save(source)
            self.assertEqual(self.run_cli("--file",str(source),"--check").returncode,1)
            self.assertEqual(self.run_cli("--file",str(source)).returncode,2)
            result=self.run_cli("--file",str(source),"--output",str(output))
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(Document(output).paragraphs[0].text,"One — two")
            self.assertEqual(Document(source).paragraphs[0].text,"One -- two")
            self.assertEqual(self.run_cli("--file",str(output),"--check").returncode,0)

    def test_docx_cli_rejects_diff(self) -> None:
        result=self.run_cli("--file","whatever.docx","--diff")
        self.assertEqual(result.returncode,2)
        self.assertIn("not supported",result.stderr)

if __name__ == "__main__":
    unittest.main()
