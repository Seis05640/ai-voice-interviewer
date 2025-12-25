from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    description: str


class JobRead(BaseModel):
    id: str
    title: str
    description: str
    created_at: datetime
