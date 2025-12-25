from __future__ import annotations

from app.llm.base import LLMClient


class FakeLLMClient(LLMClient):
    def generate(self, *, system_prompt: str | None = None, user_prompt: str) -> str:
        if system_prompt:
            return f"[FAKE_LLM]\nSYSTEM: {system_prompt}\nUSER: {user_prompt}"
        return f"[FAKE_LLM] {user_prompt}"
