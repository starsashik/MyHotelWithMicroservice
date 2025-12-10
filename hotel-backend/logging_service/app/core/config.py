"""Конфигурация приложения."""

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

    # База данных
    DATABASE_URL: str = os.getenv(
        "LOGGING_DATABASE_URL",
        "postgresql+asyncpg://postgres:admin@localhost:5454/logging_db"
    )

    # RabbitMQ
    RABBITMQ_URL: str = os.getenv(
        "RABBITMQ_URL",
        "amqp://guest:guest@rabbitmq:5672/"
    )
    RABBITMQ_QUEUE: str = os.getenv("RABBITMQ_QUEUE", "logs_queue")

    # Приложение
    APP_NAME: str = "Logging Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        """Конфигурация Pydantic."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()

