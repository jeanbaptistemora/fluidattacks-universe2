from db_model.roots.types import (
    Root,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: Root, _info: GraphQLResolveInfo) -> str:
    return parent.state.nickname
