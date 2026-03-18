

# Habit Tracker

**SPA-бэкенд для трекера полезных привычек**
*(Django REST Framework + JWT + Celery + Telegram)*

---

## Быстрый старт (Docker)

### 1. Настройка `.env`
Скопируй `env.example` в `.env` и измени следующие переменные:
```bash
cp env.example .env
```
**Важно для Docker:**
- `POSTGRES_HOST=db`
- `CELERY_BROKER_URL=redis://redis:6379/0`
- `CELERY_RESULT_BACKEND=redis://redis:6379/0`

### 2. Запуск проекта
```bash
docker compose up --build
```
После запуска API будет доступен по адресу: **[http://localhost/](http://localhost/)** (через nginx).

---

## Локальный запуск (Windows/PowerShell)

### 1. Установка зависимостей
```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

### 2. Настройка `.env`
Скопируй `env.example` в `.env` и заполни:
- `DJANGO_SECRET_KEY` (32+ символа)
- `CORS_ALLOWED_ORIGINS` (например: `http://localhost:3000,http://localhost:8080`)
- `TELEGRAM_BOT_TOKEN` (токен от [@BotFather](https://t.me/BotFather))
- `CELERY_BROKER_URL` (по умолчанию: `redis://localhost:6379/0`)

### 3. Миграции
```bash
.\.venv\Scripts\python manage.py migrate
```

### 4. Запуск API
**Вариант 1 (PowerShell):**
```powershell
.\run_server.ps1
```
**Вариант 2 (CMD):**
```cmd
run_server.bat
```
**Вариант 3 (вручную):**
```bash
.\.venv\Scripts\python manage.py runserver
```
API будет доступен на **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**.

---

## Документация
- **Swagger UI:** `/api/docs/`
- **OpenAPI schema:** `/api/schema/`

---

## Celery + Telegram напоминания
Задачи запускаются раз в минуту через **Celery Beat**.

### Запуск Celery (Windows)
**1. Worker:**
```bash
.\run_celery_worker.bat
```
или вручную:
```bash
celery -A config worker -l info --pool=solo
```

**2. Beat (в отдельном терминале):**
```bash
.\run_celery_beat.bat
```
или вручную:
```bash
celery -A config beat -l info
```

### Тестирование Telegram
Проверь отправку сообщений командой:
```bash
.\.venv\Scripts\python manage.py test_telegram <chat_id> "Тестовое сообщение"
```
**Как получить `chat_id`:**
1. Найди бота в Telegram: `https://t.me/<ваш_бот>`
2. Начни диалог и отправь сообщение.
3. Используй API: `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Найди `chat.id` в ответе.

---

## Основные эндпоинты
| Эндпоинт                     | Описание                          |
|------------------------------|-----------------------------------|
| `POST /api/auth/register/`   | Регистрация                       |
| `POST /api/auth/token/`      | Авторизация (JWT)                 |
| `POST /api/auth/token/refresh/` | Обновление токена             |
| `PATCH /api/users/me/telegram/` | Привязать Telegram `chat_id` |
| `CRUD /api/habits/`          | Управление привычками (только свои) |
| `GET /api/habits/public/`    | Публичные привычки               |

---

## Тесты и качество кода
- **Запуск тестов с покрытием:**
  ```bash
  .\.venv\Scripts\pytest --cov=. --cov-report=term-missing
  ```
- **Проверка flake8:**
  ```bash
  .\.venv\Scripts\python -m flake8 .
  ```
- **Требования:** покрытие ≥80%, flake8 100% (миграции исключены).

---

## Админка
Создай суперпользователя:
```bash
.\.venv\Scripts\python manage.py createsuperuser
```
Админка доступна по адресу: **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**.

---

## CI/CD и деплой (GitHub Actions + Docker Compose)
### Настройка сервера (Yandex Cloud VM)
1. Установи Docker:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-compose-plugin
   sudo usermod -aG docker $USER
   newgrp docker
   ```
2. Подготовь директорию:
   ```bash
   mkdir -p ~/apps/<твой_проект>
   cd ~/apps/<твой_проект>
   ```
3. Создай `.env` на сервере (скопируй `env.prod.example`).

### GitHub Secrets
Добавь в репозиторий (Settings → Secrets):
- `SSH_HOST`, `SSH_PORT`, `SSH_USER`, `SSH_KEY` (PEM), `DEPLOY_PATH`.

### Как работает деплой
- **CI:** запускается на PR/пуш в `develop` (flake8 + pytest + docker build).
- **Deploy:** собирает образ, пушит в **GHCR**, обновляет контейнеры на сервере.
