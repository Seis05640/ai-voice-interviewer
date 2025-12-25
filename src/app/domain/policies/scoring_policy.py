from __future__ import annotations

import math

from app.domain.policies.shortlisting import tokenize


def answer_quality_score(answer: str, *, expected_terms: list[str] | None = None) -> float:
    """Small deterministic score in [0, 1] based on length + keyword hits."""

    tokens = tokenize(answer)
    if not tokens:
        return 0.0

    length_component = 1 - math.exp(-len(tokens) / 60)

    if not expected_terms:
        return float(length_component)

    token_set = set(tokens)
    hits = sum(1 for t in expected_terms if t.lower() in token_set)
    keyword_component = hits / max(len(expected_terms), 1)

    return max(0.0, min(1.0, 0.6 * length_component + 0.4 * keyword_component))
