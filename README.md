# ai-voice-interviewer

This repository contains a **modular, beginner-friendly (but scalable) Python backend scaffold** for an AI-powered interview system.

## Features (scaffold)
- Jobs + candidates CRUD
- Resume/JD screening (simple deterministic scoring)
- Interview sessions (text-based demo)
- Reporting (stub)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

uvicorn app.main:app --reload
```

Then visit:
- `GET http://127.0.0.1:8000/healthz`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Project structure
Code lives under `src/app/` and is split into:
- `api/`: FastAPI routers + request/response schemas
- `services/`: use-cases (screening, interviewing, reporting)
- `domain/`: policies and domain-centric logic
- `persistence/`: SQLModel tables + repositories + DB session
- `llm/`: LLM abstraction (fake client included for demo)

## Notes
- Default DB is SQLite: `sqlite:///./ai_interview.db`
- Configure via environment variables (prefix `AIS_`), e.g. `AIS_DATABASE_URL`.
