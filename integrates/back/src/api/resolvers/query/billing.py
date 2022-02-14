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


@require_login
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **_kwargs: str
) -> Dict[str, Any]:
    return {}
