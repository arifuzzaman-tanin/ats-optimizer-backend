"""Analyze a local resume file; install the pdf extra for PDF files."""

from pathlib import Path

from ats_optimizer import ATSOptimizer


result = ATSOptimizer().analyze(
    resume=Path("resume.pdf"),
    job_description="Python and SQL experience required.",
)
print(result.to_dict())

