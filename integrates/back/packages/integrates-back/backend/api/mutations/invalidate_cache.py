# Third party
from aioextensions import (
    collect,
    schedule,
)
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login
)
from backend.typing import SimplePayload
from redis_cluster.operations import redis_cmd


@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    pattern: str
) -> SimplePayload:
    schedule(collect([
        redis_cmd('delete', key)
        for key in await redis_cmd('keys', pattern)
    ]))

    util.cloudwatch_log(
        info.context,
        f'Security: Pattern {pattern} was removed from cache'
    )

    return SimplePayload(success=True)
