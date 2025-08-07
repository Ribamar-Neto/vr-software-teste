import asyncio
import json
import logging
import random
from typing import Any

import aio_pika
from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractRobustConnection

from src.entities import Notification
from src.enums import NotificationStatusEnum
from src.repositories import NotificationRepository
from src.settings.broker.broker_settings import broker_settings

from .notification_service import NotificationService

logger = logging.getLogger(__name__)


class NotificationServiceRabbitMQ(NotificationService):
    def __init__(self, url: str, queue_name: str) -> None:
        self.url = url
        self.queue_name = queue_name
        self.prefetch_count = 10
        self.connection: AbstractRobustConnection | None = None
        self.channel = None
        self.queue = None

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
                Message(
                    body=json.dumps(message_body).encode(), delivery_mode=DeliveryMode.PERSISTENT
                ),
                routing_key=self.queue_name,
            )
            logger.info('Notification %s sent successfully', notification.trace_id)
        except Exception:
            logger.exception('Error sending notification %s', notification.trace_id)
            return False
        else:
            return True

    async def publish_to_queue(self, message: dict[str, Any], queue_name: str) -> bool:
        """Publica uma mensagem em uma fila específica"""
        try:
            if not self.channel:
                await self.connect()

            queue = await self.channel.declare_queue(queue_name, durable=True)

            await self.channel.default_exchange.publish(
                Message(body=json.dumps(message).encode(), delivery_mode=DeliveryMode.PERSISTENT),
                routing_key=queue_name,
            )
            logger.info('Message published to queue %s successfully', queue_name)
            return True
        except Exception as e:
            logger.warning('Error publishing message to queue %s: %s', queue_name, e)
            return True

    async def mark_as_delivered(self, notification_id: str) -> bool:
        try:
            logger.info('Notification %s marked as delivered', notification_id)
        except Exception:
            logger.exception('Error marking notification %s as delivered', notification_id)
            return False
        else:
            return True

    async def start_consumer(self, repository: NotificationRepository) -> None:
        """Inicia o consumidor para processar mensagens da fila de entrada"""
        try:
            if not self.channel:
                await self.connect()

            input_queue = await self.channel.declare_queue(
                broker_settings.queue_input_name, durable=True
            )
            retry_queue = await self.channel.declare_queue(
                broker_settings.queue_retry_name, durable=True
            )
            validation_queue = await self.channel.declare_queue(
                broker_settings.queue_validation_name, durable=True
            )

            async def process_message(message: aio_pika.IncomingMessage) -> None:
                async with message.process():
                    try:
                        body = json.loads(message.body.decode())
                        trace_id = body.get('trace_id')
                        message_id = body.get('message_id')
                        message_content = body.get('message_content')
                        notification_type = body.get('notification_type')

                        logger.info('Processing message with trace_id: %s', trace_id)

                        if random.random() < 0.12:  # 12% de chance de falha
                            logger.warning('Random failure occurred for trace_id: %s', trace_id)

                            notification = await repository.find(trace_id)
                            if notification:
                                notification.update_status(
                                    NotificationStatusEnum.INITIAL_PROCESSING_FAILURE
                                )
                                await repository.update(notification)

                            await self.publish_to_queue(body, broker_settings.queue_retry_name)
                            logger.info('Message sent to retry queue: %s', trace_id)
                        else:
                            await asyncio.sleep(random.uniform(1, 1.5))

                            notification = await repository.find(trace_id)
                            if notification:
                                notification.update_status(
                                    NotificationStatusEnum.PROCESSING_INTERMEDIATE
                                )
                                await repository.update(notification)

                            await self.publish_to_queue(body, broker_settings.queue_validation_name)
                            logger.info('Message sent to validation queue: %s', trace_id)

                    except Exception as e:
                        logger.exception('Error processing message: %s', e)
                        await message.reject(requeue=False)

            await input_queue.consume(process_message)
            logger.info('Consumer started for queue: %s', broker_settings.queue_input_name)

        except Exception as e:
            logger.exception('Error starting consumer: %s', e)
            raise
