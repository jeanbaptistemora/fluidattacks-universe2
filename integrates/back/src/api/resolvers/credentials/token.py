from db_model.credentials.types import (
    Credentials,
    HttpsPatSecret,
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
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> Optional[str]:
    return (
        parent.state.secret.token
        if isinstance(parent.state.secret, HttpsPatSecret)
        else None
    )
