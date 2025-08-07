from unittest.mock import AsyncMock

from src.entities import Notification
from src.repositories.notification_repository_in_memory import NotificationRepositoryInMemory
from src.schemas import CreateNotificationInput
from src.services.notification_service_rabbitmq import NotificationServiceRabbitMQ
from src.use_cases import CreateNotificationUseCase


async def test_create_notification_usecase(
    notification: Notification,
    create_notification_usecase: CreateNotificationUseCase,
    notification_repository: NotificationRepositoryInMemory,
    notification_service: NotificationServiceRabbitMQ,
) -> None:
    notification_repository.create = AsyncMock()
    notification_service.publish_to_queue = AsyncMock(return_value=True)
    input_data = CreateNotificationInput(
        message_id=notification.message_id,
        message_content=notification.message_content,
        notification_type=notification.notification_type,
    )
    created_notification = await create_notification_usecase.execute(input_data)

    assert created_notification.trace_id is not None
    assert created_notification.message_id is not None
