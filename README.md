# Allures\&Allol Marketplace Backend

Allures\&Allol — модульная система backend для маркетплейса, построенная на FastAPI с архитектурой микросервисов. Используется PostgreSQL (Supabase), Docker и современный Python-стек.

---

## 📁 Структура проекта

```
├── services/
│   ├── product_service/        # Управление товарами и категориями
│   ├── sales_service/          # Продажи и аналитика
│   ├── review_service/         # Отзывы и рекомендации (AI, NLP)
│   ├── auth_service/           # Регистрация, авторизация, токены
│   ├── profile_service/        # Профили пользователей и компаний
│   ├── payment_service/        # Платежи и Webhook NowPayments
│   ├── discount_service/       # Скидки, промокоды, валидаторы
│   ├── subscription_service/   # Подписки: free / plus / premium
│   ├── dashboard_service/      # Кабинет пользователя и аналитика
│   └── admin_service/          # Администрирование
├── common/                     # Общие модели, enum, схемы, utils
├── .env.example                # Образец файла окружения (без секретов)
├── docker-compose.yml          # Оркестрация сервисов
└── README.md
```

---

## ⚙️ Быстрый запуск

```bash
docker-compose up --build -d
```

### 🐳 Публичный образ Docker

```bash
docker pull pavlovaalla88/allures-backend:latest
```

Для запуска образа:

```bash
docker run -d \
  -p 8008:8000 \
  --env-file .env \
  pavlovaalla88/allures-backend:latest
```

> Убедитесь, что в `.env` указаны актуальные данные: подключения к PostgreSQL/Supabase, адреса микросервисов, API-ключи.

---

## 📊 Swagger UI (документация API)

| Сервис       | Swagger URL                                              |
| ------------ | -------------------------------------------------------- |
| Product      | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Sales        | [http://localhost:8001/docs](http://localhost:8001/docs) |
| Review       | [http://localhost:8002/docs](http://localhost:8002/docs) |
| Auth         | [http://localhost:8003/docs](http://localhost:8003/docs) |
| Profile      | [http://localhost:8004/docs](http://localhost:8004/docs) |
| Payment      | [http://localhost:8005/docs](http://localhost:8005/docs) |
| Discount     | [http://localhost:8006/docs](http://localhost:8006/docs) |
| Dashboard    | [http://localhost:8007/docs](http://localhost:8007/docs) |
| Admin        | [http://localhost:8010/docs](http://localhost:8010/docs) |
| Subscription | [http://localhost:8011/docs](http://localhost:8011/docs) |

---

## 🔐 Пример файла .env.example

```env
# PostgreSQL / Supabase
MAINDB_URL=postgresql://username:password@host:5432/database

# Альтернативно (если не используется MAINDB_URL напрямую)
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=your_password
DB_NAME=Alluresdb

# URL-адреса микросервисов
PRODUCT_SERVICE_URL=http://localhost:8000
SALES_SERVICE_URL=http://localhost:8001
REVIEW_SERVICE_URL=http://localhost:8002
AUTH_SERVICE_URL=http://localhost:8003
PROFILE_SERVICE_URL=http://localhost:8004
PAYMENTS_SERVICE_URL=http://localhost:8005
DISCOUNT_SERVICE_URL=http://localhost:8006
DASHBOARD_SERVICE_URL=http://localhost:8007
ADMIN_SERVICE_URL=http://localhost:8010
SUBSCRIPTION_SERVICE_URL=http://localhost:8011

# OpenAI API (GPT, рекомендации)
OPENAI_API_KEY=sk-yourkey
```

---

## 🔁 Примеры API (эндпоинты)

### Auth Service

| Метод | URL                     | Описание                         |
| ----- | ----------------------- | -------------------------------- |
| POST  | `/auth/register`        | Регистрация пользователя         |
| POST  | `/auth/login`           | Аутентификация, получение токена |
| POST  | `/auth/forgot-password` | Запрос на сброс пароля           |
| POST  | `/auth/reset-password`  | Сброс пароля                     |
| GET   | `/auth/users`           | Получение списка пользователей   |

### Discount Service

| Метод | URL          | Описание               |
| ----- | ------------ | ---------------------- |
| GET   | `/discount/` | Получить список скидок |
| POST  | `/discount/` | Создать новую скидку   |

```json
{
  "code": "NEWYEAR2026",
  "percentage": 18.0,
  "valid_until": "2026-01-01T00:00:00"
}
```

---

## 🧠 AI и Рекомендации

* Анализ тональности отзывов (NLTK)
* Генерация рекомендаций по ключевым словам
* Поддержка OpenAI (GPT API)

---

## 📦 Используемый стек

* FastAPI + Pydantic
* PostgreSQL (Supabase) + SQLAlchemy
* Docker + Docker Compose
* Gunicorn + Uvicorn + Nginx
* Pytest, dotenv
* OpenAI, NLTK, Tesseract

---

## 🛠 Планы по улучшению

* Планировщик для очистки неактивных скидок
* Полноценная аналитика в dashboard\_service
* WebSocket API (уведомления и чаты)
* Интеграция с Mono, Stripe, PayPal
* Юнит- и интеграционные тесты

---

## 🚀 Push на GitHub

```bash
git init
git remote add origin https://github.com/your-org/allures-backend.git
git checkout -b main
git add .
git commit -m "🚀 Initial backend release with Dockerfile"
git push -u origin main
```

---

## 📄 License

MIT License — feel free to use and contribute!
