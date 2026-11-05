"""End-to-end Word conversion tests."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from emdashify import check_docx, convert_docx
try:
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
except ImportError:
    Document = None


@unittest.skipUnless(Document is not None, "Install emdashify[word] for Word tests")
class WordTests(unittest.TestCase):
    def test_full_document_and_formatting(self):
        with tempfile.TemporaryDirectory() as root:
            source, target = Path(root, "in.docx"), Path(root, "out.docx")
            d = Document()
            p = d.add_paragraph();p.add_run("Before ");p.add_run("-").bold=True;p.add_run("- after").italic=True
            d.add_paragraph("Keep --help, --- and 2026-11-05")
            d.add_table(rows=1, cols=1).cell(0, 0).text = "Table -- here"
            d.sections[0].header.paragraphs[0].text = "Header -- here"
            d.sections[0].footer.paragraphs[0].text = "Footer -- here"
            d.save(source)
            self.assertTrue(check_docx(source))
            self.assertEqual(convert_docx(source, target),target)
            self.assertFalse(check_docx(target))
            self.assertEqual(Document(source).paragraphs[0].text,"Before -- after")
            changed=Document(target)
            self.assertEqual(changed.paragraphs[0].text,"Before—after")
            self.assertTrue(changed.paragraphs[0].runs[1].bold)
            self.assertTrue(changed.paragraphs[0].runs[2].italic)
            self.assertEqual(changed.paragraphs[1].text,"Keep --help, --- and 2026-11-05")
            self.assertEqual(changed.tables[0].cell(0,0).text,"Table—here")
            self.assertEqual(changed.sections[0].header.paragraphs[0].text,"Header—here")
            self.assertEqual(changed.sections[0].footer.paragraphs[0].text,"Footer—here")

    def test_compact_and_same_path(self):
        with tempfile.TemporaryDirectory() as root:
            p, out = Path(root,"a.docx"),Path(root,"b.docx")
            d=Document();d.add_paragraph("hello--world and --help and ---");d.save(p)
            self.assertFalse(check_docx(p, compact=False))
            self.assertTrue(check_docx(p))
            convert_docx(p,out)
            self.assertEqual(Document(out).paragraphs[0].text,"hello—world and --help and ---")
            with self.assertRaisesRegex(ValueError,"different"):
                convert_docx(p,p)

    def test_spaced_opt_out_preserves_original_style(self):
        with tempfile.TemporaryDirectory() as root:
            source, target = Path(root, "input.docx"), Path(root, "output.docx")
            document = Document()
            document.add_paragraph("Hello -- world and word--word")
            document.save(source)
            convert_docx(source, target, compact=False)
            self.assertEqual(
                Document(target).paragraphs[0].text,
                "Hello — world and word--word",
            )

    def test_compact_spans_formatting_runs(self):
        with tempfile.TemporaryDirectory() as root:
            source, target = Path(root, "input.docx"), Path(root, "output.docx")
            document = Document()
            paragraph = document.add_paragraph()
            paragraph.add_run("One ")
            paragraph.add_run("-").bold = True
            paragraph.add_run("- two").italic = True
            document.save(source)
            convert_docx(source, target)
            converted = Document(target)
            self.assertEqual(converted.paragraphs[0].text, "One—two")
            self.assertTrue(converted.paragraphs[0].runs[1].bold)
            self.assertTrue(converted.paragraphs[0].runs[2].italic)

    def test_invalid_extension(self):
        with self.assertRaisesRegex(ValueError,".docx"):
            convert_docx("old.doc","out.docx")

    def test_hyperlinks_and_metadata(self):
        with tempfile.TemporaryDirectory() as root:
            p,out=Path(root,"a.docx"),Path(root,"b.docx")
            d=Document();par=d.add_paragraph("Before -- after ")
            link=OxmlElement("w:hyperlink");link.set(qn("w:anchor"),"bookmark")
            run=OxmlElement("w:r");node=OxmlElement("w:t");node.text="Label -- here";run.append(node);link.append(run);par._p.append(link)
            d.core_properties.title="Title -- should not change";d.save(p)
            convert_docx(p,out)
            result=Document(out)
            self.assertEqual(result.paragraphs[0].text,"Before—after Label—here")
            self.assertEqual(result.core_properties.title,"Title -- should not change")
            self.assertEqual(len(result.paragraphs[0].hyperlinks),1)
