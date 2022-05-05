from db_model.roots.types import (
    IPRootItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: IPRootItem, _info: GraphQLResolveInfo) -> int:
    return int(parent.state.port)
