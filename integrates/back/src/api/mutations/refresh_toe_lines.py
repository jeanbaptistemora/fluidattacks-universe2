from api import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from batch.dal import (
    put_action,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, **parameters: Any
) -> SimplePayload:
    try:
        group_name = parameters["group_name"]
        user_info = await token_utils.get_jwt_content(info.context)

        await put_action(
            action_name="refresh_toe_lines",
            entity=group_name,
            subject=user_info["user_email"],
            additional_info="",
            queue="spot_later",
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Schedule the toe lines refreshing in {group_name} "
            "group successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to schedule the toe lines refreshing in "
            f"{group_name} group",
        )
        raise

    return SimplePayload(success=True)
