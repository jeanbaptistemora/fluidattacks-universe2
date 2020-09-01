import re

from typing import Any

from graphql.type.definition import GraphQLResolveInfo
from backend.decorators import (
    concurrent_decorators,
    require_login,
    enforce_user_level_auth_async
)
from backend.typing import SimplePayload as SimplePayloadType
from backend import util


@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve_invalidate_cache(
        _: Any,
        info: GraphQLResolveInfo,
        pattern: str) -> SimplePayloadType:
    """Resolve invalidate_cache."""
    success = False
    regex = r'^\w+$|^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'
    if re.match(regex, pattern):
        util.queue_cache_invalidation(pattern)
        success = True
        util.cloudwatch_log(
            info.context,
            (f'Security: Pattern {pattern} was '
             'removed from cache')  # pragma: no cover
        )
    return SimplePayloadType(success=success)
