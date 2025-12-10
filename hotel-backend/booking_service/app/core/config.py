"""Конфигурация приложения."""

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

    # RabbitMQ (для отправки логов)
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    RABBITMQ_QUEUE: str = os.getenv("RABBITMQ_QUEUE", "logs_queue")

    # База данных
    DATABASE_URL: str = os.getenv(
        "BOOKING_DATABASE_URL",
        "postgresql+asyncpg://postgres:admin@localhost:5454/booking_db"
    )

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"

    # Приложение
    APP_NAME: str = "Booking Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        """Конфигурация Pydantic."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()

