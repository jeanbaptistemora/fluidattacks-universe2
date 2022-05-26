from db_model.roots.types import (
    URLRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


def resolve(parent: URLRoot, _info: GraphQLResolveInfo) -> Optional[str]:
    return parent.state.query
