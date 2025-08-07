from uuid import UUID

from pydantic import BaseModel, Field

from src.enums.notification_type_enum import NotificationTypeEnum


class CreateNotificationInput(BaseModel):
    message_id: UUID | None = Field(default=None, examples=['123e4567-e89b-12d3-a456-426614174000'])
    message_content: str = Field(default=None, examples=['Notification content'])
    notification_type: NotificationTypeEnum = Field(default=NotificationTypeEnum.EMAIL)
