from db_model.roots.types import (
    URLRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: URLRoot, _info: GraphQLResolveInfo) -> int:
    return int(parent.state.port)
