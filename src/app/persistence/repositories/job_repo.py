from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.tables import Job
from app.utils.errors import NotFoundError


class JobRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, *, title: str, description: str) -> Job:
        row = Job(title=title, description=description)
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return row

    def get(self, job_id: str) -> Job | None:
        return self._session.get(Job, job_id)

    def get_required(self, job_id: str) -> Job:
        job = self.get(job_id)
        if job is None:
            raise NotFoundError(f"Job not found: {job_id}")
        return job

    def list_all(self) -> list[Job]:
        stmt = select(Job).order_by(Job.created_at.desc())
        return list(self._session.execute(stmt).scalars().all())
