
import strawberry
import httpx
import os
from typing import List
from .types import Payment

PAYMENTS_SERVICE_URL = os.getenv("PAYMENTS_SERVICE_URL")

@strawberry.type
class PaymentsQuery:
    @strawberry.field
    async def payments(self, user_id: int) -> List[Payment]:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{PAYMENTS_SERVICE_URL}/payments/user/{user_id}")
                res.raise_for_status()
                return [Payment(**p) for p in res.json()]
        except httpx.HTTPStatusError:
            return []
