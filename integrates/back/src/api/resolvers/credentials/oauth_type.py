from db_model.credentials.types import (
    Credentials,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.utils import (
    get_oauth_type,
)


def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> str:
    return get_oauth_type(parent)
