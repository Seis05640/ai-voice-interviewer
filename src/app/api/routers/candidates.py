from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_session, ingestion_service
from app.api.schemas.candidate import CandidateCreate, CandidateRead
from app.persistence.repositories.candidate_repo import CandidateRepository

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.post("", response_model=CandidateRead)
def create_candidate(payload: CandidateCreate, svc=Depends(ingestion_service)) -> CandidateRead:
    row = svc.create_candidate(
        name=payload.name, email=payload.email, resume_text=payload.resume_text
    )
    return CandidateRead.model_validate(row, from_attributes=True)


@router.get("", response_model=list[CandidateRead])
def list_candidates(session: Session = Depends(db_session)) -> list[CandidateRead]:
    repo = CandidateRepository(session)
    return [CandidateRead.model_validate(c, from_attributes=True) for c in repo.list_all()]
