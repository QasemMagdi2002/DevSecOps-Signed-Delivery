from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="devsecops-demo", alias="APP_NAME")
    app_env: str = Field(default="dev", alias="APP_ENV")
    app_message: str = Field(default="Secure delivery demo", alias="APP_MESSAGE")
    app_secret: str = Field(default="", alias="APP_SECRET")

    host: str = Field(default="0.0.0.0", alias="APP_HOST")
    port: int = Field(default=8000, alias="APP_PORT")
    log_level: str = Field(default="info", alias="APP_LOG_LEVEL")
    workers: int = Field(default=1, alias="APP_WORKERS")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()