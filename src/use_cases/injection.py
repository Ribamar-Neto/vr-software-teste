from src.repositories import NotificationRepositoryInMemory
from src.services import RabbitMQNotificationService
from src.settings.broker import broker_settings
from src.use_cases import CreateNotificationUseCase, FindNotificationUseCase


def create_notification_usecase() -> CreateNotificationUseCase:
    notification_repository = NotificationRepositoryInMemory()
    notification_service = RabbitMQNotificationService(
        url=broker_settings.url, queue_name=broker_settings.queue_input_name
    )
    return CreateNotificationUseCase(notification_repository, notification_service)


def find_notification_usecase() -> FindNotificationUseCase:
    notification_repository = NotificationRepositoryInMemory()
    return FindNotificationUseCase(notification_repository)
