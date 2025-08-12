#services/auth_service/main.py
import sys
import os

# Добавление корневого пути
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from dotenv import load_dotenv

from common.db.session import get_db
from services.auth_service.routers import auth

# Strawberry GraphQL
import strawberry
from strawberry.fastapi import GraphQLRouter

from schema_graphql.auth_query import AuthQuery
from schema_graphql.mutations.login_mutation import LoginMutation, LoginResponse

# Загрузка .env
load_dotenv()

# Объединение Query и Mutation
@strawberry.type
class Query(AuthQuery):
    pass

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def login(self, login: str, password: str) -> LoginResponse | None:
        return await LoginMutation().login(login, password)

# Схема
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

# Инициализация FastAPI
app = FastAPI(title="Authorization Service")

# 🔗 Подключение REST роутеров и GraphQL
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(graphql_app, prefix="/graphql")

# Разрешение CORS
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

# Проверка подключения к PostgreSQL
@app.on_event("startup")
def startup_event():
    db_gen = get_db()
    db = next(db_gen)
    try:
        db.execute(text("SELECT 1"))
        print(" PostgreSQL подключение успешно (Authorization Service)")
    except Exception as e:
        print(f" Ошибка подключения к PostgreSQL: {e}")
    finally:
        db.close()

# Корень
@app.get("/")
def read_root():
    return {"message": "Authorization Service is running"}


# uvicorn services.auth_service.main:app --reload --port 8003