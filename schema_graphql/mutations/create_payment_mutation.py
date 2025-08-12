
import strawberry
import httpx
import os
from typing import Optional
from datetime import datetime

PAYMENTS_SERVICE_URL = os.getenv("PAYMENTS_SERVICE_URL")

@strawberry.type
class PaymentOut:
    id: int
    user_id: int
    amount: float
    status: str
    created_at: datetime

@strawberry.type
class CreatePaymentMutation:
    @strawberry.mutation
    async def create_payment(self, user_id: int, amount: float) -> Optional[PaymentOut]:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{PAYMENTS_SERVICE_URL}/payment/create", json={
                    "user_id": user_id,
                    "amount": amount,
                    "status": "pending"
                })
                res.raise_for_status()
                return PaymentOut(**res.json())
        except httpx.HTTPStatusError:
            return None
