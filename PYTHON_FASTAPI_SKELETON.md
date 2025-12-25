# Python FastAPI Skeleton - Complete Implementation

This document describes the complete Python FastAPI skeleton that has been implemented in this repository.

## ✅ Requirements Met

1. **✅ Virtual environment friendly** - Uses `pyproject.toml` with setuptools
2. **✅ FastAPI backend** - Fully implemented with proper structure  
3. **✅ Clear separation of services** - Layered architecture
4. **✅ Minimal but runnable example** - Multiple working endpoints

## 📁 Folder Structure

```
src/app/
├── __init__.py
├── main.py                  # FastAPI app creation
├── config.py                # Configuration management
├── api/
│   ├── __init__.py
│   ├── deps.py              # Dependency injection
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py         # Health check endpoint
│   │   ├── jobs.py          # Jobs CRUD endpoints
│   │   ├── candidates.py    # Candidates CRUD endpoints
│   │   ├── interviews.py    # Interview endpoints
│   │   └── reports.py       # Reporting endpoints
│   └── schemas/
│       ├── __init__.py
│       ├── job.py           # Job schemas
│       ├── candidate.py     # Candidate schemas
│       ├── interview.py     # Interview schemas
│       └── report.py        # Report schemas
├── services/
│   ├── __init__.py
│   ├── ingestion_service.py # Candidate ingestion
│   ├── screening_service.py # Screening logic
│   ├── interview_service.py # Interview logic
│   ├── reporting_service.py # Reporting logic
│   └── evaluation_service.py # Evaluation logic
├── domain/
│   ├── __init__.py
│   ├── policies/
│   │   ├── __init__.py
│   │   ├── shortlisting.py   # Screening policies
│   │   ├── scoring_policy.py # Scoring logic
│   │   └── interview_policy.py # Interview policies
├── persistence/
│   ├── __init__.py
│   ├── db.py                # Database session management
│   ├── tables.py            # SQLAlchemy models
│   └── repositories/
│       ├── __init__.py
│       ├── job_repo.py      # Job repository
│       ├── candidate_repo.py # Candidate repository
│       ├── application_repo.py # Application repository
│       ├── interview_repo.py # Interview repository
│       └── report_repo.py   # Report repository
├── llm/
│   ├── __init__.py
│   ├── base.py              # LLM interface
│   ├── factory.py          # LLM factory
│   └── fake_client.py      # Fake LLM for demo
├── utils/
│   ├── __init__.py
│   ├── errors.py            # Custom exceptions
│   └── logging.py          # Logging configuration
└── workers/
    ├── __init__.py
    └── background.py        # Background workers
```

## 🚀 Quick Start

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Run the application
uvicorn app.main:app --reload

# Test the health endpoint
curl http://127.0.0.1:8000/healthz

# Access Swagger UI
open http://127.0.0.1:8000/docs
```

## 🎯 Key Features

### 1. Virtual Environment Friendly
- Uses `pyproject.toml` with setuptools
- Install in development mode: `pip install -e .`
- All dependencies managed via `pyproject.toml`

### 2. FastAPI Backend
- Proper FastAPI app structure with `main.py`
- RESTful API design with proper HTTP methods
- Automatic OpenAPI/Swagger documentation
- Health check endpoint

### 3. Clear Separation of Services
- **API Layer**: FastAPI routers and Pydantic schemas
- **Service Layer**: Business logic and use cases
- **Domain Layer**: Core business rules and policies
- **Persistence Layer**: Database models and repositories
- **LLM Layer**: AI/ML abstraction for future integration

### 4. Minimal but Runnable Example
- Working health endpoint: `GET /healthz`
- Jobs CRUD: Create and list jobs
- Candidates CRUD: Create and list candidates
- Screening functionality: Screen candidates against jobs
- Interview functionality: Start and manage interviews
- Reporting functionality: Generate reports

## 🔧 Configuration

```python
# config.py
class Settings(BaseSettings):
    app_name: str = "AI Interview System"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./ai_interview.db"
    llm_provider: str = "fake"
```

Configure via environment variables with `AIS_` prefix:
```bash
export AIS_DATABASE_URL="postgresql://user:pass@localhost/db"
export AIS_LLM_PROVIDER="openai"
```

## 📊 Database

- SQLite by default (`sqlite:///./ai_interview.db`)
- SQLAlchemy ORM for database operations
- Proper repository pattern for data access
- Tables: Jobs, Candidates, Applications, InterviewSessions, InterviewMessages, Reports

## 🤖 LLM Integration

- Abstract LLM interface for future AI integration
- Fake LLM client included for development
- Easy to swap with real LLM providers

## 🧪 Testing

The skeleton includes a test script that verifies basic functionality:

```bash
python test_basic_functionality.py
```

This tests:
- Health endpoint (`/healthz`)
- Documentation endpoint (`/docs`)
- Server startup and response handling

## 🎉 Summary

This FastAPI skeleton provides a complete, production-ready foundation for building AI-powered applications with:

- ✅ Clean, modular architecture
- ✅ Proper separation of concerns
- ✅ Virtual environment support
- ✅ Database integration
- ✅ API documentation
- ✅ Configuration management
- ✅ Error handling
- ✅ Logging
- ✅ LLM abstraction layer

The skeleton is ready to use and can be extended with additional functionality as needed.