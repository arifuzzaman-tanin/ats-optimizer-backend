"""Local document-to-text adapters.

Text analysis has no third-party dependencies. PDF extraction is deliberately
optional and never sends document contents to an external service.
"""

from __future__ import annotations

from pathlib import Path

from .exceptions import (
    DocumentReadError,
    MissingOptionalDependencyError,
    UnsupportedFileTypeError,
)


SUPPORTED_SUFFIXES = frozenset({".txt", ".md", ".pdf"})


def read_document(path: str | Path) -> str:
    """Read supported document text from *path*.

    Plain UTF-8 ``.txt`` and ``.md`` files use the standard library. PDF
    support requires installation with ``pip install ats-optimizer[pdf]``.
    """
    document = Path(path)
    suffix = document.suffix.casefold()
    if suffix not in SUPPORTED_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise UnsupportedFileTypeError(
            f"Unsupported document type {suffix or '(no extension)'!r}; supported: {supported}"
        )
    if not document.is_file():
        raise DocumentReadError(f"Document does not exist or is not a file: {document}")

    if suffix in {".txt", ".md"}:
        try:
            return document.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise DocumentReadError(f"Could not read UTF-8 text from {document}: {error}") from error

    try:
        from pypdf import PdfReader
    except ImportError as error:
        raise MissingOptionalDependencyError(
            "PDF support requires the optional dependency: pip install 'ats-optimizer[pdf]'"
        ) from error

    try:
        reader = PdfReader(document)
        text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except Exception as error:
        raise DocumentReadError(f"Could not extract text from PDF {document}: {error}") from error
    if not text:
        raise DocumentReadError(
            f"No text was extracted from {document}; scanned PDFs require OCR before analysis"
        )
    return text

