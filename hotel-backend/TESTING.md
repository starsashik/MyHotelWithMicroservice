# Руководство по тестированию микросервисов

## Предварительные требования

1. **PostgreSQL** - должна быть запущена с тремя базами данных:
   - `auth_db`
   - `booking_db`
   - `logging_db`

2. **RabbitMQ** - требуется для `logging-service`:
   ```bash
   # Docker
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```

3. **Python 3.11+** с установленными зависимостями

## 1. Инициализация баз данных

Перед запуском сервисов необходимо инициализировать базы данных:

```bash
cd hotel-backend
python scripts/init_databases.py
```

Это создаст таблицы и вставит тестовые данные (отели и комнаты).

## 2. Установка зависимостей

### Auth Service
```bash
cd hotel-backend/auth_service
pip install -r requirements.txt
# или если нет requirements.txt:
pip install fastapi uvicorn sqlalchemy asyncpg pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] python-dotenv
```

### Booking Service
```bash
cd hotel-backend/booking_service
pip install fastapi uvicorn sqlalchemy asyncpg pydantic pydantic-settings python-jose[cryptography] python-dotenv
```

### Logging Service
```bash
cd hotel-backend/logging_service
pip install fastapi uvicorn sqlalchemy asyncpg pydantic pydantic-settings aio-pika python-dotenv
```

## 3. Запуск сервисов

Откройте **три отдельных терминала** для каждого сервиса:

### Terminal 1: Auth Service (порт 8000)
```bash
cd hotel-backend/auth_service
PYTHONDONTWRITEBYTECODE=1 python -m app.main
# или
PYTHONDONTWRITEBYTECODE=1 uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2: Booking Service (порт 8001)
```bash
cd hotel-backend/booking_service
PYTHONDONTWRITEBYTECODE=1 python -m app.main
# или
PYTHONDONTWRITEBYTECODE=1 uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Terminal 3: Logging Service (порт 8002)
```bash
cd hotel-backend/logging_service
PYTHONDONTWRITEBYTECODE=1 python -m app.main
# или
PYTHONDONTWRITEBYTECODE=1 uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

## 4. Проверка работоспособности

### 4.1. Auth Service (http://localhost:8000)

#### Health Check
```bash
curl http://localhost:8000/health
# Ожидаемый ответ: {"status":"healthy"}

curl http://localhost:8000/
# Ожидаемый ответ: {"service":"Auth Service","version":"1.0.0","status":"running"}
```

#### Регистрация пользователя
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### Вход пользователя
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
# Сохраните access_token из ответа
```

#### Получение информации о текущем пользователе
```bash
TOKEN="your_access_token_here"
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

#### Документация API
Откройте в браузере: http://localhost:8000/docs

---

### 4.2. Booking Service (http://localhost:8001)

#### Health Check
```bash
curl http://localhost:8001/health
# Ожидаемый ответ: {"status":"healthy"}

curl http://localhost:8001/
# Ожидаемый ответ: {"service":"Booking Service","version":"1.0.0","status":"running"}
```

#### Получение списка отелей
```bash
curl http://localhost:8001/hotels
```

#### Получение информации об отеле
```bash
curl http://localhost:8001/hotels/{hotel_id}
# Например: curl http://localhost:8001/hotels/11111111-1111-1111-1111-111111111111
```

#### Получение комнат отеля
```bash
curl http://localhost:8001/hotels/{hotel_id}/rooms
```

#### Создание бронирования (требует JWT токен)
```bash
TOKEN="your_access_token_here"
curl -X POST http://localhost:8001/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "room_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    "check_in_date": "2024-12-25",
    "check_out_date": "2024-12-30"
  }'
```

#### Получение списка бронирований
```bash
TOKEN="your_access_token_here"
curl http://localhost:8001/bookings \
  -H "Authorization: Bearer $TOKEN"
```

#### Документация API
Откройте в браузере: http://localhost:8001/docs

---

### 4.3. Logging Service (http://localhost:8002)

#### Health Check
```bash
curl http://localhost:8002/health
# Ожидаемый ответ: {"status":"healthy","rabbitmq_connected":true}

