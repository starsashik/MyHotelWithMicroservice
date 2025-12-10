"""Зависимости FastAPI."""

import logging
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.security.jwt import decode_access_token

logger = logging.getLogger(__name__)

# Схема для Bearer токена
security = HTTPBearer()


class CurrentUser:
    """Класс для представления текущего пользователя."""

    def __init__(self, user_id: UUID):
        """
        Инициализация текущего пользователя.

        Args:
            user_id: UUID пользователя
        """
        self.id = user_id


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> CurrentUser:
    """
    Зависимость для получения текущего пользователя из JWT токена.

    Args:
        credentials: Bearer токен из заголовка Authorization

    Returns:
        CurrentUser: Объект пользователя с полем id

    Raises:
        HTTPException: Если токен невалиден
    """
    token = credentials.credentials
    user_id = decode_access_token(token)

    if user_id is None:
        logger.warning("Invalid token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return CurrentUser(user_id=user_id)

