from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    UnavailabilityError,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from typing import (
    Any,
)


@MUTATION.field("invalidateAccessToken")
@convert_kwargs_to_snake_case
@require_login
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
) -> SimplePayload:
    user_info = await sessions_domain.get_jwt_content(info.context)
    try:
        await stakeholders_domain.remove_access_token(user_info["user_email"])
        logs_utils.cloudwatch_log(
            info.context, f'{user_info["user_email"]} invalidate access token'
        )
    except UnavailabilityError:
        logs_utils.cloudwatch_log(
            info.context,
            f'{user_info["user_email"]} attempted to invalidate access token',
        )

    return SimplePayload(success=True)
