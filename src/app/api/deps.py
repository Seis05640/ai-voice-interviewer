from __future__ import annotations

from collections.abc import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.llm.base import LLMClient
from app.llm.factory import get_llm_client
from app.persistence.db import get_session
from app.services.ingestion_service import IngestionService
from app.services.interview_service import InterviewService
from app.services.reporting_service import ReportingService
from app.services.screening_service import ScreeningService


def db_session() -> Iterator[Session]:
    yield from get_session()


def llm_client() -> LLMClient:
    return get_llm_client()


def ingestion_service(session: Session = Depends(db_session)) -> IngestionService:
    return IngestionService(session)


def screening_service(session: Session = Depends(db_session)) -> ScreeningService:
    return ScreeningService(session)


def interview_service(session: Session = Depends(db_session)) -> InterviewService:
    return InterviewService(session)


def reporting_service(session: Session = Depends(db_session)) -> ReportingService:
    return ReportingService(session)
