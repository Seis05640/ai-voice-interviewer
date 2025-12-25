#!/usr/bin/env python3
"""Simple text-based interview engine example.

This demonstrates an interview flow where:
- The engine generates a fixed number of questions.
- You ask/answer one question at a time.
- State is tracked in-memory and answers are stored in the session.

Run:
  python examples/text_interview_engine_example.py
"""

import sys

sys.path.insert(0, "/home/engine/project/src")

from app.interview_engine import TextInterviewEngine


JOB_DESCRIPTION = """
Backend Engineer (Python)

We are looking for a backend engineer with experience building APIs.

Requirements:
- Python, FastAPI
- PostgreSQL
- Docker
- AWS
- Strong communication and problem solving
"""

RESUME_TEXT = """
Jane Candidate

WORK EXPERIENCE
Backend Engineer | ExampleCo | 2022 - Present
- Built REST APIs using FastAPI and SQLAlchemy
- Deployed containerized services with Docker
- Reduced P95 latency by 30% by profiling and optimizing queries

SKILLS
Python, FastAPI, SQLAlchemy, Docker, Git
"""


def main() -> None:
    engine = TextInterviewEngine()
    state = engine.start(job_description=JOB_DESCRIPTION, resume_text=RESUME_TEXT, max_questions=5)

    sample_answers = [
        "I'm a backend engineer focused on Python APIs and reliability.",
        "I improved query performance by adding indexes and removing N+1 patterns.",
        "I used FastAPI to build internal tooling with OAuth and role-based access.",
        "I don't have deep AWS experience yet, but I've used Docker locally and would ramp up via a small service deployment.",
        "What are the biggest technical challenges for this team in the next quarter?",
    ]

    i = 0
    while True:
        q = engine.next_question(state)
        if q is None:
            break

        print(f"\nQ{i + 1}: {q}")
        answer = sample_answers[i] if i < len(sample_answers) else "(no answer provided)"
        print(f"A{i + 1}: {answer}")

        engine.answer(state, answer=answer)
        i += 1

    print("\n" + "=" * 72)
    print(f"Interview complete (status={state.status}, questions={state.max_questions})")
    print("=" * 72)

    for idx, turn in enumerate(state.turns, start=1):
        print(f"\nQ{idx}: {turn.question}")
        print(f"A{idx}: {turn.answer}")


if __name__ == "__main__":
    main()
