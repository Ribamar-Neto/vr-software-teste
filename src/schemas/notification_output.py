from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from entities import Notification
from src.enums import (
    NotificationStatusEnum,
    NotificationTypeEnum,
)


class NotificationOutput(BaseModel):
    trace_id: UUID = Field(default=None, examples=['224e4687-e89b-12d3-a456-426697174000'])
    message_id: UUID | None = Field(default=None, examples=['123e4567-e89b-12d3-a456-426614174000'])
    message_content: str = Field(default=None, examples=['Notification content'])
    notification_type: NotificationTypeEnum = Field(default=NotificationTypeEnum.EMAIL)
    status: NotificationStatusEnum = Field(default=NotificationStatusEnum.RECEIVED)

    @staticmethod
    def from_entity(notification: Notification) -> NotificationOutput:
        return NotificationOutput(
            trace_id=notification.trace_id,
            message_id=notification.message_id,
            message_content=notification.message_content,
            notification_type=notification.notification_type,
            status=notification.status,
        )
