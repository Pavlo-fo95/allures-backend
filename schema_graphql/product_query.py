
import strawberry
import httpx
import os
from typing import List
from .types import Product, Review
from .utils import camel_to_snake

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")
REVIEW_SERVICE_URL = os.getenv("REVIEW_SERVICE_URL")

@strawberry.type
class ProductQuery:
    @strawberry.field
    async def products(self) -> List[Product]:
        if not PRODUCT_SERVICE_URL or not REVIEW_SERVICE_URL:
            raise ValueError("❌ URLs для продуктов и отзывов не заданы")

        async with httpx.AsyncClient() as client:
            res = await client.get(f"{PRODUCT_SERVICE_URL}/products/")
            res.raise_for_status()
            products = res.json()

            result = []
            for p in products:
                r = await client.get(f"{REVIEW_SERVICE_URL}/reviews/product/{p['id']}")
                reviews_data = r.json() if r.status_code == 200 else []
                converted_reviews = [
                    Review(
                        id=review["id"],
                        product_id=review["product_id"],
                        text=review["text"],
                        sentiment=review["sentiment"],
                        pos_score=review.get("pos_score"),
                        neg_score=review.get("neg_score"),
                        _created_at=review.get("created_at")
                    )
                    for review in reviews_data
                ]
                snake_case_product = {camel_to_snake(k): v for k, v in p.items()}
                snake_case_product["_reviews"] = converted_reviews
                result.append(Product(**snake_case_product))
            return result
