from .schema import (
    GIT_ROOT,
)
from db_model.roots.types import (
    Root,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GIT_ROOT.field("state")
def resolve(parent: Root, _info: GraphQLResolveInfo) -> str:
    return parent.state.status
