from .schema import (
    CREDENTIALS,
)
from db_model.credentials.types import (
    Credentials,
    HttpsPatSecret,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@CREDENTIALS.field("isToken")
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> bool:
    return isinstance(parent.state.secret, HttpsPatSecret)
