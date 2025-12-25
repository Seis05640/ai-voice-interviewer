from __future__ import annotations

from sqlalchemy.orm import Session

from app.persistence.repositories.candidate_repo import CandidateRepository


class IngestionService:
    def __init__(self, session: Session) -> None:
        self._candidates = CandidateRepository(session)

    def create_candidate(self, *, name: str, email: str | None, resume_text: str):
        return self._candidates.create(name=name, email=email, resume_text=resume_text)
