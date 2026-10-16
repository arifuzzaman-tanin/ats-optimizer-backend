"""High-level ATS skill-coverage analysis API."""

from __future__ import annotations

import math
from os import PathLike
from pathlib import Path

from .documents import read_document
from .exceptions import InvalidInputError
from .extraction import extract_skill_evidence
from .models import AnalysisResult, SkillMatch


def round_score(number: float) -> int:
    """Round halves upward, preserving the application's scoring behavior."""
    return math.ceil(number) if number % 1 >= 0.5 else math.floor(number)


def score_status(score: int) -> str:
    """Return the legacy display band for a percentage score."""
    if 81 <= score <= 100:
        return "Best"
    if 61 <= score <= 80:
        return "Excellent"
    if 41 <= score <= 60:
        return "Good"
    if 21 <= score <= 40:
        return "Average"
    return "Below Average"


def _text(value: str | PathLike[str], *, label: str) -> str:
    if isinstance(value, PathLike):
        result = read_document(Path(value))
    elif isinstance(value, str):
        result = value
    else:
        raise InvalidInputError(f"{label} must be text or a path-like object")
    if not result.strip():
        raise InvalidInputError(f"{label} must not be empty")
    return result


class ATSOptimizer:
    """Analyze recognized skill coverage without external services.

    String inputs are treated as document text. Pass a :class:`pathlib.Path`
    to read a local ``.txt``, ``.md``, or (with the ``pdf`` extra) ``.pdf``.
    """

    def analyze(
        self,
        resume: str | PathLike[str],
        job_description: str | PathLike[str],
    ) -> AnalysisResult:
        """Compare resume evidence with recognized job-description skills."""
        resume_text = _text(resume, label="resume")
        job_text = _text(job_description, label="job_description")
        job_evidence = extract_skill_evidence(job_text, source="job_description")
        resume_evidence = extract_skill_evidence(resume_text, source="resume")

        matched = [name for name in job_evidence if name in resume_evidence]
        missing = [name for name in job_evidence if name not in resume_evidence]
        ordered_names = [*matched, *missing]
        skills = tuple(
            SkillMatch(
                name=name,
                category=job_evidence[name].category,
                is_available_in_resume=name in resume_evidence,
                job_description_evidence=job_evidence[name].phrases,
                resume_evidence=(resume_evidence[name].phrases if name in resume_evidence else ()),
            )
            for name in ordered_names
        )
        score = round_score(100 * len(matched) / len(skills)) if skills else 0
        warning = None
        if not skills:
            warning = (
                "No recognized job skills found. Extend the skill catalogue for this domain; "
                "the score is not informative."
            )
        return AnalysisResult(score, score_status(score), skills, warning)

