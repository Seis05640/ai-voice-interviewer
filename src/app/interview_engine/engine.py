from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Literal
from uuid import uuid4

from app.domain.policies.interview_policy import build_interview_plan


@dataclass(slots=True)
class InterviewTurn:
    question: str
    answer: str | None = None


InterviewStatus = Literal["active", "completed"]


@dataclass(slots=True)
class InterviewSessionState:
    session_id: str
    status: InterviewStatus
    turns: list[InterviewTurn]
    next_turn_index: int = 0
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def max_questions(self) -> int:
        return len(self.turns)

    def current_question(self) -> str | None:
        if self.status != "active":
            return None
        if self.next_turn_index >= len(self.turns):
            return None
        return self.turns[self.next_turn_index].question

    def submit_answer(self, answer: str) -> None:
        if self.status != "active":
            raise ValueError("Interview is not active.")
        if self.next_turn_index >= len(self.turns):
            raise ValueError("No remaining questions.")

        self.turns[self.next_turn_index].answer = answer
        self.next_turn_index += 1

        if self.next_turn_index >= len(self.turns):
            self.status = "completed"
            self.ended_at = datetime.now(timezone.utc)

    def transcript(self) -> list[dict[str, str | None]]:
        return [{"question": t.question, "answer": t.answer} for t in self.turns]

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "status": self.status,
            "turns": [
                {
                    "question": t.question,
                    "answer": t.answer,
                }
                for t in self.turns
            ],
            "next_turn_index": self.next_turn_index,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InterviewSessionState":
        started_at = datetime.fromisoformat(str(data["started_at"]))
        ended_at_raw = data.get("ended_at")
        ended_at = datetime.fromisoformat(str(ended_at_raw)) if ended_at_raw else None

        turns = [InterviewTurn(question=str(t["question"]), answer=t.get("answer")) for t in data["turns"]]

        return cls(
            session_id=str(data["session_id"]),
            status=str(data["status"]),
            turns=turns,
            next_turn_index=int(data.get("next_turn_index", 0)),
            started_at=started_at,
            ended_at=ended_at,
            metadata=dict(data.get("metadata", {})),
        )


class TextInterviewEngine:
    """A small, deterministic, text-based interview engine.

    Design goals:
    - Ask exactly one question at a time.
    - Questions are tailored to job description + resume.
    - Track state and stop after a fixed number of questions.
    - Store answers in the in-memory session state.

    The default planner delegates to :func:`app.domain.policies.interview_policy.build_interview_plan`.
    """

    def __init__(
        self,
        *,
        planner: Callable[[str, str, int], list[str]] | None = None,
        session_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._planner = planner or (lambda jd, cv, n: build_interview_plan(jd, resume_text=cv, max_questions=n))
        self._session_id_factory = session_id_factory or (lambda: str(uuid4()))

    def start(self, *, job_description: str, resume_text: str, max_questions: int = 6) -> InterviewSessionState:
        questions = self._planner(job_description, resume_text, max_questions)
        turns = [InterviewTurn(question=q) for q in questions]

        return InterviewSessionState(
            session_id=self._session_id_factory(),
            status="active",
            turns=turns,
            metadata={
                "job_description_chars": len(job_description),
                "resume_text_chars": len(resume_text),
            },
        )

    def next_question(self, state: InterviewSessionState) -> str | None:
        return state.current_question()

    def answer(self, state: InterviewSessionState, *, answer: str) -> InterviewSessionState:
        state.submit_answer(answer)
        return state
