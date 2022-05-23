from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_black,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from roots.domain import (
    update_ip_root,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_service_black
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    root_id: str,
    nickname: str,
) -> SimplePayload:
    user_info: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    await update_ip_root(
        loaders=info.context.loaders,
        user_email=user_email,
        group_name=group_name.lower(),
        root_id=root_id,
        nickname=nickname,
    )

    logs_utils.cloudwatch_log(info.context, f"Security: Updated root {id}")

    return SimplePayload(success=True)
