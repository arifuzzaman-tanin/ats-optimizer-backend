# ATS Optimizer backend

Flask API for comparing **recognized job skills** with skill evidence in a resume.
The percentage measures coverage of those skills; it does not predict an ATS
decision or assess overall applicant suitability.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

The API listens on port 5000. The existing Docker/Gunicorn setup is also
supported. Skill extraction uses the Python standard library and does not
require spaCy, NumPy, a model download, an API key, or an external AI service.

## Skill extraction

`skill_extractor.py` matches capabilities and tools defined in
`skills_catalog.json`. It does not use noun/proper-noun tags as a proxy for
skills. For example:

| Description or resume phrase | Canonical skill |
| --- | --- |
| Customer service / client support | Customer support |
| Customer service interaction (phone/email) | Phone support, email support |
| Tickets from start to finish | Ticket management |
| Cases from the BPO team | Outsourced support coordination |
| Clear articles and guides for customers | Technical writing |
| Help centre / help center | Knowledge base management |
| First point of contact | First contact resolution |
| Problem-solving | Problem solving |
| Silvie, Pontosense, patents, January, families | No skill extracted |

Aliases resolve to one canonical name, so repeated or synonymous mentions do
not increase the score. Common single words such as `email`, `phone`, `setup`,
`articles`, and `Excel` require supporting context. Named tools such as Excel
and React can also appear on their own as a skill-list item. Text normalization
handles case, whitespace, hyphenation, and PDF ligatures.

For job descriptions, sections with recognized company, benefits, or culture
headings are excluded. Role, responsibility, and qualification sections are
included. Resume extraction uses the whole submitted text. Basic negative
statements such as "No Python experience" or "Python is not required" are
excluded. Generic problem solving does **not** imply technical troubleshooting.

This is a conservative, rule-based extractor, not unrestricted semantic
understanding. Its catalogue currently covers customer support, interpersonal
skills, common business capabilities, and selected technical tools, including
Azure application, integration, infrastructure, monitoring, and security terms.
Unknown skills are omitted until added to the catalogue. Section filtering needs
recognizable headings; a single unstructured paragraph may mix company and
role information. Complex negations and paraphrases may need additional rules.
Missing means **no recognized evidence in the submitted resume**, not proof
that the candidate lacks the capability.

## API

`GET /health` returns `{"status": "ok"}`.

`POST /extract_skills` accepts JSON with two nonempty strings:

```json
{
  "job_description": "Customer support, troubleshooting and Python skills",
  "resume": "Customer service representative with Python experience"
}
```

Existing response fields and the `skills` array's `name` and
`is_available_in_resume` fields are preserved. Each skill also includes its
category and the normalized phrases supporting it in both documents:

```json
{
  "name": "customer support",
  "is_available_in_resume": true,
  "category": "customer_support",
  "job_description_evidence": ["customer support"],
  "resume_evidence": ["customer service", "customer service representative"]
}
```

The sample request returns 67%: two of three recognized skills match. Complete
coverage returns 100%. If no job skills are recognized, the API returns an empty
skills list, 0%, and a `warning` explaining that the score is not informative.
`score_scope` and `skill_extraction_method` describe the calculation. Invalid
JSON, field types, and empty strings return HTTP 400.

The API continues to accept extracted resume **text**, rather than PDF uploads.
The provided PDF was read locally for validation; PDF parsing is not a runtime
dependency of this API.

## Extend the catalogue

Add an entry to `skills_catalog.json`:

```json
{
  "name": "network troubleshooting",
  "category": "technical",
  "aliases": ["diagnosing network issues", "network diagnostics"]
}
```

Use `patterns` for precise normalized-text regular expressions, or
`contextual_aliases` for ambiguous phrases:

```json
{
  "name": "network configuration",
  "category": "technical",
  "aliases": ["router configuration"],
  "contextual_aliases": [
    {"aliases": ["configuration"], "context": "\\b(?:network|router|switch)\\b"}
  ]
}
```

Context applies within one sentence or bullet. Set `name_is_alias: false` when
the canonical name itself is ambiguous, and put that name in a contextual rule.
For named tools, `allow_standalone: true` on that rule permits the alias as the
entire sentence/list item. Canonical names and unconditional aliases otherwise
match directly. Regex patterns must encode any context they require.

Restart the service after editing the catalogue, because compiled rules are
cached. Add tests with both positive evidence and plausible false positives.

## Validate

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Run the repeatable extraction benchmark with:

```powershell
.\.venv\Scripts\python.exe benchmarks\benchmark_extraction.py
```

Literal aliases are indexed into a single-pass matcher at process startup;
only the catalogue's custom regular expressions use full-text regex scans.
Successful extraction responses include `Server-Timing` values for the job
description and resume phases. Request bodies are limited to 512 KiB by
default; set `MAX_REQUEST_BYTES` to change that deployment limit.

Tests cover the supplied job description, selected resume experience without
personal data, synonyms, company noise, multiword skills, context boundaries,
negation, PDF text normalization, technical symbols, scoring, input validation,
health checks, and CORS.

## Deploy from GitHub to PythonAnywhere

The GitHub Actions workflow in `.github/workflows/deploy-pythonanywhere.yml`
runs the tests on every push to `main`. If they pass, it uploads the runtime
files through the PythonAnywhere API, reloads
`arifuzzamantanin.pythonanywhere.com`, and checks the `/health` endpoint.

Create an API token on the PythonAnywhere **Account > API token** page. In the
GitHub repository, open **Settings > Environments > production**, add an
environment secret named `PYTHONANYWHERE_API_TOKEN`, and paste the token as its
value. Never commit the token to the repository.

The workflow updates application source files but does not run commands inside
PythonAnywhere. When `requirements.txt` changes, install the updated packages
once from a PythonAnywhere Bash console before deploying:

```bash
workon ats-optimizer-env
cd /home/arifuzzamantanin/mysite
pip install -r requirements.txt
```
