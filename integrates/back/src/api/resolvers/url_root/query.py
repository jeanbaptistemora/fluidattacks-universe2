from .schema import (
    URL_ROOT,
)
from db_model.roots.types import (
    URLRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@URL_ROOT.field("query")
def resolve(parent: URLRoot, _info: GraphQLResolveInfo) -> Optional[str]:
    return parent.state.query
