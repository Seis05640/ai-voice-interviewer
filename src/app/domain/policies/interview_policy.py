from __future__ import annotations

import json

from app.domain.policies.shortlisting import tokenize


def build_interview_plan(job_description: str, *, max_questions: int = 6) -> list[str]:
    """Generate a simple interview plan from job description keywords.

    This is intentionally deterministic and beginner-friendly; later you can swap
    it with an LLM-backed planner behind the same service.
    """

    tokens = tokenize(job_description)
    stop = {
        "the",
        "and",
        "to",
        "of",
        "a",
        "in",
        "for",
        "with",
        "on",
        "is",
        "are",
        "as",
        "at",
        "be",
        "or",
        "an",
    }

    keywords: list[str] = []
    seen: set[str] = set()
    for t in tokens:
        if t in stop or len(t) < 3:
            continue
        if t in seen:
            continue
        seen.add(t)
        keywords.append(t)
        if len(keywords) >= max_questions - 2:
            break

    questions: list[str] = [
        "Briefly introduce yourself and summarize your relevant experience.",
    ]

    for kw in keywords:
        questions.append(f"Tell me about a project where you used {kw}.")

    questions.extend(
        [
            "Describe a challenging problem you solved and how you approached it.",
            "Do you have any questions for us?",
        ]
    )

    return questions[:max_questions]


def plan_to_json(plan: list[str]) -> str:
    return json.dumps(plan, ensure_ascii=False)


def plan_from_json(plan_json: str) -> list[str]:
    try:
        data = json.loads(plan_json)
    except json.JSONDecodeError:
        return []

    if not isinstance(data, list):
        return []

    return [str(x) for x in data]
