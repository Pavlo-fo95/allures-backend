#main.py product_service
import sys
import os

# Добавляем корень проекта для импорта общих модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from common.db.session import get_db
from common.config.settings import settings

from services.product_service.api.routes import router as product_router
from services.review_service.api.routes import router as review_router

# GraphQL
from strawberry.fastapi import GraphQLRouter
from schema_graphql import schema

# Загрузка переменных среды
load_dotenv()

# Инициализация FastAPI
app = FastAPI(title="Product Service")

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

# Вывод строки подключения
print("▶ MAINDB_URL из settings:", settings.MAINDB_URL)

# Подключение REST маршрутов
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(review_router, prefix="/reviews", tags=["Reviews"])

# Подключение GraphQL
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Проверка подключения к БД при старте
@app.on_event("startup")
def startup_event():
    db_gen = get_db()
    db = next(db_gen)
    try:
        db.execute(text("SELECT 1"))
        print("✅ PostgreSQL подключение успешно (Product Service)")
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
    finally:
        db.close()

# Тестовые эндпоинты
@app.get("/")
def root():
    return {"message": "Product Service is running"}

@app.get("/check-db")
def check_db():
    db_gen = get_db()
    db = next(db_gen)
    try:
        result = db.execute(text("SELECT * FROM products LIMIT 1")).fetchall()
        return {"products_count": len(result)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/review/{product_id}")
def get_reviews(product_id: int):
    return [{"id": 1, "product_id": product_id, "text": "Great!", "sentiment": "positive"}]

# uvicorn services.product_service.main:app --reload --port 8000