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


@CREDENTIALS.field("password")
@enforce_owner
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> str | None:
    return (
        parent.state.secret.password
        if isinstance(parent.state.secret, HttpsSecret)
        else None
    )
