from .schema import (
    IP_ROOT,
)
from db_model.roots.types import (
    Root,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@IP_ROOT.field("nickname")
def resolve(parent: Root, _info: GraphQLResolveInfo) -> str:
    return parent.state.nickname
