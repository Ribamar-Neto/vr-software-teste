from abc import ABC, abstractmethod
from uuid import UUID

from src.entities import Notification


class NotificationRepository(ABC):
    @abstractmethod
    async def create(self, notification: Notification) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, notification: Notification) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, notification: Notification) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find(self, trace_id: UUID) -> Notification | None:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list[Notification]:
        raise NotImplementedError
