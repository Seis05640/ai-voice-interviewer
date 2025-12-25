from __future__ import annotations

from pydantic import BaseModel


class InterviewStartRequest(BaseModel):
    job_id: str
    candidate_id: str


class InterviewStartResponse(BaseModel):
    session_id: str
    status: str
    question: str


class InterviewMessageRequest(BaseModel):
    content: str


class InterviewMessageResponse(BaseModel):
    session_id: str
    status: str
    question: str | None = None
