from abc import ABC, abstractmethod
from typing import Any

from src.entities import Notification


class NotificationService(ABC):
    @abstractmethod
    async def send_notification(self, notification: Notification) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def mark_as_delivered(self, notification_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def publish_to_queue(self, message: dict[str, Any], queue_name: str) -> bool:
        raise NotImplementedError
