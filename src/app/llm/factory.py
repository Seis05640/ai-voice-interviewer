from __future__ import annotations

from app.config import settings
from app.llm.base import LLMClient
from app.llm.fake_client import FakeLLMClient


def get_llm_client() -> LLMClient:
    provider = settings.llm_provider.lower()
    if provider == "fake":
        return FakeLLMClient()

    raise ValueError(
        "Unknown AIS_LLM_PROVIDER. For the scaffold only 'fake' is implemented."
    )
