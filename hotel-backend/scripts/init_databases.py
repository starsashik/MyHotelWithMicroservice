"""
Скрипт инициализации баз данных для системы бронирования отелей.

Создаёт три базы данных PostgreSQL и их таблицы, вставляет тестовые данные.
При повторном запуске не создаёт дубликаты данных.
"""

import asyncio
import os
import sys
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path
from uuid import UUID, uuid4

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Добавляем путь к common для импорта моделей
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.models import Base, User, Hotel, Room, Booking, LogEntry

# Загрузка переменных окружения из .env файла
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Фиксированные UUID для тестовых данных (для предотвращения дублирования)
TEST_HOTEL_1_ID = UUID("11111111-1111-1111-1111-111111111111")
TEST_HOTEL_2_ID = UUID("22222222-2222-2222-2222-222222222222")
TEST_HOTEL_3_ID = UUID("33333333-3333-3333-3333-333333333333")

TEST_ROOM_IDS = [
    UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),  # Grand Hotel 101
    UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),  # Grand Hotel 102
    UUID("cccccccc-cccc-cccc-cccc-cccccccccccc"),  # Grand Hotel 201
    UUID("dddddddd-dddd-dddd-dddd-dddddddddddd"),  # Seaside Resort 101
    UUID("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"),  # Seaside Resort 102
    UUID("ffffffff-ffff-ffff-ffff-ffffffffffff"),  # Seaside Resort 301
    UUID("00000000-0000-0000-0000-000000000001"),  # Mountain Lodge 101
    UUID("00000000-0000-0000-0000-000000000002"),  # Mountain Lodge 202
]


# Используем общие модели из common.models
# User, Hotel, Room, Booking, LogEntry уже импортированы выше


# ============================================================================
# Функции инициализации
# ============================================================================


async def init_auth_db():
    """Инициализация базы данных auth_db."""
    auth_url = os.getenv("AUTH_DATABASE_URL")
    if not auth_url:
        raise ValueError("AUTH_DATABASE_URL environment variable is not set")

    engine = create_async_engine(auth_url, echo=False)
    
    # Создаём метаданные только для модели User
    from sqlalchemy import MetaData
    user_metadata = MetaData()
    # Копируем таблицу User в новую метаданную
    User.__table__.tometadata(user_metadata, schema="public")
    
    async with engine.begin() as conn:
        await conn.run_sync(user_metadata.create_all)
    await engine.dispose()
    print("✓ auth_db initialized")


