from db_model.credentials.types import (
    Credentials,
    HttpsPatSecret,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> bool:
    return isinstance(parent.state.secret, HttpsPatSecret)
