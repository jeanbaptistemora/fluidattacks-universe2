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
    Dict,
)


@QUERY.field("billing")
@require_login
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **_kwargs: str
) -> Dict[str, Any]:
    return {}
