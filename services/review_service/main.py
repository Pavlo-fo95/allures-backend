# services/review_service/main.py
import sys
import os

# Добавление корневого пути (для доступа к /services и /common)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from dotenv import load_dotenv

from common.db.base import Base
from common.db.session import engine, get_db
from services.review_service.api.routes import router

# Strawberry GraphQL
from strawberry.fastapi import GraphQLRouter
from schema_graphql.schema import schema

# Загрузка .env
load_dotenv()

# Инициализация FastAPI
app = FastAPI(title="Review Service")

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

# REST роутеры
app.include_router(router, prefix="/reviews", tags=["Reviews"])

# GraphQL
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Создание таблиц и проверка подключения
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db_gen = get_db()
    db = next(db_gen)
    try:
        db.execute(text("SELECT 1"))
        print("✅ PostgreSQL подключение успешно (Review Service)")
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
    finally:
        db.close()

# Корневой эндпоинт
@app.get("/")
def root():
    return {"message": "Review Service is running"}

# uvicorn services.review_service.main:app --reload --port 8002