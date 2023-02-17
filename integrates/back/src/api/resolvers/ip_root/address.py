from .schema import (
    IP_ROOT,
)
from db_model.roots.types import (
    IPRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@IP_ROOT.field("address")
def resolve(parent: IPRoot, _info: GraphQLResolveInfo) -> str:
    return parent.state.address
