from .schema import (
    URL_ROOT,
)
from db_model.roots.types import (
    URLRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@URL_ROOT.field("query")
def resolve(parent: URLRoot, _info: GraphQLResolveInfo) -> str | None:
    return parent.state.query
