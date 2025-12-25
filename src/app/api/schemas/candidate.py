from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class CandidateCreate(BaseModel):
    name: str
    email: str | None = None
    resume_text: str


class CandidateRead(BaseModel):
    id: str
    name: str
    email: str | None = None
    resume_text: str
    created_at: datetime
