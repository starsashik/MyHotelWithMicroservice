"""API маршруты для управления пользователями."""

import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes_auth import get_current_user
from app.db.session import get_db
from app.schemas.user import UserResponse, UserUpdateName
from common.models import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=list[UserResponse],
    summary="Получить список пользователей",
    description="Возвращает список всех пользователей. Требует авторизации.",
)
async def list_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> list[UserResponse]:
    """Получение всех пользователей."""
    result = await db.execute(select(User))
    users = result.scalars().all()
    logger.info("Requested users list: %s users found", len(users))
    return [UserResponse.model_validate(user) for user in users]


@router.patch(
    "",
    response_model=UserResponse,
    summary="Обновить данные пользователя",
    description="Обновляет имя пользователя по id или email. Требует авторизации.",
)
async def update_user(
    payload: UserUpdateName,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Обновление имени пользователя по id или email."""
    if not payload.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User id or email is required",
        )

    query = (
        select(User).where(User.id == payload.id)
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.name = payload.name
    db.add(user)
    await db.commit()
    await db.refresh(user)

    logger.info("User updated: %s", user.id)
    return UserResponse.model_validate(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя",
    description="Удаляет пользователя по id. Требует авторизации.",
)
async def delete_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> Response:
    """Удаление пользователя по идентификатору."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()

    logger.info("User deleted: %s", user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

