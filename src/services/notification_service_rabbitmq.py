import logging

import aio_pika
from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractRobustConnection

from src.entities import Notification

from .notification_service import NotificationService

logger = logging.getLogger(__name__)


class NotificationServiceRabbitMQ(NotificationService):
    def __init__(self, url: str, queue_name: str) -> None:
        self.url = url
        self.queue_name = queue_name
        self.prefetch_count = 10

    async def connect(self) -> None:
        try:
            self.connection: AbstractRobustConnection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=self.prefetch_count)
            self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
            logger.info('Connected to RabbitMQ successfully')
        except Exception:
            logger.exception('Error connecting to RabbitMQ')
            raise

    async def disconnect(self) -> None:
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            logger.info('Disconnected from RabbitMQ')

    async def send_notification(self, notification: Notification) -> bool:
        try:
            if not self.channel:
                await self.connect()
            message_body = notification.to_dict()
            await self.channel.default_exchange.publish(  # type: ignore[union-attr]
                Message(body=message_body, delivery_mode=DeliveryMode.PERSISTENT),  # type: ignore[arg-type]
                routing_key=self.queue_name,
            )
            logger.info('Notification %s sent successfully', notification.trace_id)
        except Exception:
            logger.exception('Error sending notification %s', notification.trace_id)
            return False
        else:
            return True

    async def mark_as_delivered(self, notification_id: str) -> bool:
        try:
            logger.info('Notification %s marked as delivered', notification_id)
        except Exception:
            logger.exception('Error marking notification %s as delivered', notification_id)
            return False
        else:
            return True
