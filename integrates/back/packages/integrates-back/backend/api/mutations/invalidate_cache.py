# Standard
import re

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login
)
from backend.typing import SimplePayload


@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    pattern: str
) -> SimplePayload:
    success = False
    regex = r'^\w+$|^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'

    if re.match(regex, pattern):
        util.queue_cache_invalidation(pattern)
        success = True
        util.cloudwatch_log(
            info.context,
            f'Security: Pattern {pattern} was removed from cache'
        )

    return SimplePayload(success=success)
