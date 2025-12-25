"""Text-based interview engine.

This module provides a small in-memory engine you can use in a CLI, tests, or as
an orchestration layer behind an API.

The production FastAPI app in this repository persists interview sessions to the
DB (see :mod:`app.services.interview_service`). This engine is complementary:
- It generates one question at a time.
- It tracks interview state.
- It stores answers.
"""

from app.interview_engine.engine import (
    InterviewSessionState,
    InterviewTurn,
    TextInterviewEngine,
)

__all__ = [
    "InterviewSessionState",
    "InterviewTurn",
    "TextInterviewEngine",
]
