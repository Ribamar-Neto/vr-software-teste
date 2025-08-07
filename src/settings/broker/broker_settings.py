from pydantic_settings import BaseSettings, SettingsConfigDict

from src.enums import EnvironmentEnum


class BrokerSettings(BaseSettings):
    BROKER_USERNAME: str = 'guest'
    BROKER_PASSWORD: str = 'guest'
    BROKER_HOST: str = 'localhost'
    BROKER_PORT: int = 5672
    BROKER_VHOST: str = '/'
    BROKER_URL: str | None = None
    ENVIRONMENT: str = EnvironmentEnum.DEVELOPMENT

    @property
    def url(self) -> str:
        if self.ENVIRONMENT == EnvironmentEnum.TESTING:
            return 'amqp://guest:guest@localhost:5673/'

        # Se BROKER_URL estiver definido, use ele diretamente
        if self.BROKER_URL:
            return self.BROKER_URL

        # Senão, construa a URL a partir das partes
        return f'amqp://{self.BROKER_USERNAME}:{self.BROKER_PASSWORD}@{self.BROKER_HOST}:{self.BROKER_PORT}/{self.BROKER_VHOST}'

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
