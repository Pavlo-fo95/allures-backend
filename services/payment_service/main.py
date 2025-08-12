#services/payment_service/main.py
import sys
import os
import common.utils.env_loader

# Добавление корневого пути
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from common.db.session import get_db
from services.payment_service.routers.payment import router as payment_router

# Strawberry GraphQL
import strawberry
from strawberry.fastapi import GraphQLRouter
from schema_graphql.payments_query import PaymentsQuery as GQLQuery

# Загрузка .env
load_dotenv()

# Инициализация FastAPI
app = FastAPI(title="Payment Service")

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

# 🔗 REST маршруты
app.include_router(payment_router, prefix="/payment", tags=["Payment Methods"])

# 🧠 GraphQL
schema = strawberry.Schema(query=GQLQuery)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Проверка подключения к PostgreSQL
@app.on_event("startup")
def startup_event():
    db_gen = get_db()
    db = next(db_gen)
    try:
        db.execute(text("SELECT 1"))
        print(" ✅ PostgreSQL подключение успешно (Payment Service)")
    except Exception as e:
        print(f" ❌ Ошибка подключения к PostgreSQL: {e}")
    finally:
        db.close()

# Корневой эндпоинт
@app.get("/")
def read_root():
    return {"message": "Payment Service is running"}


# uvicorn services.payment_service.main:app --reload --port 8005