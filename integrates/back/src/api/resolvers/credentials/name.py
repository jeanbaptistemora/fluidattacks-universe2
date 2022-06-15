from db_model.credentials.types import (
    Credential,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: Credential, _info: GraphQLResolveInfo) -> str:
    return parent.state.name
