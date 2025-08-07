from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class CreateNotificationOutput(BaseModel):
    message_id: UUID | None = Field(default=None, examples=['123e4567-e89b-12d3-a456-426614174000'])
    trace_id: UUID | None = Field(default=None, examples=['224e4687-e89b-12d3-a456-426697174000'])
