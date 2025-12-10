"""API роуты для работы с логами."""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func as sql_func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from common.models import LogEntry
from app.schemas.log import LogEntryListResponse, LogEntryResponse

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("", response_model=LogEntryListResponse)
async def get_logs(
    level: Optional[int] = Query(None, ge=0, le=3, description="Фильтр по уровню лога"),
    service_name: Optional[str] = Query(None, description="Фильтр по имени сервиса"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
    db: AsyncSession = Depends(get_db),
):
    """
    Получить список логов с возможной фильтрацией.
    
    Args:
        level: Опциональный фильтр по уровню лога (0-3)
        service_name: Опциональный фильтр по имени сервиса
        limit: Максимальное количество записей (по умолчанию 100)
        db: Сессия базы данных
        
    Returns:
        LogEntryListResponse: Список логов и общее количество
    """
    # Строим базовый запрос
    query = select(LogEntry)
    count_query = select(sql_func.count()).select_from(LogEntry)
    
    # Применяем фильтры
    conditions = []
    if level is not None:
        conditions.append(LogEntry.level == level)
    if service_name is not None:
        conditions.append(LogEntry.service_name == service_name)
    
    if conditions:
        for condition in conditions:
            query = query.where(condition)
            count_query = count_query.where(condition)
    
    # Сортировка по дате создания (новые первыми)
    query = query.order_by(LogEntry.created_at.desc())
    
    # Применяем лимит
    query = query.limit(limit)
    
    # Выполняем запросы
    result = await db.execute(query)
    logs = result.scalars().all()
    
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()
    
    return LogEntryListResponse(
        logs=[LogEntryResponse.model_validate(log) for log in logs],
        total=total,
    )

