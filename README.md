# ATS Optimizer

Compare the skills in a resume with the skills in a job description.

The package runs locally. It does not need an API key, database, or AI model.

> The score is skill coverage, not a real ATS hiring score.

## Install

From PyPI after the package is published:

```bash
pip install ats-optimizer
```

For PDF files:

```bash
pip install "ats-optimizer[pdf]"
```

From this repository:

```bash
pip install -e .
```

Python 3.10 or newer is required.

## Use text

```python
from ats_optimizer import ATSOptimizer

optimizer = ATSOptimizer()

result = optimizer.analyze(
    resume="Python developer with PostgreSQL experience",
    job_description="Python, SQL, PostgreSQL, and Docker required",
)

print(result.score)
print(result.matched_skills)
print(result.missing_skills)
```

Example output:

```text
50
('postgresql', 'python')
('docker', 'sql')
```

## Use a file

Pass a `Path` when you want to read a file:

```python
from pathlib import Path
from ats_optimizer import ATSOptimizer

result = ATSOptimizer().analyze(
    resume=Path("resume.pdf"),
    job_description=Path("job-description.txt"),
)
```

Supported files:

- `.txt`
- `.md`
- `.pdf` with the `pdf` extra installed

Scanned PDFs need OCR first. DOCX is not currently supported.

## Get JSON

```python
import json

print(json.dumps(result.to_dict(), indent=2))
```

## Handle errors

```python
from ats_optimizer import ATSOptimizer, ATSOptimizerError

try:
    result = ATSOptimizer().analyze("My resume", "The job description")
except ATSOptimizerError as error:
    print(error)
```

## Use with a web framework

Call `ATSOptimizer().analyze(...)` inside your Flask, FastAPI, or Django route.
Return `result.to_dict()` as JSON.

## Run tests

```bash
pip install -e ".[pdf,dev]"
python -m unittest discover -s tests -v
```

## Build the package

```bash
python -m build
python -m twine check dist/*
```

See [PUBLISHING.md](PUBLISHING.md) for release commands. See
[PACKAGE_ANALYSIS.md](PACKAGE_ANALYSIS.md) for the detailed technical analysis.

## Important limitations

- Unknown skills are ignored until added to the catalogue.
- A missing skill means it was not recognized in the resume text.
- The package does not judge candidate quality.
- The package does not generate resume rewrite recommendations.

## License

Released into the public domain under the [Unlicense](LICENSE). Anyone may use,
copy, modify, publish, sell, or distribute it for any purpose. The software is
provided without warranty.
