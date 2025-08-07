from unittest.mock import AsyncMock

import pytest

from src.entities import Notification
from src.exceptions import NotificationNotFoundError
from src.repositories import NotificationRepository
from src.schemas import NotificationOutput
from src.use_cases import FindNotificationUseCase


async def test_find_notification_usecase(
    notification: Notification,
    find_notification_usecase: FindNotificationUseCase,
    notification_repository: NotificationRepository,
) -> None:
    notification_repository.find = AsyncMock(return_value=notification)
    result = await find_notification_usecase.execute(notification.trace_id)

    assert result == NotificationOutput.from_entity(notification)


async def test_find_notification_usecase_not_found(
    find_notification_usecase: FindNotificationUseCase,
    notification_repository: NotificationRepository,
) -> None:
    notification_repository.find = AsyncMock(return_value=None)

    with pytest.raises(NotificationNotFoundError) as error:
        await find_notification_usecase.execute('non-existent-id')

    assert str(error.value) == NotificationNotFoundError.message
