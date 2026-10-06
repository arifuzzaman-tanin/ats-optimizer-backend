"""Extract known capabilities, rather than treating all nouns as skills.

The catalogue is deliberately conservative: unknown words are never promoted
to skills. Add domain skills and their aliases in skills_catalog.json.
"""

from bisect import bisect_left, bisect_right
from collections import deque
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


@dataclass(frozen=True)
class LiteralRule:
    name: str
    category: str
    phrase: str
    context: re.Pattern | None = None
    allow_standalone: bool = False


@dataclass(frozen=True)
class RegexRule:
    name: str
    category: str
    pattern: re.Pattern


@dataclass(frozen=True)
class CatalogMatcher:
    transitions: tuple[dict[str, int], ...]
    failures: tuple[int, ...]
    outputs: tuple[tuple[LiteralRule, ...], ...]
    regex_rules: tuple[RegexRule, ...]


@lru_cache(maxsize=1)
def catalog_entries():
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        return tuple(json.load(handle))


def _literal_key(phrase):
    """Use the same flexible whitespace/hyphen behavior as phrase_pattern."""
    return re.sub(r"[\s-]+", " ", normalize_text(phrase))


@lru_cache(maxsize=1)
def load_catalog():
    """Build a single-pass matcher for literals and compile custom regex rules."""
    transitions = [{}]
    outputs = [[]]
    regex_rules = []
    names = set()
    for entry in catalog_entries():
        name = normalize_text(entry["name"])
        if name in names:
            raise ValueError(f"Duplicate skill in catalogue: {name}")
        names.add(name)
        category = entry["category"]
        aliases = ([name] if entry.get("name_is_alias", True) else []) + entry.get("aliases", [])
        for alias in aliases:
            phrase = _literal_key(alias)
            state = 0
            for character in phrase:
                next_state = transitions[state].get(character)
                if next_state is None:
                    next_state = len(transitions)
                    transitions[state][character] = next_state
                    transitions.append({})
                    outputs.append([])
                state = next_state
            outputs[state].append(LiteralRule(name, category, phrase))
        for pattern in entry.get("patterns", []):
            regex_rules.append(RegexRule(name, category, re.compile(pattern)))
        for rule in entry.get("contextual_aliases", []):
            context = re.compile(rule["context"])
            for alias in rule["aliases"]:
                phrase = _literal_key(alias)
                state = 0
                for character in phrase:
                    next_state = transitions[state].get(character)
                    if next_state is None:
                        next_state = len(transitions)
                        transitions[state][character] = next_state
                        transitions.append({})
                        outputs.append([])
                    state = next_state
                outputs[state].append(LiteralRule(
                    name, category, phrase, context, rule.get("allow_standalone", False)
                ))

    failures = [0] * len(transitions)
    pending = deque(transitions[0].values())
    while pending:
        state = pending.popleft()
        for character, next_state in transitions[state].items():
            pending.append(next_state)
            failure = failures[state]
            while failure and character not in transitions[failure]:
                failure = failures[failure]
            failures[next_state] = transitions[failure].get(character, 0)
            outputs[next_state].extend(outputs[failures[next_state]])

    return CatalogMatcher(
        tuple(transitions), tuple(failures),
        tuple(tuple(state_outputs) for state_outputs in outputs),
        tuple(regex_rules),
    )


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
    "requirements", "role requirements", "qualifications", "skills", "required skills",
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


def _search_text_with_offsets(text):
    """Collapse separator runs while retaining offsets into normalized text."""
    search_text = []
    starts = []
    ends = []
    index = 0
    while index < len(text):
        start = index
        if text[index].isspace() or text[index] == "-":
            index += 1
            while index < len(text) and (text[index].isspace() or text[index] == "-"):
                index += 1
            search_text.append(" ")
        else:
            search_text.append(text[index])
            index += 1
        starts.append(start)
        ends.append(index)
    return "".join(search_text), starts, ends


def _is_boundary_character(character):
    return character.isalnum() or character == "_" or character in "+#"


def _literal_matches(text, matcher):
    search_text, starts, ends = _search_text_with_offsets(text)
    state = 0
    for index, character in enumerate(search_text):
        while state and character not in matcher.transitions[state]:
            state = matcher.failures[state]
        state = matcher.transitions[state].get(character, 0)
        for rule in matcher.outputs[state]:
            search_start = index - len(rule.phrase) + 1
            start = starts[search_start]
            end = ends[index]
            if start and _is_boundary_character(text[start - 1]):
                continue
            if end < len(text) and _is_boundary_character(text[end]):
                continue
            yield rule, start, end


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
    matcher = load_catalog()
    found = {}

    for rule, start, end in _literal_matches(text, matcher):
        left, right = clause_bounds(text, start, end, boundaries)
        if is_negated(text, start, end, left, right):
            continue
        clause = text[left:right].strip()
        if rule.context is not None:
            standalone = rule.allow_standalone and clause == text[start:end].strip()
            if not standalone and not rule.context.search(clause):
                continue
        evidence = clause if rule.context is not None else text[start:end].strip()
        category, phrases = found.setdefault(rule.name, (rule.category, set()))
        phrases.add(evidence)

    # Free-form catalogue regexes remain on a small fallback path. Literal
    # aliases no longer require thousands of full-document scans.
    for rule in matcher.regex_rules:
        for match in rule.pattern.finditer(text):
            left, right = clause_bounds(text, match.start(), match.end(), boundaries)
            if is_negated(text, match.start(), match.end(), left, right):
                continue
            category, phrases = found.setdefault(rule.name, (rule.category, set()))
            phrases.add(match.group().strip())

    return {
        name: SkillEvidence(category, tuple(sorted(phrases)))
        for name, (category, phrases) in sorted(found.items())
    }


def extract_skills(text, *, source="resume"):
    return list(extract_skill_evidence(text, source=source))


@lru_cache(maxsize=1)
def alias_lookup():
    lookup = {}
    for entry in catalog_entries():
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
