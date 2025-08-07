from uuid import UUID

from src.entities import Notification

from .notification_repository import NotificationRepository


class NotificationRepositoryInMemory(NotificationRepository):
    def __init__(self) -> None:
        self._notifications: dict[UUID, Notification] = {}

    async def create(self, notification: Notification) -> None:
        self._notifications[notification.trace_id] = notification

    async def update(self, notification: Notification) -> None:
        self._notifications[notification.trace_id] = notification

    async def delete(self, notification: Notification) -> None:
        del self._notifications[notification.trace_id]

    async def find(self, trace_id: UUID) -> Notification | None:
        return self._notifications.get(trace_id)

    async def find_all(self) -> list[Notification]:
        return list(self._notifications.values())
