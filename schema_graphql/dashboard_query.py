import os
import strawberry
import httpx

@strawberry.type
class DashboardStats:
    total_users: int
    total_sales: float
    active_discounts: int
    active_profiles: int
    total_admins: int

# Загрузка URL'ов микросервисов из .env
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
SALES_SERVICE_URL = os.getenv("SALES_SERVICE_URL")
DISCOUNT_SERVICE_URL = os.getenv("DISCOUNT_SERVICE_URL")
PROFILE_SERVICE_URL = os.getenv("PROFILE_SERVICE_URL")
ADMIN_SERVICE_URL = os.getenv("ADMIN_SERVICE_URL")

@strawberry.type
class DashboardQuery:
    @strawberry.field
    async def get_dashboard_stats(self) -> DashboardStats:
        async with httpx.AsyncClient() as client:
            try:
                res_users = await client.get(f"{AUTH_SERVICE_URL}/auth/count")
                res_sales = await client.get(f"{SALES_SERVICE_URL}/sales/total")
                res_discounts = await client.get(f"{DISCOUNT_SERVICE_URL}/discounts/active")
                res_profiles = await client.get(f"{PROFILE_SERVICE_URL}/profiles/active")
                res_admins = await client.get(f"{ADMIN_SERVICE_URL}/admin/count")

                return DashboardStats(
                    total_users=res_users.json().get("count", 0),
                    total_sales=res_sales.json().get("total_sales", 0.0),
                    active_discounts=res_discounts.json().get("active", 0),
                    active_profiles=res_profiles.json().get("active", 0),
                    total_admins=res_admins.json().get("count", 0)
                )
            except Exception as e:
                print("❌ Ошибка при сборе dashboard статистики:", str(e))
                return DashboardStats(
                    total_users=0,
                    total_sales=0.0,
                    active_discounts=0,
                    active_profiles=0,
                    total_admins=0
                )
