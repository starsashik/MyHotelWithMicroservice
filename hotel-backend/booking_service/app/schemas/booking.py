"""Pydantic схемы для бронирования."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from app.schemas.room import RoomResponse


class BookingBase(BaseModel):
    """Базовая схема бронирования."""

    room_id: UUID = Field(..., description="ID комнаты")
    check_in_date: date = Field(..., description="Дата заезда")
    check_out_date: date = Field(..., description="Дата выезда")

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingBase":
        """
        Валидация дат бронирования.

        Returns:
            BookingBase: Экземпляр схемы

        Raises:
            ValueError: Если дата выезда меньше или равна дате заезда
        """
        if self.check_out_date <= self.check_in_date:
            raise ValueError("check_out_date must be greater than check_in_date")
        return self


class BookingCreate(BookingBase):
    """Схема для создания бронирования."""

    pass


class BookingResponse(BookingBase):
    """Схема ответа с информацией о бронировании."""

    id: UUID
    user_id: UUID
    created_at: datetime
    room: RoomResponse

    class Config:
        """Конфигурация Pydantic."""

        from_attributes = True

