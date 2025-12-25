from __future__ import annotations

from pydantic import BaseModel


class ReportGenerateRequest(BaseModel):
    session_id: str


class ReportRead(BaseModel):
    report_id: str
    job_id: str
    candidate_id: str
    overall_score: float
    recommendation: str
    summary: str
