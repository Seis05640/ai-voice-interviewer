from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.tables import InterviewMessage, InterviewSession, InterviewStatus
from app.utils.errors import NotFoundError


class InterviewRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_session(self, *, job_id: str, candidate_id: str, plan_json: str) -> InterviewSession:
        row = InterviewSession(job_id=job_id, candidate_id=candidate_id, plan_json=plan_json)
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return row

    def get_session(self, session_id: str) -> InterviewSession | None:
        return self._session.get(InterviewSession, session_id)

    def get_session_required(self, session_id: str) -> InterviewSession:
        row = self.get_session(session_id)
        if row is None:
            raise NotFoundError(f"Interview session not found: {session_id}")
        return row

    def update_next_question_index(self, session_id: str, next_index: int) -> None:
        row = self.get_session_required(session_id)
        row.next_question_index = next_index
        self._session.add(row)
        self._session.commit()

    def add_message(self, *, session_id: str, role: str, content: str) -> InterviewMessage:
        msg = InterviewMessage(session_id=session_id, role=role, content=content)
        self._session.add(msg)
        self._session.commit()
        self._session.refresh(msg)
        return msg

    def list_messages(self, session_id: str) -> list[InterviewMessage]:
        stmt = (
            select(InterviewMessage)
            .where(InterviewMessage.session_id == session_id)
            .order_by(InterviewMessage.created_at.asc())
        )
        return list(self._session.execute(stmt).scalars().all())

    def complete_session(self, *, session_id: str, ended_at: datetime) -> None:
        row = self.get_session_required(session_id)
        row.status = InterviewStatus.completed
        row.ended_at = ended_at
        self._session.add(row)
        self._session.commit()
