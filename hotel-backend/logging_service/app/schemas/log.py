"""Pydantic схемы для логов."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class LogEntryBase(BaseModel):
    """Базовая схема записи лога."""

    level: int = Field(..., ge=0, le=3, description="Уровень лога (0-3)")
    message: str = Field(..., min_length=1, max_length=1000, description="Сообщение лога")
    service_name: str = Field(..., min_length=1, max_length=255, description="Имя сервиса")


class LogEntryCreate(LogEntryBase):
    """Схема для создания записи лога."""

    timestamp: str | None = Field(None, description="Временная метка в ISO формате")


class LogEntryResponse(LogEntryBase):
    """Схема ответа с информацией о записи лога."""

    id: UUID
    created_at: datetime

    class Config:
        """Конфигурация Pydantic."""

        from_attributes = True


class LogEntryListResponse(BaseModel):
    """Схема ответа со списком логов."""

    logs: list[LogEntryResponse]
    total: int

