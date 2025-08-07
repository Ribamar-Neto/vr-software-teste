from uuid import UUID

from pydantic import BaseModel, Field

from src.enums import NotificationTypeEnum


class CreateNotificationInput(BaseModel):
    message_id: UUID | None = Field(default=None, examples=['550e8400-e29b-41d4-a716-446655440000'])
    message_content: str = Field(examples=['Notification content example'])
    notification_type: NotificationTypeEnum = Field(examples=[NotificationTypeEnum.EMAIL])
