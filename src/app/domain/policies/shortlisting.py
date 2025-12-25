from __future__ import annotations

import re
from collections import Counter


_WORD_RE = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in _WORD_RE.findall(text)]


def token_overlap_score(job_description: str, resume_text: str) -> float:
    """Simple baseline score in [0, 1] based on unique-token overlap."""

    jd = set(tokenize(job_description))
    cv = set(tokenize(resume_text))
    if not jd:
        return 0.0

    return len(jd & cv) / len(jd)


def top_overlap_terms(job_description: str, resume_text: str, *, top_n: int = 10) -> list[str]:
    jd_tokens = tokenize(job_description)
    cv_tokens = set(tokenize(resume_text))

    counts = Counter(jd_tokens)
    terms = [t for t, _ in counts.most_common() if t in cv_tokens]
    return terms[:top_n]


def rationale(job_description: str, resume_text: str) -> str:
    terms = top_overlap_terms(job_description, resume_text, top_n=8)
    if not terms:
        return "Low keyword overlap between resume and job description."

    return "Matched terms: " + ", ".join(terms)
