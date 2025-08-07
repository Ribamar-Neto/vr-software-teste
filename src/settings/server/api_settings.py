from pydantic import BaseModel


class APISettings(BaseModel):
    title: str = 'Desafio VR Software API'
    description: str = 'API para sistema de notificações'
    debug: bool = True


api_settings = APISettings()
