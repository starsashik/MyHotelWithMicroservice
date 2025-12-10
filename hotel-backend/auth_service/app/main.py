"""FastAPI приложение для auth-service."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_auth import router as auth_router
from app.api.routes_user import router as user_router
from app.core.config import settings
from app.db.session import engine
from common.messaging.rabbit_handler import RabbitMQHandler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Подключаем отправку логов в RabbitMQ
try:
    handler = RabbitMQHandler(
        url=settings.RABBITMQ_URL,
        queue_name=settings.RABBITMQ_QUEUE,
        service_name="auth_service",
    )
    logging.getLogger().addHandler(handler)
except Exception as e:
    logger.warning(f"Failed to attach RabbitMQ logging handler: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.
    
    Args:
        app: Экземпляр FastAPI приложения
    """
    # Startup
    logger.info("Starting Auth Service...")
    logger.info(f"Database URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Auth Service...")
    await engine.dispose()
    logger.info("Database connections closed")


# Создание FastAPI приложения
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Микросервис для аутентификации и авторизации в системе бронирования отелей",
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
app.include_router(auth_router)
app.include_router(user_router)


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
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )

