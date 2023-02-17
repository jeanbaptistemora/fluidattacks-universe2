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
from typing import (
    Optional,
)


@CREDENTIALS.field("key")
@enforce_owner
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> Optional[str]:
    return (
        parent.state.secret.key
        if isinstance(parent.state.secret, SshSecret)
        else None
    )
