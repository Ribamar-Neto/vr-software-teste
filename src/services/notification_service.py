from abc import ABC, abstractmethod

from src.entities import Notification


class NotificationService(ABC):
    @abstractmethod
    async def send_notification(self, notification: Notification) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def mark_as_sent(self, notification_id: str) -> bool:
        raise NotImplementedError