curl http://localhost:8002/
# Ожидаемый ответ: {"service":"Logging Service","version":"1.0.0","status":"running"}
```

#### Получение логов
```bash
curl http://localhost:8002/logs
```

#### Фильтрация логов по уровню
```bash
curl http://localhost:8002/logs?level=1
# level: 0=DEBUG, 1=INFO, 2=WARNING, 3=ERROR
```

#### Фильтрация логов по сервису
```bash
curl http://localhost:8002/logs?service_name=booking_service
```

#### Ограничение количества логов
```bash
curl http://localhost:8002/logs?limit=10
```

#### Документация API
Откройте в браузере: http://localhost:8002/docs

---

## 5. Автоматизированное тестирование

Создайте простой скрипт для проверки всех сервисов:

### test_services.sh (для Linux/Mac)
```bash
#!/bin/bash

echo "Testing Auth Service..."
curl -s http://localhost:8000/health | grep -q "healthy" && echo "✓ Auth Service OK" || echo "✗ Auth Service FAILED"

echo "Testing Booking Service..."
curl -s http://localhost:8001/health | grep -q "healthy" && echo "✓ Booking Service OK" || echo "✗ Booking Service FAILED"

echo "Testing Logging Service..."
curl -s http://localhost:8002/health | grep -q "healthy" && echo "✓ Logging Service OK" || echo "✗ Logging Service FAILED"
```

### test_services.ps1 (для Windows PowerShell)
```powershell
Write-Host "Testing Auth Service..."
$response = Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing
if ($response.Content -match "healthy") { Write-Host "✓ Auth Service OK" } else { Write-Host "✗ Auth Service FAILED" }

Write-Host "Testing Booking Service..."
$response = Invoke-WebRequest -Uri http://localhost:8001/health -UseBasicParsing
if ($response.Content -match "healthy") { Write-Host "✓ Booking Service OK" } else { Write-Host "✗ Booking Service FAILED" }

Write-Host "Testing Logging Service..."
$response = Invoke-WebRequest -Uri http://localhost:8002/health -UseBasicParsing
if ($response.Content -match "healthy") { Write-Host "✓ Logging Service OK" } else { Write-Host "✗ Logging Service FAILED" }
```

## 6. Проверка интеграций

### Проверка RabbitMQ для Logging Service

1. Убедитесь, что RabbitMQ запущен:
```bash
docker ps | grep rabbitmq
```

2. Проверьте очереди в RabbitMQ Management UI:
   - Откройте http://localhost:15672 (guest/guest)
   - Проверьте наличие очереди `logs_queue`

### Проверка баз данных

Подключитесь к PostgreSQL и проверьте таблицы:

```sql
-- Проверка auth_db
\c auth_db
SELECT COUNT(*) FROM users;

-- Проверка booking_db
\c booking_db
SELECT COUNT(*) FROM hotels;
SELECT COUNT(*) FROM rooms;

-- Проверка logging_db
\c logging_db
SELECT COUNT(*) FROM logs;
```

## 7. Устранение неполадок

### Сервис не запускается

1. **Проверьте переменные окружения:**
   ```bash
   # Создайте .env файл в корне hotel-backend
   AUTH_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/auth_db
   BOOKING_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/booking_db
   LOGGING_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/logging_db
   RABBITMQ_URL=amqp://guest:guest@localhost:5672/
   JWT_SECRET=your-secret-key-change-in-production
   ```

2. **Проверьте подключение к БД:**
   ```bash
   psql -U postgres -d auth_db -c "SELECT 1;"
   ```

3. **Проверьте логи сервиса** в консоли при запуске

### Logging Service не подключается к RabbitMQ

1. Проверьте, что RabbitMQ запущен:
   ```bash
   docker ps | grep rabbitmq
   ```

2. Проверьте URL подключения в конфигурации

3. Проверьте логи сервиса на наличие ошибок подключения

### Ошибки импорта моделей

Убедитесь, что путь к `common` доступен:
```bash
cd hotel-backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# или добавьте в Python код:
# sys.path.insert(0, str(Path(__file__).parent.parent))
```

## 8. Использование httpie (альтернатива curl)

Если установлен `httpie`, можно использовать более удобный синтаксис:

```bash
# Установка
pip install httpie

# Примеры использования
http GET localhost:8000/health
http POST localhost:8000/auth/register name="Test" email="test@example.com" password="password123"
http GET localhost:8001/hotels
http GET localhost:8002/logs
```

## Примечания

- Все сервисы должны быть запущены одновременно для полной функциональности
- Booking Service использует JWT токены от Auth Service
- Logging Service получает логи через RabbitMQ (асинхронно)
- Все сервисы автоматически создают таблицы при первом запуске (в продакшене используйте миграции)

