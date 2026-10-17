"""Immutable result models returned by the public API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SkillMatch:
    """One job skill and the evidence found in both inputs."""

    name: str
    category: str
    is_available_in_resume: bool
    job_description_evidence: tuple[str, ...]
    resume_evidence: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return {
            "name": self.name,
            "is_available_in_resume": self.is_available_in_resume,
            "category": self.category,
            "job_description_evidence": list(self.job_description_evidence),
            "resume_evidence": list(self.resume_evidence),
        }


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Skill-coverage analysis for a resume and job description."""

    score: int
    status: str
    skills: tuple[SkillMatch, ...]
    warning: str | None = None

    @property
    def matched_skills(self) -> tuple[str, ...]:
        """Canonical names of job skills evidenced in the resume."""
        return tuple(skill.name for skill in self.skills if skill.is_available_in_resume)

    @property
    def missing_skills(self) -> tuple[str, ...]:
        """Canonical job skills without recognized resume evidence."""
        return tuple(skill.name for skill in self.skills if not skill.is_available_in_resume)

    @property
    def total_required_skills(self) -> int:
        return len(self.skills)

    @property
    def total_matching_skills(self) -> int:
        return len(self.matched_skills)

    @property
    def total_missing_skills(self) -> int:
        return len(self.missing_skills)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable mapping compatible with the Flask API."""
        value: dict[str, Any] = {
            "resume_score_in_percentage": self.score,
            "resume_status": self.status,
            "total_required_skills_in_job_description": self.total_required_skills,
            "total_missing_skills_in_resume": self.total_missing_skills,
            "total_matching_skills_in_resume": self.total_matching_skills,
            "skills": [skill.to_dict() for skill in self.skills],
            "comma_separated_missing_skills": ", ".join(self.missing_skills),
            "skill_extraction_method": "curated_catalogue_with_context_and_aliases",
            "score_scope": (
                "Recognized job skills evidenced in the resume; not an overall ATS score"
            ),
        }
        if self.warning is not None:
            value["warning"] = self.warning
        return value

