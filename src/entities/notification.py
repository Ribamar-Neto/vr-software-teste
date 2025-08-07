from __future__ import annotations

from uuid import UUID, uuid4

from src.enums import NotificationStatusEnum, NotificationTypeEnum


class Notification:
    def __init__(
        self,
        trace_id: UUID,
        message_id: UUID,
        message_content: str,
        notification_type: NotificationTypeEnum,
        status: NotificationStatusEnum,
    ) -> None:
        self.trace_id = trace_id
        self.message_id = message_id
        self.message_content = message_content
        self.notification_type = notification_type
        self.status = status

    def update_status(self, new_status: NotificationStatusEnum) -> None:
        self.status = new_status

    @classmethod
    def create(
        cls, message_id: UUID | None, message_content: str, notification_type: NotificationTypeEnum
    ) -> Notification:
        return cls(
            trace_id=uuid4(),
            message_id=message_id or uuid4(),
            message_content=message_content,
            notification_type=notification_type,
            status=NotificationStatusEnum.RECEIVED,
        )

    def to_dict(self) -> dict:
        return {
            'trace_id': self.trace_id,
            'message_id': self.message_id,
            'message_content': self.message_content,
            'notification_type': self.notification_type,
            'status': self.status,
        }
