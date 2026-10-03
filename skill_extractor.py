"""Extract known capabilities, rather than treating all nouns as skills.

The catalogue is deliberately conservative: unknown words are never promoted
to skills. Add domain skills and their aliases in skills_catalog.json.
"""

from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
import re
import unicodedata


CATALOG_PATH = Path(__file__).with_name("skills_catalog.json")


def normalize_text(text):
    """Normalize PDF ligatures, Unicode punctuation, case and whitespace."""
    text = unicodedata.normalize("NFKC", text).casefold()
    text = text.translate(str.maketrans({"–": "-", "—": "-", "‑": "-", "’": "'"}))
    return re.sub(r"\s+", " ", text).strip()


def phrase_pattern(phrase):
    # Hyphenation varies between resumes: problem-solving / problem solving.
    parts = re.split(r"[\s-]+", normalize_text(phrase))
    return r"(?<![\w+#])" + r"[\s-]+".join(map(re.escape, parts)) + r"(?![\w+#])"


@dataclass(frozen=True)
class SkillEvidence:
    category: str
    phrases: tuple[str, ...]


@lru_cache(maxsize=1)
def load_catalog():
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        entries = json.load(handle)
    compiled = []
    names = set()
    for entry in entries:
        name = normalize_text(entry["name"])
        if name in names:
            raise ValueError(f"Duplicate skill in catalogue: {name}")
        names.add(name)
        rules = []
        aliases = ([name] if entry.get("name_is_alias", True) else []) + entry.get("aliases", [])
        for alias in aliases:
            rules.append((re.compile(phrase_pattern(alias)), None))
        for pattern in entry.get("patterns", []):
            rules.append((re.compile(pattern), None))
        for rule in entry.get("contextual_aliases", []):
            for alias in rule["aliases"]:
                context_pattern = rule["context"]
                if rule.get("allow_standalone", False):
                    context_pattern = f"(?:{context_pattern})|^(?:{phrase_pattern(alias)})$"
                context = re.compile(context_pattern)
                rules.append((re.compile(phrase_pattern(alias)), context))
        compiled.append((name, entry["category"], tuple(rules)))
    return tuple(compiled)


# Company descriptions can mention real technologies that the role never asks
# the applicant to use. Only omit sections with an explicit, recognized heading.
IGNORED_HEADINGS = {
    "the company", "company", "about the company", "about us", "who we are", "why now",
    "our mission", "our story", "our products", "how we work", "benefits",
    "our benefits", "what we offer", "perks", "compensation", "salary",
    "learn more", "about autodesk", "salary transparency", "belonging",
    "in-person onboarding and identity verification",
    "equal opportunity", "equal opportunity employer", "how to apply",
    "equal employment opportunity",
    "this isn't for you if",
}
ROLE_HEADINGS = {
    "about the job", "position overview", "the role", "about the role", "your role", "responsibilities",
    "key responsibilities", "what you'll own", "what you will own",
    "what you'll do", "what you will do", "what you do", "what year one looks like",
    "requirements", "qualifications", "skills", "required skills",
    "preferred skills", "minimum qualifications", "preferred qualifications",
    "what we're looking for", "what we are looking for", "what you bring",
    "this is for you if", "nice to have",
    "what you'll work on", "what you will work on", "our stack", "why this role",
}


def role_text(text):
    lines = []
    ignored = False
    for line in text.splitlines():
        heading = normalize_text(line.strip(" #*\t\r\n:").rstrip(":"))
        if heading in IGNORED_HEADINGS:
            ignored = True
            continue
        if heading in ROLE_HEADINGS:
            ignored = False
            continue
        if not ignored:
            lines.append(line)
    return "\n".join(lines)


def clause_bounds(text, start, end, boundaries):
    """Bound contextual rules to one sentence/bullet, not the entire resume."""
    starts, ends = boundaries
    left_index = bisect_right(ends, start)
    right_index = bisect_left(starts, end)
    left = ends[left_index - 1] if left_index else 0
    right = starts[right_index] if right_index < len(starts) else len(text)
    return left, right


def is_negated(text, start, end, left, right):
    before = text[max(left, start - 100):start]
    after = text[end:min(right, end + 100)]
    if re.search(r"\b(?:don't|doesn't|do not|does not)\s+(?:know|use|have experience (?:in|with))\s*$", before):
        return True
    if re.search(
        r"\b(?:no|without|lack(?:ing)?|not|never)\s+"
        r"(?:(?:prior|any|hands[ -]on|working|practical|proficient|experienced|"
        r"experience|knowledge|skills?|proficiency|familiarity|trained|training|"
        r"in|with|of|using|use|used|work|worked|have|has|had)\s+)*$", before
    ):
        return True
    if re.match(
        r"\s*(?:(?:experience|knowledge|skills?|proficiency|training)\s+)?"
        r"(?:(?:is|are)\s+)?(?:not\s+(?:required|needed|necessary)|"
        r"(?:isn't|aren't)\s+(?:required|needed|necessary))\b", after
    ):
        return True
    return False


def extract_skill_evidence(text, *, source="resume"):
    if not isinstance(text, str):
        raise TypeError("Skill extraction expects text")
    if source not in {"resume", "job_description"}:
        raise ValueError("source must be 'resume' or 'job_description'")
    text = role_text(text) if source == "job_description" else text
    # Keep Markdown bullets as boundaries even when PDF whitespace is collapsed.
    text = re.sub(r"(?m)^[ \t]*[-*][ \t]+", " • ", text)
    text = normalize_text(text)
    # A period inside .NET or Node.js is not a sentence boundary.
    breaks = list(re.finditer(r"[.!?;](?=\s|$)|[•●]|\bbut\b", text))
    boundaries = ([match.start() for match in breaks], [match.end() for match in breaks])
    found = {}
    for name, category, rules in load_catalog():
        evidence = set()
        for pattern, context in rules:
            for match in pattern.finditer(text):
                left, right = clause_bounds(text, match.start(), match.end(), boundaries)
                if is_negated(text, match.start(), match.end(), left, right):
                    continue
                clause = text[left:right].strip()
                if context is not None and not context.search(clause):
                    continue
                # Contextual matches expose their supporting clause as evidence.
                evidence.add(clause if context is not None else match.group().strip())
        if evidence:
            found[name] = SkillEvidence(category, tuple(sorted(evidence)))
    return dict(sorted(found.items()))


def extract_skills(text, *, source="resume"):
    return list(extract_skill_evidence(text, source=source))


@lru_cache(maxsize=1)
def alias_lookup():
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        entries = json.load(handle)
    lookup = {}
    for entry in entries:
        name = normalize_text(entry["name"])
        contextual = [alias for rule in entry.get("contextual_aliases", []) for alias in rule["aliases"]]
        for alias in [name, *entry.get("aliases", []), *contextual]:
            key = re.sub(r"[\s-]+", " ", normalize_text(alias))
            if key in lookup and lookup[key] != name:
                raise ValueError(f"Ambiguous skill alias: {alias}")
            lookup[key] = name
    return lookup


def canonical_skill_name(name):
    normalized = re.sub(r"[\s-]+", " ", normalize_text(name))
    return alias_lookup().get(normalized, normalized)


def compare_skills(job_skills, resume_skills, *, matching):
    """Compare canonical names, preserving job labels without duplicates."""
    resume_names = {canonical_skill_name(name) for name in resume_skills}
    result = []
    seen = set()
    for name in job_skills:
        canonical = canonical_skill_name(name)
        if canonical not in seen and (canonical in resume_names) == matching:
            result.append(name)
        seen.add(canonical)
    return result
