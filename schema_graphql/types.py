
import strawberry
from typing import Optional, List
from datetime import datetime

@strawberry.type
class Review:
    id: int
    product_id: int
    text: str
    sentiment: str
    pos_score: Optional[float]
    neg_score: Optional[float]
    _created_at: Optional[str]

    @strawberry.field(name="createdAt")
    def created_at(self) -> Optional[str]:
        return self._created_at

@strawberry.type
class Product:
    id: int
    name: str
    description: Optional[str]
    price: float
    old_price: Optional[float]
    image: str
    status: Optional[str]
    current_inventory: Optional[int]
    is_hit: Optional[bool]
    is_discount: Optional[bool]
    is_new: Optional[bool]
    category_id: Optional[int]
    category_name: Optional[str]
    subcategory: Optional[str]
    product_type: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    _reviews: Optional[List[Review]] = None

    @strawberry.field
    def reviews(self) -> Optional[List[Review]]:
        return self._reviews

@strawberry.type
class AuthUser:
    id: int
    login: str
    full_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    avatar_url: Optional[str]
    language: Optional[str]
    bonus_balance: Optional[int]
    delivery_address: Optional[str]
    registered_at: datetime
    role: Optional[str]
    is_blocked: Optional[bool]

@strawberry.type
class Subscription:
    id: int
    code: str
    language: str
    name: str
    price: int
    duration_days: int
    product_limit: int
    promo_balance: int
    support_level: Optional[str]
    stats_access: bool
    description: Optional[str]

@strawberry.type
class UserSubscription:
    id: int
    user_id: int
    subscription_id: int
    start_date: datetime
    end_date: datetime
    is_active: bool
    subscription: Subscription

@strawberry.type
class Payment:
    id: int
    user_id: int
    amount: float
    status: str
    created_at: str
