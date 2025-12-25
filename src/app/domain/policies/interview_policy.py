from __future__ import annotations

import json
import re
from collections import Counter

from app.domain.policies.shortlisting import tokenize


_STOPWORDS: set[str] = {
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
    "we",
    "you",
    "your",
    "our",
    "will",
    "role",
    "requirements",
    "responsibilities",
    "experience",
}


def build_interview_plan(
    job_description: str,
    *,
    resume_text: str | None = None,
    max_questions: int = 6,
) -> list[str]:
    """Generate a deterministic interview plan.

    If resume_text is provided, the plan is tailored to both the job description
    and the candidate's resume.
    """

    if max_questions <= 0:
        return []

    if resume_text:
        return _build_plan_from_job_and_resume(
            job_description, resume_text, max_questions=max_questions
        )

    return _build_plan_from_job_only(job_description, max_questions=max_questions)


def _build_plan_from_job_only(job_description: str, *, max_questions: int) -> list[str]:
    tokens = tokenize(job_description)

    keywords: list[str] = []
    seen: set[str] = set()
    for t in tokens:
        if t in _STOPWORDS or len(t) < 3:
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


def _truncate(text: str, *, max_len: int = 140) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_len:
        return compact
    return compact[: max_len - 1].rstrip() + "…"


def _term_count(text_lower: str, term_lower: str) -> int:
    if re.fullmatch(r"[a-z0-9 ]+", term_lower):
        pattern = r"(?<![a-z0-9])" + re.escape(term_lower) + r"(?![a-z0-9])"
        return len(re.findall(pattern, text_lower))
    return text_lower.count(term_lower)


def _rank_terms_by_job_frequency(job_description: str, terms: set[str]) -> list[str]:
    text_lower = job_description.lower()

    scored: list[tuple[int, str]] = []
    for term in terms:
        t = term.strip().lower()
        if not t:
            continue
        scored.append((_term_count(text_lower, t), t))

    scored.sort(key=lambda x: (-x[0], x[1]))
    return [t for c, t in scored if c > 0]


def _build_plan_from_job_and_resume(
    job_description: str,
    resume_text: str,
    *,
    max_questions: int,
) -> list[str]:
    from app.nlp.experience_extractor import extract_experience
    from app.nlp.skill_extractor import extract_skills

    questions: list[str] = []

    intro = "Briefly introduce yourself and summarize your most relevant experience for this role."
    closing = "Do you have any questions for us about the role, team, or next steps?"
    behavioral = "Describe a challenging problem you solved, how you approached it, and what you learned."

    questions.append(intro)

    tail: list[str] = []
    if max_questions >= 2:
        tail.append(closing)
    if max_questions >= 3:
        tail.insert(0, behavioral)

    slots = max_questions - len(questions) - len(tail)
    if slots <= 0:
        return (questions + tail)[:max_questions]

    jd_skills = extract_skills(job_description)
    cv_skills = extract_skills(resume_text)

    required_terms: set[str] = set(jd_skills["technical"]) | set(jd_skills["soft"])

    jd_tokens = [t for t in tokenize(job_description) if t not in _STOPWORDS and len(t) >= 3]
    for term, _ in Counter(jd_tokens).most_common(25):
        required_terms.add(term)

    resume_terms: set[str] = set(cv_skills["technical"]) | set(cv_skills["soft"])
    resume_terms |= {t for t in tokenize(resume_text) if len(t) >= 3}

    matched_terms = required_terms & resume_terms
    gap_terms = required_terms - resume_terms

    matched_ranked = _rank_terms_by_job_frequency(job_description, matched_terms)
    gaps_ranked = _rank_terms_by_job_frequency(job_description, gap_terms)

    exp = extract_experience(resume_text)
    highlight: str | None = None
    if exp.get("achievements"):
        highlight = str(exp["achievements"][0])
    elif exp.get("job_titles"):
        highlight = str(exp["job_titles"][0])

    targeted: list[str] = []
    if highlight:
        snippet = _truncate(highlight)
        targeted.append(
            "On your resume you mention: "
            f"\"{snippet}\". Can you walk me through the context, your specific contribution, and the outcome?"
        )

    asked_topics: set[str] = set()

    def add_matched(term: str) -> None:
        asked_topics.add(term)
        targeted.append(
            f"Tell me about the most impactful work you've done using {term}. "
            "What was the problem, what did you build, and how did you measure success?"
        )

    def add_gap(term: str) -> None:
        asked_topics.add(term)
        targeted.append(
            f"This role involves {term}. What experience do you have with it, and if it's new to you, "
            "how would you ramp up in your first 30 days?"
        )

    i = 0
    j = 0
    while len(targeted) < slots and (i < len(matched_ranked) or j < len(gaps_ranked)):
        if i < len(matched_ranked):
            t = matched_ranked[i]
            i += 1
            if t not in asked_topics:
                add_matched(t)
                if len(targeted) >= slots:
                    break

        if j < len(gaps_ranked):
            t = gaps_ranked[j]
            j += 1
            if t not in asked_topics:
                add_gap(t)

    fallbacks = [
        "What accomplishment are you most proud of, and what made it difficult?",
        "How do you like to work with product/engineering stakeholders when requirements are unclear?",
        "What's an example of a trade-off you made between speed and quality, and how did you decide?",
    ]
    for fb in fallbacks:
        if len(targeted) >= slots:
            break
        targeted.append(fb)

    questions.extend(targeted[:slots])
    questions.extend(tail)

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
