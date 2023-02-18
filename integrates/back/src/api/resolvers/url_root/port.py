from .schema import (
    URL_ROOT,
)
from db_model.roots.types import (
    URLRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@URL_ROOT.field("port")
def resolve(parent: URLRoot, _info: GraphQLResolveInfo) -> int:
    return int(parent.state.port)
