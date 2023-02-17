from .schema import (
    CREDENTIALS,
)
from db_model.credentials.types import (
    Credentials,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.utils import (
    get_oauth_type,
)


@CREDENTIALS.field("oauthType")
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> str:
    return get_oauth_type(parent)
