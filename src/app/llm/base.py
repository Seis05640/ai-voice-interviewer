from __future__ import annotations

from typing import Protocol


class LLMClient(Protocol):
    def generate(self, *, system_prompt: str | None = None, user_prompt: str) -> str: ...
