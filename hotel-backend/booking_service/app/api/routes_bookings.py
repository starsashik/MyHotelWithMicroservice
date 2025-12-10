"""API маршруты для бронирований."""

import logging
from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.dependencies import CurrentUser, get_current_user
from common.models import Booking, Room
from app.schemas.booking import BookingCreate, BookingResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


async def check_room_availability(
    room_id: UUID,
    check_in: date,
    check_out: date,
    db: AsyncSession,
    exclude_booking_id: UUID | None = None,
) -> bool:
    """
    Проверяет доступность комнаты на указанные даты.

    Args:
        room_id: UUID комнаты
        check_in: Дата заезда
        check_out: Дата выезда
        db: Сессия базы данных
        exclude_booking_id: UUID бронирования для исключения из проверки (при обновлении)

    Returns:
        bool: True если комната доступна, False если занята
    """
    # Поиск пересекающихся бронирований
    query = select(Booking).where(
        Booking.room_id == room_id,
        Booking.check_in_date < check_out,
        Booking.check_out_date > check_in,
    )

    if exclude_booking_id:
        query = query.where(Booking.id != exclude_booking_id)

    result = await db.execute(query)
    conflicting_bookings = result.scalars().all()

    return len(conflicting_bookings) == 0


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать бронирование",
    description="Создает новое бронирование для авторизованного пользователя",
)
async def create_booking(
    booking_data: BookingCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> BookingResponse:
    """
    Создать новое бронирование.

    Args:
        booking_data: Данные для создания бронирования
        db: Сессия базы данных
        current_user: Текущий пользователь

    Returns:
        BookingResponse: Информация о созданном бронировании

    Raises:
        HTTPException: Если комната не найдена или недоступна на указанные даты
    """
    # Проверка существования комнаты
    result = await db.execute(select(Room).where(Room.id == booking_data.room_id))
    room = result.scalar_one_or_none()

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    # Проверка доступности комнаты
    is_available = await check_room_availability(
        booking_data.room_id,
        booking_data.check_in_date,
        booking_data.check_out_date,
        db,
    )

    if not is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is not available for the selected dates",
        )

    new_booking = Booking(
        user_id=current_user.id,
        room_id=booking_data.room_id,
        check_in_date=booking_data.check_in_date,
        check_out_date=booking_data.check_out_date,
    )

    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)

    # Загружаем связанную комнату для ответа
    result = await db.execute(
        select(Booking)
        .where(Booking.id == new_booking.id)
        .options(selectinload(Booking.room))
    )
    booking_with_room = result.scalar_one()

    logger.info(
        f"Booking created: {new_booking.id} for room {booking_data.room_id} "
        f"by user {current_user.id}"
    )
    return BookingResponse.model_validate(booking_with_room)


@router.get(
    "/my",
    response_model=list[BookingResponse],
    summary="Мои бронирования",
    description="Возвращает список бронирований текущего пользователя",
)
async def get_my_bookings(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> list[BookingResponse]:
    """
    Получить список бронирований текущего пользователя.

    Args:
        db: Сессия базы данных
        current_user: Текущий пользователь

    Returns:
        list[BookingResponse]: Список бронирований
    """
    result = await db.execute(
        select(Booking)
        .where(Booking.user_id == current_user.id)
        .options(selectinload(Booking.room))
        .order_by(Booking.created_at.desc())
    )
    bookings = result.scalars().all()

    return [BookingResponse.model_validate(booking) for booking in bookings]


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить бронирование",
    description="Удаляет бронирование по ID",
)
async def delete_booking(
    booking_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> None:
    """
    Удалить бронирование по ID.

    Args:
        booking_id: UUID бронирования
        db: Сессия базы данных
        current_user: Текущий пользователь

    Raises:
        HTTPException: Если бронирование не найдено или не принадлежит пользователю
    """
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id)
    )
    booking = result.scalar_one_or_none()

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    # Проверка принадлежности бронирования пользователю
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this booking",
        )

    await db.delete(booking)
    await db.commit()

    logger.info(
        f"Booking deleted: {booking_id} by user {current_user.id}"
    )

