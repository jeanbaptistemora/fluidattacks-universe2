# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
    schedule,
)
from api.mutations import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from redis_cluster.operations import (
    redis_cmd,
)


@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, pattern: str
) -> SimplePayload:
    schedule(
        collect(
            [
                redis_cmd("delete", key)
                for key in await redis_cmd("keys", pattern)
            ]
        )
    )

    logs_utils.cloudwatch_log(
        info.context, f"Security: Pattern {pattern} was removed from cache"
    )

    return SimplePayload(success=True)
