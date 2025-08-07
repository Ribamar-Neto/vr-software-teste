from pydantic_settings import BaseSettings, SettingsConfigDict

from src.enums import EnvironmentEnum


class BrokerSettings(BaseSettings):
    BROKER_USERNAME: str | None = None
    BROKER_PASSWORD: str | None = None
    BROKER_HOST: str | None = None
    BROKER_PORT: int | None = None
    ENVIRONMENT: str = EnvironmentEnum.DEVELOPMENT

    @property
    def url(self) -> str:
        if self.ENVIRONMENT == EnvironmentEnum.TESTING:
            return 'amqp://guest:guest@localhost:5673/'
        return f'amqp://{self.BROKER_USERNAME}:{self.BROKER_PASSWORD}@{self.BROKER_HOST}:{self.BROKER_PORT}/'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='allow')

    @property
    def queue_input_name(self) -> str:
        return 'fila.notificacao.entrada.ribamarneto'

    @property
    def queue_retry_name(self) -> str:
        return 'fila.notificacao.retry.ribamarneto'

    @property
    def queue_validation_name(self) -> str:
        return 'fila.notificacao.validacao.ribamarneto'

    @property
    def queue_dlq_name(self) -> str:
        return 'fila.notificacao.dlq.ribamarneto'


broker_settings = BrokerSettings()
