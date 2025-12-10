"""Pydantic схемы для комнаты."""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class RoomBase(BaseModel):
    """Базовая схема комнаты."""

    room_number: str = Field(..., min_length=1, max_length=50, description="Номер комнаты")
    room_type: int = Field(..., description="Тип комнаты")
    price_per_night: Decimal = Field(..., gt=0, description="Цена за ночь")
    img_url: str | None = Field(None, max_length=500, description="URL изображения комнаты")


class RoomCreate(RoomBase):
    """Схема для создания комнаты."""

    pass


class RoomUpdate(BaseModel):
    """Схема для обновления комнаты."""

    room_number: str | None = Field(None, min_length=1, max_length=50, description="Номер комнаты")
    room_type: int | None = Field(None, description="Тип комнаты")
    price_per_night: Decimal | None = Field(None, gt=0, description="Цена за ночь")
    img_url: str | None = Field(None, max_length=500, description="URL изображения комнаты")


class RoomResponse(RoomBase):
    """Схема ответа с информацией о комнате."""

    id: UUID
    hotel_id: UUID

    class Config:
        """Конфигурация Pydantic."""

        from_attributes = True

