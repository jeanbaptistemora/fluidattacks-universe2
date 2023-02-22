from .schema import (
    CREDENTIALS,
)
from db_model.credentials.types import (
    Credentials,
    HttpsSecret,
)
from decorators import (
    enforce_owner,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@CREDENTIALS.field("user")
@enforce_owner
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> str | None:
    return (
        parent.state.secret.user
        if isinstance(parent.state.secret, HttpsSecret)
        else None
    )
