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
    PERSON_UUIDS: dict

    # broker RabbitMQ
    BROKER_HOST: str
    BROKER_PORT: int
    BROKER_USERNAME: str
    BROKER_PASSWORD: str
    BROKER_EXCHANGE: str
    BROKER_ROUTING_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


dotenv.load_dotenv()
setting = Settings()
