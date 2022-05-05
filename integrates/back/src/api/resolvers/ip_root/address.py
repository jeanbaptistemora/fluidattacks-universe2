from db_model.roots.types import (
    IPRootItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: IPRootItem, _info: GraphQLResolveInfo) -> str:
    return parent.state.address
