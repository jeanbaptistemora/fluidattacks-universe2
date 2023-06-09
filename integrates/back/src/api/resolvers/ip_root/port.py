from .schema import (
    IP_ROOT,
)
from db_model.roots.types import (
    IPRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@IP_ROOT.field("port")
def resolve(_parent: IPRoot, _info: GraphQLResolveInfo) -> int:
    return 0
