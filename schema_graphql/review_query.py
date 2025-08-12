# schema_graphql/review_query.py
import strawberry
from typing import List, Optional
import httpx
from common.config.settings import settings

REVIEW_SERVICE_URL = settings.REVIEW_SERVICE_URL

@strawberry.type
class ReviewType:
    id: int
    product_id: int
    user_id: int
    text: str
    sentiment: str
    pos_score: Optional[float]
    neg_score: Optional[float]
    score: Optional[float]


@strawberry.type
class ReviewQuery:
    @strawberry.field
    async def get_reviews(self) -> List[ReviewType]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{REVIEW_SERVICE_URL}/reviews/reviews/")
            resp.raise_for_status()
            data = resp.json()
            return [ReviewType(**r) for r in data]

    @strawberry.field
    async def get_reviews_by_user(self, user_id: int) -> List[ReviewType]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{REVIEW_SERVICE_URL}/reviews/reviews/user/{user_id}")
            resp.raise_for_status()
            data = resp.json()
            return [ReviewType(**r) for r in data]

    @strawberry.field
    async def get_reviews_by_product(self, product_id: int) -> List[ReviewType]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{REVIEW_SERVICE_URL}/reviews/reviews/product/{product_id}")
            resp.raise_for_status()
            data = resp.json()
            return [ReviewType(**r) for r in data]
