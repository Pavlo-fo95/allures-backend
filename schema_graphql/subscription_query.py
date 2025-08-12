
import strawberry
import httpx
import os
from typing import Optional
from .types import UserSubscription, Subscription

SUBSCRIPTION_SERVICE_URL = os.getenv("SUBSCRIPTION_SERVICE_URL")

@strawberry.type
class SubscriptionQuery:
    @strawberry.field
    async def subscription(self, user_id: int) -> Optional[UserSubscription]:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{SUBSCRIPTION_SERVICE_URL}/subscription/user/{user_id}")
                res.raise_for_status()
                data = res.json()
                sub_data = data.pop("subscription", None)
                subscription_obj = Subscription(**sub_data) if sub_data else None
                return UserSubscription(**data, subscription=subscription_obj)
        except httpx.HTTPStatusError:
            return None
