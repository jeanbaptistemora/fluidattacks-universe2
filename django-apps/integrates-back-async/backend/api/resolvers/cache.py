import re

from typing import Any
from ariadne import convert_kwargs_to_snake_case

from graphql.type.definition import GraphQLResolveInfo
from backend.decorators import (
    require_login,
    enforce_user_level_auth_async
)
from backend.typing import SimplePayload as SimplePayloadType
from backend import util


@require_login
@enforce_user_level_auth_async
@convert_kwargs_to_snake_case  # type: ignore
async def resolve_invalidate_cache(
        _: Any,
        info: GraphQLResolveInfo,
        pattern: str) -> SimplePayloadType:
    """Resolve invalidate_cache."""
    success = False
    regex = r'^\w+$'
    if re.match(regex, pattern):
        await util.invalidate_cache(pattern)
        success = True
        util.cloudwatch_log(
            info.context,
            (f'Security: Pattern {pattern} was '
             'removed from cache')  # pragma: no cover
        )
    return SimplePayloadType(success=success)
