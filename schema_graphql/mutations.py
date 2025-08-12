
import strawberry
from .mutations.login_mutation import LoginMutation
from .mutations.create_payment_mutation import CreatePaymentMutation

@strawberry.type
class Mutation(LoginMutation, CreatePaymentMutation):
    pass
