from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_session, reporting_service
from app.api.schemas.report import ReportGenerateRequest, ReportRead
from app.persistence.repositories.report_repo import ReportRepository

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate", response_model=ReportRead)
def generate(payload: ReportGenerateRequest, svc=Depends(reporting_service)) -> ReportRead:
    return ReportRead(**svc.generate_for_session(session_id=payload.session_id))


@router.get("/{report_id}", response_model=ReportRead)
def get_report(report_id: str, session: Session = Depends(db_session)) -> ReportRead:
    repo = ReportRepository(session)
    row = repo.get_required(report_id)
    return ReportRead(
        report_id=row.id,
        job_id=row.job_id,
        candidate_id=row.candidate_id,
        overall_score=row.overall_score,
        recommendation=row.recommendation,
        summary=row.summary,
    )
