import pytest

from src.entities import Notification
from src.enums.notification_type_enum import NotificationTypeEnum
from src.repositories import NotificationRepository
from src.services import NotificationService
from src.use_cases import CreateNotificationUseCase, FindNotificationUseCase


@pytest.fixture
def notification_repository() -> NotificationRepository:
    return NotificationRepository


@pytest.fixture
def notification_service() -> NotificationService:
    return NotificationService


@pytest.fixture
def find_notification_usecase(
    notification_repository: NotificationRepository,
) -> FindNotificationUseCase:
    return FindNotificationUseCase(notification_repository)


@pytest.fixture
def create_notification_usecase(
    notification_repository: NotificationRepository,
    notification_service: NotificationService,
) -> CreateNotificationUseCase:
    return CreateNotificationUseCase(notification_repository, notification_service)


@pytest.fixture
def notification() -> Notification:
    return Notification.create(
        message_id='550e8400-e29b-41d4-a716-446655440000',
        message_content='Notification content example',
        notification_type=NotificationTypeEnum.EMAIL,
    )
