"""Public exception hierarchy for :mod:`ats_optimizer`."""


class ATSOptimizerError(Exception):
    """Base class for package-specific failures."""


class InvalidInputError(ATSOptimizerError, ValueError):
    """Raised when analysis input is empty or has an unsupported type."""


class UnsupportedFileTypeError(ATSOptimizerError, ValueError):
    """Raised when a document format is not supported."""


class MissingOptionalDependencyError(ATSOptimizerError, ImportError):
    """Raised when an optional document parser has not been installed."""


class DocumentReadError(ATSOptimizerError, OSError):
    """Raised when text cannot be extracted from a document."""

