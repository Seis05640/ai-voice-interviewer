from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.tables import Candidate
from app.utils.errors import NotFoundError


class CandidateRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, *, name: str, email: str | None, resume_text: str) -> Candidate:
        row = Candidate(name=name, email=email, resume_text=resume_text)
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return row

    def get(self, candidate_id: str) -> Candidate | None:
        return self._session.get(Candidate, candidate_id)

    def get_required(self, candidate_id: str) -> Candidate:
        candidate = self.get(candidate_id)
        if candidate is None:
            raise NotFoundError(f"Candidate not found: {candidate_id}")
        return candidate

    def list_all(self) -> list[Candidate]:
        stmt = select(Candidate).order_by(Candidate.created_at.desc())
        return list(self._session.execute(stmt).scalars().all())
