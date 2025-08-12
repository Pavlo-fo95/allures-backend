import httpx
from common.config.settings import settings
from sqlalchemy.orm import Session
from common.models.dashboard_log import DashboardLog
from datetime import datetime

SALES_SERVICE_URL = settings.SALES_SERVICE_URL
REVIEW_SERVICE_URL = settings.REVIEW_SERVICE_URL

async def get_sales_count(user_id: int) -> int:
    """
    Получает количество продаж для конкретного пользователя.
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{SALES_SERVICE_URL}/sales/sales/user/{user_id}")
            resp.raise_for_status()
            data = resp.json()
            return len(data) if isinstance(data, list) else 0
    except Exception as e:
        print(f" Ошибка при получении продаж пользователя {user_id}: {e}")
        return 0

async def get_reviews_count(user_id: int) -> int:
    """
    Получает количество отзывов пользователя из общего списка.
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{REVIEW_SERVICE_URL}/reviews/reviews/")
            resp.raise_for_status()
            reviews = resp.json()
            if isinstance(reviews, list):
                return sum(1 for r in reviews if r.get("user_id") == user_id)
    except Exception as e:
        print(f" Ошибка при получении отзывов пользователя {user_id}: {e}")
    return 0

def save_dashboard_log(db: Session, user_id: int, user_agent: str):
    """
    Сохраняет лог входа пользователя на дашборд.
    """
    log = DashboardLog(
        user_id=user_id,
        user_agent=user_agent,
        accessed_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()


def save_dashboard_log(db: Session, user_id: int, user_agent: str):
    """
    Сохраняет лог входа пользователя на дашборд.
    """
    log = DashboardLog(
        user_id=user_id,
        user_agent=user_agent,
        accessed_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
