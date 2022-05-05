from db_model.roots.types import (
    RootItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: RootItem, _info: GraphQLResolveInfo) -> str:
    return parent.state.status
