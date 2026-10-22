"""Public API for the ATS Optimizer skill-coverage library."""

from .analyzer import ATSOptimizer
from .documents import SUPPORTED_SUFFIXES, read_document
from .exceptions import (
    ATSOptimizerError,
    DocumentReadError,
    InvalidInputError,
    MissingOptionalDependencyError,
    UnsupportedFileTypeError,
)
from .extraction import (
    SkillEvidence,
    canonical_skill_name,
    compare_skills,
    extract_skill_evidence,
    extract_skills,
    load_catalog,
)
from .models import AnalysisResult, SkillMatch

__version__ = "0.1.1"

__all__ = [
    "ATSOptimizer",
    "ATSOptimizerError",
    "AnalysisResult",
    "DocumentReadError",
    "InvalidInputError",
    "MissingOptionalDependencyError",
    "SUPPORTED_SUFFIXES",
    "SkillEvidence",
    "SkillMatch",
    "UnsupportedFileTypeError",
    "canonical_skill_name",
    "compare_skills",
    "extract_skill_evidence",
    "extract_skills",
    "load_catalog",
    "read_document",
]

