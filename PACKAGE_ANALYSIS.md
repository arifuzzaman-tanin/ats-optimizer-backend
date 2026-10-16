# Architecture analysis and migration plan

## Baseline analyzed on October 16, 2026

The original repository is a small Flask service. `app.py` owns HTTP input
validation, CORS, response formatting, score calculation, and status bands.
`skill_extractor.py` owns normalization, job-section filtering, negation,
catalogue compilation, extraction, canonicalization, and comparison.
`skills_catalog.json` is the core domain asset. `flask_app.py`, Docker, Nginx,
and the PythonAnywhere workflow are deployment adapters.

There is no database, persistence layer, authentication system, external API,
AI model, job queue, resume object model, recommendation engine, or runtime
PDF parser. The original endpoint accepts already-extracted text. These absent
features are not represented as existing capabilities.

Baseline verification passed 67 `unittest` tests. The catalogue contained
4,954 entries, 6,326 aliases, 5,026 regex patterns, and 4,968 contextual
aliases. The supplied benchmark's 4,790-character fixture measured 74.00 ms
median and 155.29 ms p95 on the local Python 3.13 environment.

## Dependency and package boundary

The reusable package contains the matcher, bundled catalogue, scoring/status
behavior, immutable results, document adapters, and exceptions. Flask, CORS,
Gunicorn, request-size policy, Docker, Nginx, and PythonAnywhere remain
application-specific. Core text analysis uses only the standard library.
`pypdf` is optional and performs local extraction only.

The root `skill_extractor.py` is retained unchanged for the existing service.
Its implementation was copied into `src/ats_optimizer/extraction.py` for the
first compatibility-focused release. A later application migration should
switch `app.py` to the package and turn the root module into a deprecation
shim; doing so now would add deployment risk to the existing PythonAnywhere
layout.

## Behavior retained

- Canonical skill names, aliases, contexts, regex patterns, evidence ordering,
  heading exclusions, and negation behavior.
- Matched skills appear before missing skills.
- Score denominator is recognized job skills only.
- Half-up score rounding and `Best`/`Excellent`/`Good`/`Average` bands.
- Zero recognized skills returns zero with a warning.
- Flask response fields and endpoint behavior are unchanged.

PDF support is a new optional adapter, not a claim about the old application.
Typed models, structured exceptions, and file validation are also new package
interfaces. Recommendation text is deliberately not invented.

## Risks and concerns

- **Performance:** literals use an Aho-Corasick-style automaton, but more than
  5,000 regex rules still scan each document. Cache warm-up and CPU cost grow
  per worker. Future work should classify or combine safe expressions and add
  representative load budgets before changing behavior.
- **Regex safety:** catalogue patterns are trusted code-like configuration.
  Unreviewed patterns can cause catastrophic backtracking. Do not allow users
  to upload catalogue regexes.
- **Catalogue quality:** category names are inconsistent and include spelling
  errors and numeric-looking values. Cleaning them would change public output
  and needs a separately versioned data migration.
- **Scalability:** matcher state is duplicated in each process. The service is
  CPU-bound, synchronous, and has no cross-process cache.
- **Security/privacy:** request limits exist in Flask but not in the library.
  Hosts must set their own memory/time limits. Resume content is sensitive;
  avoid logging it and define retention/deletion policies in consuming apps.
- **Parsing:** PDF text order depends on the source PDF. Scanned files require
  OCR, which is intentionally out of scope.
- **Semantics:** catalogue coverage can produce false negatives and does not
  model proficiency, recency, years of experience, required-vs-preferred
  weighting, or a proprietary ATS ranking.
- **Licensing:** the package uses the Unlicense. Confirm ownership and
  redistribution rights for every catalogue entry before public publication.

No tracked credential values were found by the baseline secret-pattern scan.
The deployment token is correctly referenced through a GitHub secret.

## Public API and compatibility policy

`ATSOptimizer.analyze` is the primary API. Inputs are nonempty text strings or
path-like objects, and output is `AnalysisResult`. Strings are unambiguously
text; callers use `Path` for files. Result classes are frozen dataclasses and
serialize through `to_dict()`.

Semantic versioning is recommended. Until 1.0, document intentional API changes
in the changelog. Catalogue additions can change extracted results even when
the Python API is unchanged, so release notes must call out data changes.

## Configuration and operations

The core requires no environment variables or credentials. The existing app's
`MAX_REQUEST_BYTES` remains a deployment setting. Consumers select PDF support
at install time. Logging is left to host applications; exceptions carry
actionable messages without document contents.

## Testing strategy

1. Preserve the existing regression suite for extraction and Flask behavior.
2. Test public result properties, exact legacy score behavior, serialization,
   empty/type errors, text files, unsupported formats, and PDF errors.
3. Build wheel and sdist, run Twine checks, inspect archive contents, install
   the wheel into a clean environment, and run import/example smoke tests.
4. Run CI on Python 3.10–3.13 and test the built wheel, not only the checkout.
5. Keep the benchmark non-gating until hardware-normalized thresholds exist.

## Migration sequence

1. Publish 0.1.x only after confirming catalogue redistribution rights.
2. Have the Flask service depend on the released package and compare endpoint
   snapshots against the current service.
3. Replace root extraction code with a warning-backed import shim in a minor
   release, after deployment paths install the package.
4. Consider entry-point-based custom catalogues and weighted requirements only
   as explicit enhancements with separately documented scoring semantics.

