import pytest

from src.entities import Notification
from src.enums.notification_type_enum import NotificationTypeEnum
from src.repositories.notification_repository_in_memory import NotificationRepositoryInMemory
from src.services.notification_service_rabbitmq import NotificationServiceRabbitMQ
from src.use_cases import CreateNotificationUseCase, FindNotificationUseCase


@pytest.fixture
def notification_repository() -> NotificationRepositoryInMemory:
    return NotificationRepositoryInMemory()


@pytest.fixture
def notification_service() -> NotificationServiceRabbitMQ:
    return NotificationServiceRabbitMQ(url='amqp://test', queue_name='test_queue')


@pytest.fixture
def find_notification_usecase(
    notification_repository: NotificationRepositoryInMemory,
) -> FindNotificationUseCase:
    return FindNotificationUseCase(notification_repository)


@pytest.fixture
def create_notification_usecase(
    notification_repository: NotificationRepositoryInMemory,
    notification_service: NotificationServiceRabbitMQ,
) -> CreateNotificationUseCase:
    return CreateNotificationUseCase(notification_repository, notification_service)


@pytest.fixture
def notification() -> Notification:
    return Notification.create(
        message_id='550e8400-e29b-41d4-a716-446655440000',
        message_content='Notification content example',
        notification_type=NotificationTypeEnum.EMAIL,
    )
