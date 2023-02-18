from .schema import (
    URL_ROOT,
)
from db_model.roots.types import (
    Root,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@URL_ROOT.field("state")
def resolve(parent: Root, _info: GraphQLResolveInfo) -> str:
    return parent.state.status
