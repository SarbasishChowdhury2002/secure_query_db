from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Search encryption key
    SEARCH_KEY: str = "week3-secret-key"

    # Database
    DB_PASSWORD: str = "2002"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"

    # App
    APP_NAME: str = "Secure Query Processing System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()