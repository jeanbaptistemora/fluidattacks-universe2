from db_model.credentials.types import (
    Credential,
    HttpsPatSecret,
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
        parent.state.secret.token
        if isinstance(parent.state.secret, HttpsPatSecret)
        else None
    )
