"""Функции для хэширования и проверки паролей."""

from passlib.context import CryptContext

# Контекст для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хэширует пароль.

    Args:
        password: Пароль в открытом виде

    Returns:
        str: Хэшированный пароль
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет пароль.

    Args:
        plain_password: Пароль в открытом виде
        hashed_password: Хэшированный пароль

    Returns:
        bool: True если пароль совпадает, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)

