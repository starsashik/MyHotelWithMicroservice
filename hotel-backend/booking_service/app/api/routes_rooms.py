"""API маршруты для комнат."""

import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import CurrentUser, get_current_user
from common.models import Hotel, Room
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Rooms"])

@router.get(
    "/hotels/{hotel_id}/rooms",
    response_model=list[RoomResponse],
    summary="Список комнат отеля",
    description="Возвращает список всех комнат для указанного отеля",
)
async def get_hotel_rooms(
    hotel_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[RoomResponse]:
    """
    Получить список комнат отеля.

    Args:
        hotel_id: UUID отеля
        db: Сессия базы данных

    Returns:
        list[RoomResponse]: Список комнат

    Raises:
        HTTPException: Если отель не найден
    """
    # Проверка существования отеля
    result = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
    hotel = result.scalar_one_or_none()

    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel not found",
        )

    result = await db.execute(
        select(Room).where(Room.hotel_id == hotel_id).order_by(Room.room_number)
    )
    rooms = result.scalars().all()
    return [RoomResponse.model_validate(room) for room in rooms]


@router.post(
    "/hotels/{hotel_id}/rooms",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать комнату",
    description="Создает новую комнату для отеля (требуется авторизация)",
)
async def create_hotel_room(
    hotel_id: UUID,
    room_data: RoomCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> RoomResponse:
    """
    Создать новую комнату для отеля.

    Args:
        hotel_id: UUID отеля
        room_data: Данные для создания комнаты
        db: Сессия базы данных
        current_user: Текущий пользователь

    Returns:
        RoomResponse: Информация о созданной комнате

    Raises:
        HTTPException: Если отель не найден
    """
    # Проверка существования отеля
    result = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
    hotel = result.scalar_one_or_none()

    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel not found",
        )

    new_room = Room(
        hotel_id=hotel_id,
        room_number=room_data.room_number,
        room_type=room_data.room_type,
        price_per_night=room_data.price_per_night,
        img_url=room_data.img_url,
    )

    db.add(new_room)
    await db.commit()
    await db.refresh(new_room)

    logger.info(f"Room created: {new_room.id} for hotel {hotel_id} by user {current_user.id}")
    return RoomResponse.model_validate(new_room)


@router.get(
    "/rooms/{room_id}",
    response_model=RoomResponse,
    summary="Получить комнату",
    description="Возвращает информацию о комнате по ID",
)
async def get_room(
    room_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RoomResponse:
    """
    Получить комнату по ID.

    Args:
        room_id: UUID комнаты
        db: Сессия базы данных

    Returns:
        RoomResponse: Информация о комнате

    Raises:
        HTTPException: Если комната не найдена
    """
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    return RoomResponse.model_validate(room)


@router.put(
    "/rooms/{room_id}",
    response_model=RoomResponse,
    summary="Обновить комнату",
    description="Обновляет информацию о комнате (требуется авторизация)",
)
async def update_room(
    room_id: UUID,
    room_data: RoomUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> RoomResponse:
    """
    Обновить комнату.

    Args:
        room_id: UUID комнаты
        room_data: Данные для обновления комнаты
        db: Сессия базы данных
        current_user: Текущий пользователь

    Returns:
        RoomResponse: Обновленная информация о комнате

    Raises:
        HTTPException: Если комната не найдена
    """
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    # Обновление полей
    update_data = room_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(room, field, value)

    await db.commit()
    await db.refresh(room)

    logger.info(f"Room updated: {room_id} by user {current_user.id}")
    return RoomResponse.model_validate(room)


@router.delete(
    "/rooms/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить комнату",
    description="Удаляет комнату (требуется авторизация)",
)
async def delete_room(
    room_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> None:
    """
    Удалить комнату.

    Args:
        room_id: UUID комнаты
        db: Сессия базы данных
        current_user: Текущий пользователь

    Raises:
        HTTPException: Если комната не найдена
    """
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    await db.delete(room)
    await db.commit()

    logger.info(f"Room deleted: {room_id} by user {current_user.id}")

