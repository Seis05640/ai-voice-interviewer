from __future__ import annotations

from sqlalchemy.orm import Session

from app.persistence.repositories.job_repo import JobRepository
from app.persistence.repositories.report_repo import ReportRepository
from app.services.evaluation_service import EvaluationService


class ReportingService:
    def __init__(self, session: Session) -> None:
        self._jobs = JobRepository(session)
        self._reports = ReportRepository(session)
        self._evaluation = EvaluationService(session)

    def generate_for_session(self, *, session_id: str) -> dict:
        interview = self._reports.get_interview_required(session_id)
        job = self._jobs.get_required(interview.job_id)

        score = self._evaluation.evaluate_session(session_id=session_id)
        recommendation = "hire" if score >= 0.6 else "no_hire"

        summary = (
            f"Interview report for job '{job.title}'. "
            f"Overall score: {score:.2f}. Recommendation: {recommendation}."
        )

        report = self._reports.upsert(
            job_id=interview.job_id,
            candidate_id=interview.candidate_id,
            overall_score=score,
            recommendation=recommendation,
            summary=summary,
        )

        return {
            "report_id": report.id,
            "job_id": report.job_id,
            "candidate_id": report.candidate_id,
            "overall_score": report.overall_score,
            "recommendation": report.recommendation,
            "summary": report.summary,
        }
