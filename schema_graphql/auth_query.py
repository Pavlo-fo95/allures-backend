
import strawberry
import httpx
import os
from typing import Optional
from .types import AuthUser

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

@strawberry.type
class AuthQuery:
    @strawberry.field
    def get_user_by_login(self, login: str) -> Optional[AuthUser]:
        try:
            response = httpx.get(f"{AUTH_SERVICE_URL}/user/by-login/{login}")
            response.raise_for_status()
            return AuthUser(**response.json())
        except httpx.HTTPStatusError:
            return None
