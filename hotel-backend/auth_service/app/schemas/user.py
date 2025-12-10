"""Pydantic схемы для пользователя."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Базовая схема пользователя."""

    name: str = Field(..., min_length=1, max_length=255, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email пользователя")


class UserCreate(UserBase):
    """Схема для создания пользователя."""

    password: str = Field(..., min_length=6, max_length=100, description="Пароль")


class UserResponse(UserBase):
    """Схема ответа с информацией о пользователе."""

    id: UUID
    created_at: datetime

    class Config:
        """Конфигурация Pydantic."""

        from_attributes = True


class UserLogin(BaseModel):
    """Схема для входа пользователя."""

    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=6, max_length=100, description="Пароль")


class TokenResponse(BaseModel):
    """Схема ответа с токеном."""

    access_token: str = Field(..., description="JWT токен доступа")
    token_type: str = Field(default="bearer", description="Тип токена")


class UserUpdateName(BaseModel):
    """Схема для обновления имени пользователя."""

    name: str = Field(..., min_length=1, max_length=255, description="Новое имя")
    id: UUID | None = Field(
        default=None,
        description="Идентификатор пользователя (обязателен, если не указан email)",
    )
