from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_session, screening_service
from app.api.schemas.job import JobCreate, JobRead
from app.persistence.repositories.job_repo import JobRepository

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobRead)
def create_job(payload: JobCreate, session: Session = Depends(db_session)) -> JobRead:
    repo = JobRepository(session)
    row = repo.create(title=payload.title, description=payload.description)
    return JobRead.model_validate(row, from_attributes=True)


@router.get("", response_model=list[JobRead])
def list_jobs(session: Session = Depends(db_session)) -> list[JobRead]:
    repo = JobRepository(session)
    return [JobRead.model_validate(j, from_attributes=True) for j in repo.list_all()]


@router.post("/{job_id}/screen")
def screen(job_id: str, svc=Depends(screening_service)) -> dict:
    results = svc.screen_job(job_id=job_id)
    return {"job_id": job_id, "results": results}
