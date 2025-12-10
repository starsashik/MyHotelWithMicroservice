"""RabbitMQ consumer для обработки логов."""

import json
import logging
from datetime import datetime

from aio_pika import IncomingMessage, connect_robust
from aio_pika.abc import AbstractConnection, AbstractChannel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from common.models import LogEntry
from app.schemas.log import LogEntryCreate

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    """Класс для работы с RabbitMQ consumer."""

    def __init__(self):
        """Инициализация consumer."""
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.is_running = False

    async def connect(self):
        """Подключение к RabbitMQ."""
        try:
            logger.info(f"Connecting to RabbitMQ: {settings.RABBITMQ_URL.split('@')[1] if '@' in settings.RABBITMQ_URL else 'configured'}")
            self.connection = await connect_robust(settings.RABBITMQ_URL)
            self.channel = await self.connection.channel()
            
            # Объявляем очередь
            queue = await self.channel.declare_queue(settings.RABBITMQ_QUEUE, durable=True)
            logger.info(f"Queue '{settings.RABBITMQ_QUEUE}' declared")
            
            # Настраиваем обработчик сообщений
            await queue.consume(self.process_message)
            logger.info("RabbitMQ consumer started")
            self.is_running = True
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def process_message(self, message: IncomingMessage):
        """
        Обработка входящего сообщения из RabbitMQ.
        
        Args:
            message: Входящее сообщение из очереди
        """
        async with message.process():
            try:
                # Парсим JSON сообщение
                body = json.loads(message.body.decode())
                logger.debug(f"Received message: {body}")
                
                # Валидируем данные через Pydantic
                log_data = LogEntryCreate(**body)
                
                # Сохраняем в базу данных
                await self.save_log_to_db(log_data)
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON message: {e}")
            except Exception as e:
                logger.error(f"Failed to process message: {e}")

    async def save_log_to_db(self, log_data: LogEntryCreate):
        """
        Сохранение лога в базу данных.
        
        Args:
            log_data: Данные лога для сохранения
        """
        async with AsyncSessionLocal() as session:
            try:
                # Подготавливаем данные для создания записи
                log_kwargs = {
                    "level": log_data.level,
                    "message": log_data.message,
                    "service_name": log_data.service_name,
                }
                
                # Парсим timestamp если он указан
                if log_data.timestamp:
                    # Обрабатываем различные форматы ISO timestamp
                    timestamp_str = log_data.timestamp.replace('Z', '+00:00')
                    log_kwargs["created_at"] = datetime.fromisoformat(timestamp_str)
                # Если timestamp не указан, БД установит created_at автоматически через server_default
                
                # Создаем запись в БД
                log_entry = LogEntry(**log_kwargs)
                
                session.add(log_entry)
                await session.commit()
                logger.debug(f"Log saved: {log_entry.id}")
                
            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to save log to database: {e}")
                raise

    async def disconnect(self):
        """Отключение от RabbitMQ."""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            logger.info("RabbitMQ connection closed")
        self.is_running = False


# Глобальный экземпляр consumer
consumer = RabbitMQConsumer()

