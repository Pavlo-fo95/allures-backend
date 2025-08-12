
# schema_graphql/mutations/login_mutation.py
import strawberry
import httpx
import os
from typing import Optional
from datetime import datetime

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

@strawberry.type
class LoginResponse:
    access_token: str
    token_type: str
    login: str
    role: str
    registered_at: datetime
    id: int
    is_blocked: bool

@strawberry.type
class LoginMutation:
    @strawberry.mutation
    async def login(self, login: str, password: str) -> Optional[LoginResponse]:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{AUTH_SERVICE_URL}/auth/login", json={
                    "login": login,
                    "password": password
                })
                res.raise_for_status()
                return LoginResponse(**res.json())
        except httpx.HTTPStatusError:
            return None
