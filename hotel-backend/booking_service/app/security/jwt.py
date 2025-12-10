"""Функции для верификации JWT токенов."""

from uuid import UUID

from jose import JWTError, jwt

from app.core.config import settings


def decode_access_token(token: str) -> UUID | None:
    """
    Декодирует и валидирует JWT токен.

    Args:
        token: JWT токен

    Returns:
        UUID | None: UUID пользователя из токена или None если токен невалиден
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return UUID(user_id)
    except (JWTError, ValueError):
        return None

