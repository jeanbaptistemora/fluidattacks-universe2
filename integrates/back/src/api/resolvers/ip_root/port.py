from db_model.roots.types import (
    IPRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(_parent: IPRoot, _info: GraphQLResolveInfo) -> int:
    return 0
