# schema_graphql/schema.py
import strawberry
from .auth_query import AuthQuery
from .product_query import ProductQuery
from .subscription_query import SubscriptionQuery
from .payments_query import PaymentsQuery
from .dashboard_query import DashboardQuery
from .review_query import ReviewQuery

@strawberry.type
class Query(
    AuthQuery,
    ProductQuery,
    SubscriptionQuery,
    PaymentsQuery,
    DashboardQuery,
    ReviewQuery
):
    pass

from .mutations import Mutation

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    auto_camel_case=True
)