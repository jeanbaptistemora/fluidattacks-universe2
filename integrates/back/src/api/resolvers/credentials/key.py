from db_model.credentials.types import (
    Credential,
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


@enforce_owner
def resolve(parent: Credential, _info: GraphQLResolveInfo) -> Optional[str]:
    return (
        parent.state.secret.key
        if isinstance(parent.state.secret, SshSecret)
        else None
    )
