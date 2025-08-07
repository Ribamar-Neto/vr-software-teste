from uuid import UUID

from src.exceptions import NotificationNotFoundError
from src.repositories import NotificationRepository
from src.schemas import NotificationOutput


class FindNotificationUseCase:
    def __init__(self, notification_repository: NotificationRepository) -> None:
        self.notification_repository = notification_repository

    async def execute(self, trace_id: UUID) -> NotificationOutput:
        notification = await self.notification_repository.find(trace_id)
        if notification is None:
            raise NotificationNotFoundError
        return NotificationOutput.from_entity(notification)
