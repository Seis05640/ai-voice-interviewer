from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AIS_",
        extra="ignore",
    )

    app_name: str = "AI Interview System"
    log_level: str = "INFO"

    database_url: str = Field(default="sqlite:///./ai_interview.db")
    llm_provider: str = Field(default="fake")


settings = Settings()
