"""Pydantic схемы для отеля."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class HotelBase(BaseModel):
    """Базовая схема отеля."""

    name: str = Field(..., min_length=1, max_length=255, description="Название отеля")
    location: str = Field(..., min_length=1, max_length=255, description="Местоположение отеля")
    description: str = Field(..., min_length=1, description="Описание отеля")
    img_url: str | None = Field(None, max_length=500, description="URL изображения отеля")


class HotelCreate(HotelBase):
    """Схема для создания отеля."""

    pass


class HotelUpdate(BaseModel):
    """Схема для обновления отеля."""

    name: str | None = Field(None, min_length=1, max_length=255, description="Название отеля")
    location: str | None = Field(None, min_length=1, max_length=255, description="Местоположение отеля")
    description: str | None = Field(None, min_length=1, description="Описание отеля")
    img_url: str | None = Field(None, max_length=500, description="URL изображения отеля")


class HotelResponse(HotelBase):
    """Схема ответа с информацией об отеле."""

    id: UUID
    created_at: datetime

    class Config:
        """Конфигурация Pydantic."""

        from_attributes = True

