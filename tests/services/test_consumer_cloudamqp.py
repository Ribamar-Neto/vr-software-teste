#!/usr/bin/env python3
"""
Script de teste para verificar o funcionamento do consumidor RabbitMQ no CloudAMQP
"""

import asyncio
import json
from uuid import uuid4

import aio_pika

from src.settings.broker.broker_settings import broker_settings


async def test_consumer_cloudamqp() -> None:
    """Testa o consumidor enviando uma mensagem de teste para o CloudAMQP"""

    try:
        connection = await aio_pika.connect_robust(broker_settings.url)
        channel = await connection.channel()

        queue = await channel.declare_queue(broker_settings.queue_input_name, durable=True)

        test_message = {
            'trace_id': str(uuid4()),
            'message_id': str(uuid4()),
            'message_content': 'Teste de mensagem do consumidor no CloudAMQP',
            'notification_type': 'email',
            'status': 'received',
        }

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(test_message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=broker_settings.queue_input_name,
        )

        await asyncio.sleep(5)

        retry_queue = await channel.declare_queue(broker_settings.queue_retry_name, durable=True)
        validation_queue = await channel.declare_queue(
            broker_settings.queue_validation_name, durable=True
        )

        retry_message = await retry_queue.get(fail=False)
        if retry_message:
            await retry_message.ack()

        validation_message = await validation_queue.get(fail=False)
        if validation_message:
            await validation_message.ack()

        await connection.close()

    except Exception:
        pass


if __name__ == '__main__':
    asyncio.run(test_consumer_cloudamqp())
