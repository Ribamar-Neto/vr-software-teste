from src.entities import Notification
from src.repositories import NotificationRepository
from src.schemas import CreateNotificationInput, CreateNotificationOutput
from src.services import NotificationService


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
        await self.notification_service.send_notification(notification)
        return CreateNotificationOutput.from_entity(notification)
