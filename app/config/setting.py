import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
import uuid


class Settings(BaseSettings):
    # General Settings
    LOG_LEVEL: str | int | None = 'INFO'
    SWAGGER_ENABLED: bool = True

    # Security
    API_KEY: str = uuid.uuid4().__str__()

    # HA
    PERSON_UUIDS: dict = {}

    # broker RabbitMQ
    BROKER_HOST: str = 'localhost'
    BROKER_PORT: int = 5672
    BROKER_USERNAME: str = 'username'
    BROKER_PASSWORD: str = 'password'
    BROKER_EXCHANGE: str = 'exchange'
    BROKER_ROUTING_KEY_TRACKING: str = 'routing-key'
    BROKER_ROUTING_KEY_FOOD: str = 'routing-key'

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


dotenv.load_dotenv()
setting = Settings()
