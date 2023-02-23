from .schema import (
    QUERY,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@QUERY.field("billing")
@require_login
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **_kwargs: str
) -> dict[str, Any]:
    return {}
