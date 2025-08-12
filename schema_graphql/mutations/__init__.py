# schema_graphql/mutations/__init__.py
import strawberry
from schema_graphql.mutations.login_mutation import LoginMutation
from schema_graphql.mutations.create_payment_mutation import CreatePaymentMutation

login_mutation = LoginMutation()
create_payment_mutation = CreatePaymentMutation()

@strawberry.type
class Mutation:
    login = strawberry.field(resolver=login_mutation.login)
    create_payment = strawberry.field(resolver=create_payment_mutation.create_payment)
    # create_subscription = strawberry.field(resolver=...
    # your_function...)