from db_model.roots.types import (
    URLRootItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: URLRootItem, _info: GraphQLResolveInfo) -> int:
    return int(parent.state.port)
