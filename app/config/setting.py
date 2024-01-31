import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # General Settings
    LOG_LEVEL: str | int | None = 'INFO'
    SWAGGER_ENABLED: bool = True

    # Security
    API_KEY: str

    # HA
    PERSON_UUIDS: dict

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


dotenv.load_dotenv()
setting = Settings()
