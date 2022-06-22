from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@require_login
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
) -> SimplePayloadType:
    user_info = await token_utils.get_jwt_content(info.context)

    success = await stakeholders_domain.remove_access_token(
        user_info["user_email"]
    )
    if success:
        logs_utils.cloudwatch_log(
            info.context, f'{user_info["user_email"]} invalidate access token'
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f'{user_info["user_email"]} attempted to invalidate access token',
        )

    return SimplePayloadType(success=success)
