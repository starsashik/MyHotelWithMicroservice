"""FastAPI приложение для logging-service."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_logs import router as logs_router
from app.core.config import settings
from app.db.session import engine
from app.worker.consumer import consumer

# Настройка логирования
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.
    
    Args:
        app: Экземпляр FastAPI приложения
    """
    # Startup
    logger.info("Starting Logging Service...")
    logger.info(f"Database URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    
    # Подключение к RabbitMQ и запуск consumer
    try:
        await consumer.connect()
        logger.info("RabbitMQ consumer connected and running")
    except Exception as e:
        logger.error(f"Failed to start RabbitMQ consumer: {e}")
        # В зависимости от требований можно либо остановить приложение, либо продолжить работу
    
    yield
    
    # Shutdown
    logger.info("Shutting down Logging Service...")
    
    # Отключаемся от RabbitMQ
    await consumer.disconnect()
    
    # Закрываем соединения с БД
    await engine.dispose()
    logger.info("Database connections closed")


# Создание FastAPI приложения
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Микросервис для логирования сообщений из RabbitMQ и предоставления HTTP API для запроса логов",
    lifespan=lifespan,
)

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(logs_router)


@app.get("/", tags=["Health"])
async def root():
    """
    Корневой эндпоинт для проверки работоспособности.

    Returns:
        dict: Информация о сервисе
    """
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Эндпоинт для проверки здоровья сервиса.

    Returns:
        dict: Статус здоровья сервиса
    """
    return {
        "status": "healthy",
        "rabbitmq_connected": consumer.is_running,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8002,
        reload=settings.DEBUG,
    )

