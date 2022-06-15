from db_model.credentials.types import (
    Credential,
    SshSecret,
)
from decorators import (
    enforce_organization_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@enforce_organization_level_auth_async
def resolve(parent: Credential, _info: GraphQLResolveInfo) -> Optional[str]:
    return (
        parent.state.secret.key
        if isinstance(parent.state.secret, SshSecret)
        else None
    )
