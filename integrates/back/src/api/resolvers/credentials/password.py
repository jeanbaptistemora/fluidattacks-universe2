from db_model.credentials.types import (
    Credential,
    HttpsSecret,
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
        parent.state.secret.password
        if isinstance(parent.state.secret, HttpsSecret)
        else None
    )
