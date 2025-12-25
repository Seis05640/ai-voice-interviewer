from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routers import candidates, health, interviews, jobs, reports
from app.config import settings
from app.persistence.db import init_db
from app.utils.errors import NotFoundError, ValidationError
from app.utils.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(title=settings.app_name)

    @app.on_event("startup")
    def _startup() -> None:
        init_db()

    @app.exception_handler(NotFoundError)
    def _not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ValidationError)
    def _validation_handler(_: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    app.include_router(health.router)
    app.include_router(jobs.router)
    app.include_router(candidates.router)
    app.include_router(interviews.router)
    app.include_router(reports.router)

    return app


app = create_app()
