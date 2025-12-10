"""Общие настройки конфигурации для всех микросервисов."""

import os
from typing import Optional

from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    """Общие настройки для всех микросервисов."""

    # RabbitMQ (если используется)
    RABBITMQ_URL: str = os.getenv(
        "RABBITMQ_URL",
        "amqp://guest:guest@localhost:5672/"
    )
    RABBITMQ_QUEUE: str = os.getenv("RABBITMQ_QUEUE", "logs_queue")

    # JWT (общий секрет для всех сервисов)
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Общие настройки
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        """Конфигурация Pydantic."""

        env_file = ".env"
        case_sensitive = True


# Экземпляр общих настроек (можно импортировать в сервисах при необходимости)
common_settings = CommonSettings()

