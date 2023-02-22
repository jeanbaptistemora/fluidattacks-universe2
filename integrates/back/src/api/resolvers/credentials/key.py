from .schema import (
    CREDENTIALS,
)
from db_model.credentials.types import (
    Credentials,
    SshSecret,
)
from decorators import (
    enforce_owner,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@CREDENTIALS.field("key")
@enforce_owner
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> str | None:
    return (
        parent.state.secret.key
        if isinstance(parent.state.secret, SshSecret)
        else None
    )
