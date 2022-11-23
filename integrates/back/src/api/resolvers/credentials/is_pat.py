from db_model.credentials.types import (
    Credentials,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> bool:
    return parent.state.is_pat
