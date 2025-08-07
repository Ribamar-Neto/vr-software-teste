from src.entities import Notification
from src.repositories import NotificationRepository
from src.schemas import CreateNotificationInput, CreateNotificationOutput
from src.services import NotificationService
from src.settings.broker.broker_settings import broker_settings


class CreateNotificationUseCase:
    def __init__(
        self,
        notification_repository: NotificationRepository,
        notification_service: NotificationService,
    ) -> None:
        self.notification_repository = notification_repository
        self.notification_service = notification_service

    async def execute(self, input_data: CreateNotificationInput) -> CreateNotificationOutput:
        notification = Notification.create(
            message_id=input_data.message_id,
            message_content=input_data.message_content,
            notification_type=input_data.notification_type,
        )
        await self.notification_repository.create(notification)

        # Publica na fila de entrada do RabbitMQ
        await self.notification_service.publish_to_queue(
            notification.to_dict(), broker_settings.queue_input_name
        )

        return CreateNotificationOutput.from_entity(notification)
