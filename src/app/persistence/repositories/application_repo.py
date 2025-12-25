from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.tables import Application


class ApplicationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def upsert(
        self, *, job_id: str, candidate_id: str, score: float, rationale: str
    ) -> Application:
        stmt = select(Application).where(
            Application.job_id == job_id, Application.candidate_id == candidate_id
        )
        existing = self._session.execute(stmt).scalars().first()

        if existing is None:
            row = Application(
                job_id=job_id,
                candidate_id=candidate_id,
                score=score,
                rationale=rationale,
            )
            self._session.add(row)
        else:
            row = existing
            row.score = score
            row.rationale = rationale

        self._session.commit()
        self._session.refresh(row)
        return row
