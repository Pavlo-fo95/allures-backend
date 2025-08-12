#services/dashboard_service/main.py
import sys
import os
import common.utils.env_loader

# Добавление корневого пути (для импорта общих модулей)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from dotenv import load_dotenv

from services.dashboard_service.routers import dashboard
from common.db.session import get_db

# Загрузка .env
load_dotenv()

# Инициализация FastAPI
app = FastAPI(title="Dashboard Service")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://api.alluresallol.com",
        "https://alluresallol.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 Подключение REST-роутера
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# ✅ Проверка подключения к БД
@app.on_event("startup")
def startup_event():
    db_gen = get_db()
    db = next(db_gen)
    try:
        db.execute(text("SELECT 1"))
        print("✅ PostgreSQL подключение успешно (Dashboard Service)")
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
    finally:
        db.close()

# Корневой эндпоинт
@app.get("/")
def root():
    return {"message": "Dashboard Service is running"}

# Статичный summary endpoint — для устранения ошибки 422
@app.get("/dashboard/summary")
def get_summary():
    return {"summary": "Dashboard summary is working"}

# uvicorn services.dashboard_service.main:app --reload --port 8007
