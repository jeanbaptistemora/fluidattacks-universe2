from db_model.roots.types import (
    IPRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: IPRoot, _info: GraphQLResolveInfo) -> str:
    return parent.state.address
