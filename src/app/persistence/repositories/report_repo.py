from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.tables import InterviewSession, Report
from app.utils.errors import NotFoundError


class ReportRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_interview_required(self, session_id: str) -> InterviewSession:
        row = self._session.get(InterviewSession, session_id)
        if row is None:
            raise NotFoundError(f"Interview session not found: {session_id}")
        return row

    def upsert(
        self,
        *,
        job_id: str,
        candidate_id: str,
        overall_score: float,
        recommendation: str,
        summary: str,
    ) -> Report:
        stmt = select(Report).where(Report.job_id == job_id, Report.candidate_id == candidate_id)
        existing = self._session.execute(stmt).scalars().first()

        if existing is None:
            row = Report(
                job_id=job_id,
                candidate_id=candidate_id,
                overall_score=overall_score,
                recommendation=recommendation,
                summary=summary,
            )
            self._session.add(row)
        else:
            row = existing
            row.overall_score = overall_score
            row.recommendation = recommendation
            row.summary = summary

        self._session.commit()
        self._session.refresh(row)
        return row

    def get(self, report_id: str) -> Report | None:
        return self._session.get(Report, report_id)

    def get_required(self, report_id: str) -> Report:
        report = self.get(report_id)
        if report is None:
            raise NotFoundError(f"Report not found: {report_id}")
        return report
