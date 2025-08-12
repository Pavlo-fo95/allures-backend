#services/subscription_service/main.py
import sys
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from services.subscription_service.routers.subscription_routers import router as subscription_router

# Добавление корня для импорта из common и schema_graphql
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from common.db.session import get_db
from dotenv import load_dotenv

# Strawberry GraphQL
import strawberry
from strawberry.fastapi import GraphQLRouter
from schema_graphql.subscription_query import SubscriptionQuery
from schema_graphql.mutations import Mutation

# Загрузка переменных окружения
load_dotenv()

# Инициализация FastAPI
app = FastAPI(title="Subscription Service")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://allures-allol.com",
        "https://allures-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST маршруты
app.include_router(subscription_router, prefix="/subscription", tags=["Subscription"])

# GraphQL Query + Mutation
@strawberry.type
class Query(SubscriptionQuery):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Проверка подключения к БД
@app.on_event("startup")
def startup_event():
    db_gen = get_db()
    db = next(db_gen)
    try:
        db.execute(text("SELECT 1"))
        print(" PostgreSQL подключение успешно (Subscription Service)")
    except Exception as e:
        print(f" Ошибка подключения к PostgreSQL: {e}")
    finally:
        db.close()

# Корневой эндпоинт
@app.get("/")
def root():
    return {"message": "Subscription Service is running"}

# uvicorn services.subscription_service.main:app --reload --port 8011