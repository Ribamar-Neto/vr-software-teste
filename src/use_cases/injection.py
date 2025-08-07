from fastapi import Request

from src.repositories import NotificationRepository
from src.repositories.notification_repository_in_memory import NotificationRepositoryInMemory
from src.services import NotificationService
from src.services.notification_service_rabbitmq import NotificationServiceRabbitMQ
from src.settings.broker.broker_settings import broker_settings
from src.use_cases.create_notification_use_case import CreateNotificationUseCase
from src.use_cases.find_notification_use_case import FindNotificationUseCase


def get_notification_repository(request: Request) -> NotificationRepository:
    """Obtém o repository do estado da aplicação ou cria um novo"""
    if hasattr(request.app.state, 'notification_repository'):
        return request.app.state.notification_repository
    return NotificationRepositoryInMemory()


def get_notification_service(request: Request) -> NotificationService:
    """Obtém o service do estado da aplicação ou cria um novo"""
    if hasattr(request.app.state, 'notification_service'):
        return request.app.state.notification_service
    return NotificationServiceRabbitMQ(
        url=broker_settings.url, queue_name=broker_settings.queue_input_name
    )


def create_notification_usecase(request: Request) -> CreateNotificationUseCase:
    return CreateNotificationUseCase(
        notification_repository=get_notification_repository(request),
        notification_service=get_notification_service(request),
    )


def find_notification_usecase(request: Request) -> FindNotificationUseCase:
    return FindNotificationUseCase(
        notification_repository=get_notification_repository(request),
    )
