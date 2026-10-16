import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from ats_optimizer import (
    ATSOptimizer, DocumentReadError, InvalidInputError,
    MissingOptionalDependencyError, UnsupportedFileTypeError, read_document,
)


class PublicApiTests(unittest.TestCase):
    def setUp(self):
        self.optimizer = ATSOptimizer()

    def test_analysis_exposes_typed_results_and_legacy_score(self):
        result = self.optimizer.analyze(
            resume="Python and SQL experience",
            job_description="Python, SQL, and Docker skills",
        )
        self.assertEqual(result.score, 67)
        self.assertEqual(result.status, "Excellent")
        self.assertEqual(result.matched_skills, ("python", "sql"))
        self.assertEqual(result.missing_skills, ("docker",))
        self.assertEqual(result.total_required_skills, 3)
        self.assertEqual(result.total_matching_skills, 2)
        self.assertEqual(result.total_missing_skills, 1)

    def test_result_is_json_serializable_and_response_compatible(self):
        value = self.optimizer.analyze("Python", "Python and SQL").to_dict()
        self.assertEqual(value["resume_score_in_percentage"], 50)
        self.assertEqual(value["total_required_skills_in_job_description"], 2)
        self.assertEqual(value["comma_separated_missing_skills"], "sql")
        json.dumps(value)

    def test_no_recognized_skills_warns(self):
        result = self.optimizer.analyze("Python", "Toronto in January")
        self.assertEqual(result.score, 0)
        self.assertEqual(result.skills, ())
        self.assertIsNotNone(result.warning)

    def test_empty_and_invalid_inputs_are_actionable(self):
        for resume, job in [("", "Python"), ("Python", "  "), (None, "Python")]:
            with self.subTest(resume=resume, job=job):
                with self.assertRaises(InvalidInputError):
                    self.optimizer.analyze(resume, job)  # type: ignore[arg-type]

    def test_string_that_looks_like_path_remains_text(self):
        result = self.optimizer.analyze("missing-resume.pdf", "Python")
        self.assertEqual(result.score, 0)


class DocumentTests(unittest.TestCase):
    def test_utf8_text_path_can_be_analyzed(self):
        with TemporaryDirectory() as folder:
            resume = Path(folder, "resume.txt")
            resume.write_text("Python developer", encoding="utf-8")
            result = ATSOptimizer().analyze(resume, "Python and SQL")
            self.assertEqual(result.matched_skills, ("python",))

    def test_unsupported_extension_fails(self):
        with TemporaryDirectory() as folder:
            path = Path(folder, "resume.docx")
            path.write_bytes(b"not a document")
            with self.assertRaisesRegex(UnsupportedFileTypeError, "supported"):
                read_document(path)

    def test_missing_document_fails(self):
        with TemporaryDirectory() as folder:
            with self.assertRaisesRegex(DocumentReadError, "does not exist"):
                read_document(Path(folder, "resume.txt"))

    def test_invalid_pdf_fails_without_leaking_contents(self):
        with TemporaryDirectory() as folder:
            path = Path(folder, "resume.pdf")
            path.write_bytes(b"not a pdf")
            with self.assertRaisesRegex(DocumentReadError, "Could not extract"):
                read_document(path)

    def test_missing_pdf_extra_has_install_instructions(self):
        with TemporaryDirectory() as folder:
            path = Path(folder, "resume.pdf")
            path.write_bytes(b"%PDF")
            real_import = __import__

            def import_without_pypdf(name, *args, **kwargs):
                if name == "pypdf":
                    raise ImportError("blocked for test")
                return real_import(name, *args, **kwargs)

            with patch("builtins.__import__", side_effect=import_without_pypdf):
                with self.assertRaisesRegex(MissingOptionalDependencyError, "ats-optimizer.*pdf"):
                    read_document(path)


if __name__ == "__main__":
    unittest.main()

