from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.policies.shortlisting import rationale, token_overlap_score
from app.persistence.repositories.application_repo import ApplicationRepository
from app.persistence.repositories.candidate_repo import CandidateRepository
from app.persistence.repositories.job_repo import JobRepository


class ScreeningService:
    def __init__(self, session: Session) -> None:
        self._jobs = JobRepository(session)
        self._candidates = CandidateRepository(session)
        self._applications = ApplicationRepository(session)

    def screen_job(self, *, job_id: str) -> list[dict]:
        job = self._jobs.get_required(job_id)
        candidates = self._candidates.list_all()

        results: list[dict] = []
        for c in candidates:
            score = token_overlap_score(job.description, c.resume_text)
            why = rationale(job.description, c.resume_text)

            app = self._applications.upsert(
                job_id=job.id,
                candidate_id=c.id,
                score=score,
                rationale=why,
            )

            results.append(
                {
                    "application_id": app.id,
                    "candidate_id": c.id,
                    "job_id": job.id,
                    "score": score,
                    "rationale": why,
                    "status": app.status,
                }
            )

        results.sort(key=lambda r: r["score"], reverse=True)
        return results
