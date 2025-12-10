"""API маршруты для отелей."""

import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import CurrentUser, get_current_user
from common.models import Hotel
from app.schemas.hotel import HotelCreate, HotelResponse, HotelUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get(
    "/",
    response_model=list[HotelResponse],
    summary="Список отелей",
    description="Возвращает список всех отелей",
)
async def get_hotels(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[HotelResponse]:
    """
    Получить список всех отелей.

    Args:
        db: Сессия базы данных

    Returns:
        list[HotelResponse]: Список отелей
    """
    result = await db.execute(select(Hotel).order_by(Hotel.created_at.desc()))
    hotels = result.scalars().all()
    return [HotelResponse.model_validate(hotel) for hotel in hotels]


# @router.get(
#     "/{hotel_id}",
#     response_model=HotelResponse,
#     summary="Получить отель",
#     description="Возвращает информацию об отеле по ID",
# )
# 
# async def get_hotel(
#     hotel_id: UUID,
#     db: Annotated[AsyncSession, Depends(get_db)],
# ) -> HotelResponse:
#     """
#     Получить отель по ID.

#     Args:
#         hotel_id: UUID отеля
#         db: Сессия базы данных

#     Returns:
#         HotelResponse: Информация об отеле

#     Raises:
#         HTTPException: Если отель не найден
#     """
#     result = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
#     hotel = result.scalar_one_or_none()

#     if hotel is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Hotel not found",
#         )

#     return HotelResponse.model_validate(hotel)


@router.post(
    "/",
    response_model=HotelResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать отель",
    description="Создает новый отель (требуется авторизация)",
)
async def create_hotel(
    hotel_data: HotelCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> HotelResponse:
    """
    Создать новый отель.

    Args:
        hotel_data: Данные для создания отеля
        db: Сессия базы данных
        current_user: Текущий пользователь

    Returns:
        HotelResponse: Информация о созданном отеле
    """
    new_hotel = Hotel(
        name=hotel_data.name,
        location=hotel_data.location,
        description=hotel_data.description,
        img_url=hotel_data.img_url,
    )

    db.add(new_hotel)
    await db.commit()
    await db.refresh(new_hotel)

    logger.info(f"Hotel created: {new_hotel.id} by user {current_user.id}")
    return HotelResponse.model_validate(new_hotel)


@router.put(
    "/{hotel_id}",
    response_model=HotelResponse,
    summary="Обновить отель",
    description="Обновляет информацию об отеле (требуется авторизация)",
)
async def update_hotel(
    hotel_id: UUID,
    hotel_data: HotelUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> HotelResponse:
    """
    Обновить отель.

    Args:
        hotel_id: UUID отеля
        hotel_data: Данные для обновления отеля
        db: Сессия базы данных
        current_user: Текущий пользователь

    Returns:
        HotelResponse: Обновленная информация об отеле

    Raises:
        HTTPException: Если отель не найден
    """
    result = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
    hotel = result.scalar_one_or_none()

    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel not found",
        )

    # Обновление полей
    update_data = hotel_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(hotel, field, value)

    await db.commit()
    await db.refresh(hotel)

    logger.info(f"Hotel updated: {hotel_id} by user {current_user.id}")
    return HotelResponse.model_validate(hotel)


@router.delete(
    "/{hotel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить отель",
    description="Удаляет отель (требуется авторизация)",
)
async def delete_hotel(
    hotel_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> None:
    """
    Удалить отель.

    Args:
        hotel_id: UUID отеля
        db: Сессия базы данных
        current_user: Текущий пользователь

    Raises:
        HTTPException: Если отель не найден
    """
    result = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
    hotel = result.scalar_one_or_none()

    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel not found",
        )

    await db.delete(hotel)
    await db.commit()

    logger.info(f"Hotel deleted: {hotel_id} by user {current_user.id}")

