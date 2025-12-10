"""Logging handler that forwards log records to RabbitMQ."""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Optional

from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractChannel, AbstractConnection


class RabbitMQHandler(logging.Handler):
    """Logging handler publishing records to RabbitMQ."""

    def __init__(self, url: str, queue_name: str, service_name: str):
        super().__init__()
        self.url = url
        self.queue_name = queue_name
        self.service_name = service_name
        self._connection: Optional[AbstractConnection] = None
        self._channel: Optional[AbstractChannel] = None
        self._lock = asyncio.Lock()

    async def _ensure_channel(self):
        if self._connection and not self._connection.is_closed:
            return
        self._connection = await connect_robust(self.url)
        self._channel = await self._connection.channel()
        await self._channel.declare_queue(self.queue_name, durable=True)

    async def _publish(self, record: logging.LogRecord):
        try:
            async with self._lock:
                await self._ensure_channel()
            # Map standard logging levels to 0-3 range expected by logging_service
            level_map = [
                (logging.ERROR, 3),
                (logging.WARNING, 2),
                (logging.INFO, 1),
                (logging.DEBUG, 0),
            ]
            mapped_level = 3
            for threshold, val in level_map:
                if record.levelno >= threshold:
                    mapped_level = val
                    break

            payload = {
                "level": mapped_level,
                "message": record.getMessage(),
                "service_name": self.service_name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            body = json.dumps(payload).encode()
            await self._channel.default_exchange.publish(
                Message(body=body, delivery_mode=2),
                routing_key=self.queue_name,
            )
        except Exception:
            # Do not propagate exceptions to the logging system
            self.handleError(record)

    def emit(self, record: logging.LogRecord) -> None:
        # Шумные системные логгеры — не отправляем в очередь
        if record.name.startswith(("aio_pika", "aiormq")):
            return
        msg = record.getMessage()
        if "bcrypt version" in msg:
            return

        loop = asyncio.get_event_loop()
        if loop.is_closed():
            return
        loop.create_task(self._publish(record))