async def init_booking_db():
    """Инициализация базы данных booking_db и вставка тестовых данных."""
    booking_url = os.getenv("BOOKING_DATABASE_URL")
    if not booking_url:
        raise ValueError("BOOKING_DATABASE_URL environment variable is not set")

    engine = create_async_engine(booking_url, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Создание таблиц - используем метаданные для Hotel, Room, Booking
    from sqlalchemy import MetaData
    booking_metadata = MetaData()
    # Копируем таблицы в новую метаданную
    Hotel.__table__.tometadata(booking_metadata, schema="public")
    Room.__table__.tometadata(booking_metadata, schema="public")
    Booking.__table__.tometadata(booking_metadata, schema="public")
    
    async with engine.begin() as conn:
        await conn.run_sync(booking_metadata.create_all)

    # Вставка тестовых данных
    async with async_session() as session:
        # Проверка существования отелей
        existing_hotels = await session.execute(
            select(Hotel).where(
                Hotel.id.in_([TEST_HOTEL_1_ID, TEST_HOTEL_2_ID, TEST_HOTEL_3_ID])
            )
        )
        existing_hotel_ids = {hotel.id for hotel in existing_hotels.scalars().all()}

        # Создание отелей только если их еще нет
        hotels_to_create = []
        if TEST_HOTEL_1_ID not in existing_hotel_ids:
            hotel1 = Hotel(
                id=TEST_HOTEL_1_ID,
                name="Grand Hotel",
                location="Москва, Красная площадь, 1",
                description="Роскошный отель в самом центре Москвы с видом на Кремль.",
                img_url="https://example.com/hotel1.jpg",
            )
            hotels_to_create.append(hotel1)
        else:
            hotel1 = await session.get(Hotel, TEST_HOTEL_1_ID)

        if TEST_HOTEL_2_ID not in existing_hotel_ids:
            hotel2 = Hotel(
                id=TEST_HOTEL_2_ID,
                name="Seaside Resort",
                location="Сочи, Приморская набережная, 15",
                description="Современный курортный отель на берегу Чёрного моря.",
                img_url="https://example.com/hotel2.jpg",
            )
            hotels_to_create.append(hotel2)
        else:
            hotel2 = await session.get(Hotel, TEST_HOTEL_2_ID)

        if TEST_HOTEL_3_ID not in existing_hotel_ids:
            hotel3 = Hotel(
                id=TEST_HOTEL_3_ID,
                name="Mountain Lodge",
                location="Красная Поляна, Горная улица, 42",
                description="Уютный горный отель для любителей активного отдыха.",
                img_url=None,
            )
            hotels_to_create.append(hotel3)
        else:
            hotel3 = await session.get(Hotel, TEST_HOTEL_3_ID)

        if hotels_to_create:
            session.add_all(hotels_to_create)
            await session.flush()
            print(f"  → Created {len(hotels_to_create)} new hotel(s)")
        else:
            print("  → Hotels already exist, skipping creation")

        # Проверка существования комнат
        existing_rooms = await session.execute(
            select(Room).where(Room.id.in_(TEST_ROOM_IDS))
        )
        existing_room_ids = {room.id for room in existing_rooms.scalars().all()}

        # Создание комнат только если их еще нет
        rooms_to_create = []
        room_data = [
            (TEST_ROOM_IDS[0], hotel1.id, "101", 1, Decimal("2500.00"), "https://example.com/room101.jpg"),
            (TEST_ROOM_IDS[1], hotel1.id, "102", 2, Decimal("3500.00"), "https://example.com/room102.jpg"),
            (TEST_ROOM_IDS[2], hotel1.id, "201", 3, Decimal("5000.00"), "https://example.com/room201.jpg"),
            (TEST_ROOM_IDS[3], hotel2.id, "101", 1, Decimal("3000.00"), "https://example.com/seaside101.jpg"),
            (TEST_ROOM_IDS[4], hotel2.id, "102", 2, Decimal("4500.00"), "https://example.com/seaside102.jpg"),
            (TEST_ROOM_IDS[5], hotel2.id, "301", 3, Decimal("6500.00"), "https://example.com/seaside301.jpg"),
            (TEST_ROOM_IDS[6], hotel3.id, "101", 1, Decimal("2000.00"), None),
            (TEST_ROOM_IDS[7], hotel3.id, "202", 2, Decimal("3000.00"), "https://example.com/mountain202.jpg"),
        ]

        for room_id, hotel_id, room_number, room_type, price, img_url in room_data:
            if room_id not in existing_room_ids:
                room = Room(
                    id=room_id,
                    hotel_id=hotel_id,
                    room_number=room_number,
                    room_type=room_type,
                    price_per_night=price,
                    img_url=img_url,
                )
                rooms_to_create.append(room)

        if rooms_to_create:
            session.add_all(rooms_to_create)
            print(f"  → Created {len(rooms_to_create)} new room(s)")
        else:
            print("  → Rooms already exist, skipping creation")

        await session.commit()

    await engine.dispose()
    print("✓ booking_db initialized with test data")


async def init_logging_db():
    """Инициализация базы данных logging_db."""
    logging_url = os.getenv("LOGGING_DATABASE_URL")
    if not logging_url:
        raise ValueError("LOGGING_DATABASE_URL environment variable is not set")

    engine = create_async_engine(logging_url, echo=False)
    
    # Создаём метаданные только для модели LogEntry (без указания схемы, по умолчанию public)
    from sqlalchemy import MetaData
    logging_metadata = MetaData()
    LogEntry.__table__.tometadata(logging_metadata)
    
    async with engine.begin() as conn:
        await conn.run_sync(logging_metadata.create_all)
    await engine.dispose()
    print("✓ logging_db initialized")


async def log_initialization():
    """Создание лога о выполнении скрипта инициализации."""
    logging_url = os.getenv("LOGGING_DATABASE_URL")
    if not logging_url:
        print("⚠ Warning: LOGGING_DATABASE_URL not set, skipping log creation")
        return

    try:
        engine = create_async_engine(logging_url, echo=False)
        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            log_entry = LogEntry(
                id=uuid4(),
                level=1,  # INFO level
                message=(
                    "Database initialization script executed successfully. "
                    "All tables created and test data inserted (hotels and rooms)."
                ),
                service_name="init_databases",
            )
            session.add(log_entry)
            await session.commit()

        await engine.dispose()
        print("✓ Initialization log created in logging_db")
    except Exception as e:
        print(f"⚠ Warning: Failed to create log entry: {e}")


async def init_databases():
    """Основная функция инициализации всех баз данных."""
    print("Starting database initialization...")
    print("-" * 50)

    try:
        await init_auth_db()
        await init_booking_db()
        await init_logging_db()

        print("-" * 50)
        print("✓ All databases initialized successfully!")
        
        # Создание лога о выполнении скрипта
        await log_initialization()
    except Exception as e:
        print(f"✗ Error during initialization: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(init_databases())

