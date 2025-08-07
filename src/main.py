from fastapi.routing import APIRouter

from src.repositories.notification_repository_in_memory import NotificationRepositoryInMemory
from src.routers import notification_router
from src.services.notification_service_rabbitmq import NotificationServiceRabbitMQ
from src.settings.broker.broker_settings import broker_settings
from src.settings.server.fastapi import app

routers: list[APIRouter] = [notification_router]
routers.sort(key=lambda router: router.prefix)


def sort_routes_by_path(router: APIRouter) -> None:
    router.routes.sort(key=lambda route: route.path)  # type: ignore[attr-defined]


for router in routers:
    sort_routes_by_path(router)
    app.include_router(router)


@app.on_event('startup')
async def startup_event() -> None:
    """Inicia o consumidor RabbitMQ quando a aplicação iniciar"""
    repository = NotificationRepositoryInMemory()
    notification_service = NotificationServiceRabbitMQ(
        url=broker_settings.url, queue_name=broker_settings.queue_input_name
    )

    try:
        await notification_service.start_consumer(repository)
    except Exception:
        notification_service.connection = None
        notification_service.channel = None

    app.state.notification_repository = repository
    app.state.notification_service = notification_service


@app.on_event('shutdown')
async def shutdown_event() -> None:
    if hasattr(app.state, 'notification_service'):
        await app.state.notification_service.disconnect()
