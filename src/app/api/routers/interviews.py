from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import interview_service
from app.api.schemas.interview import (
    InterviewMessageRequest,
    InterviewMessageResponse,
    InterviewStartRequest,
    InterviewStartResponse,
)

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post("/start", response_model=InterviewStartResponse)
def start(payload: InterviewStartRequest, svc=Depends(interview_service)):
    data = svc.start_session(job_id=payload.job_id, candidate_id=payload.candidate_id)
    return InterviewStartResponse(**data)


@router.post("/{session_id}/message", response_model=InterviewMessageResponse)
def post_message(session_id: str, payload: InterviewMessageRequest, svc=Depends(interview_service)):
    data = svc.post_candidate_message(session_id=session_id, content=payload.content)
    return InterviewMessageResponse(**data)
