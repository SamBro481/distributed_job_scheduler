from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    type: str
    payload: dict[str, Any]
    priority: int = 0
    run_at: datetime | None = None


class JobResponse(BaseModel):
    id: int
    type: str
    payload: dict[str, Any]
    status: str
    priority: int
    retries: int
    max_retries: int
    run_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)