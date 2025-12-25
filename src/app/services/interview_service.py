from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.domain.policies.interview_policy import (
    build_interview_plan,
    plan_from_json,
    plan_to_json,
)
from app.persistence.repositories.interview_repo import InterviewRepository
from app.persistence.repositories.job_repo import JobRepository


class InterviewService:
    def __init__(self, session: Session) -> None:
        self._jobs = JobRepository(session)
        self._interviews = InterviewRepository(session)

    def start_session(self, *, job_id: str, candidate_id: str) -> dict:
        job = self._jobs.get_required(job_id)
        plan = build_interview_plan(job.description)

        session_row = self._interviews.create_session(
            job_id=job_id,
            candidate_id=candidate_id,
            plan_json=plan_to_json(plan),
        )

        first_question = plan[0] if plan else "Introduce yourself."
        self._interviews.add_message(
            session_id=session_row.id,
            role="interviewer",
            content=first_question,
        )
        self._interviews.update_next_question_index(session_row.id, 1)

        return {
            "session_id": session_row.id,
            "status": session_row.status,
            "question": first_question,
        }

    def post_candidate_message(self, *, session_id: str, content: str) -> dict:
        session_row = self._interviews.get_session_required(session_id)
        if session_row.status != "active":
            return {
                "session_id": session_row.id,
                "status": session_row.status,
                "question": None,
            }

        self._interviews.add_message(
            session_id=session_row.id,
            role="candidate",
            content=content,
        )

        plan = plan_from_json(session_row.plan_json)
        idx = session_row.next_question_index

        if idx >= len(plan):
            self._interviews.complete_session(
                session_id=session_row.id,
                ended_at=datetime.now(timezone.utc),
            )
            return {
                "session_id": session_row.id,
                "status": "completed",
                "question": None,
            }

        next_q = plan[idx]
        self._interviews.add_message(
            session_id=session_row.id,
            role="interviewer",
            content=next_q,
        )
        self._interviews.update_next_question_index(session_row.id, idx + 1)

        return {
            "session_id": session_row.id,
            "status": "active",
            "question": next_q,
        }
