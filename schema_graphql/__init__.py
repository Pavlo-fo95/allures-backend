import strawberry
from schema_graphql.mutations.login_mutation import LoginMutation, LoginResponse

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def login(self, login: str, password: str) -> LoginResponse | None:
        return await LoginMutation().login(login, password)