from .schema import (
    URL_ROOT,
)
from db_model.roots.types import (
    URLRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@URL_ROOT.field("path")
def resolve(parent: URLRoot, _info: GraphQLResolveInfo) -> str:
    return parent.state.path
