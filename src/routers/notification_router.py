from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from src.schemas import (
    CreateNotificationInput,
    CreateNotificationOutput,
    NotificationOutput,
)
from src.use_cases import (
    CreateNotificationUseCase,
    FindNotificationUseCase,
    create_notification_usecase,
    find_notification_usecase,
)

router = APIRouter(prefix='/notifications', tags=['Notifications'])


@router.post('', status_code=status.HTTP_202_ACCEPTED)
async def create_notification(
    input_data: CreateNotificationInput,
    usecase: Annotated[CreateNotificationUseCase, Depends(create_notification_usecase)],
) -> CreateNotificationOutput:
    return await usecase.execute(input_data=input_data)


@router.get('/status/{trace_id}', status_code=status.HTTP_200_OK)
async def find_notification(
    trace_id: UUID,
    usecase: Annotated[FindNotificationUseCase, Depends(find_notification_usecase)],
) -> NotificationOutput:
    return await usecase.execute(trace_id=trace_id)
