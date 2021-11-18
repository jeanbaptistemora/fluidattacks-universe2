from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch import (
    dal as batch_dal,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from roots import (
    domain as roots_domain,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(require_login, enforce_group_level_auth_async)
@rename_kwargs(
    {"group_name": "source_group_name", "target_group_name": "group_name"}
)
@enforce_group_level_auth_async
@rename_kwargs(
    {"group_name": "target_group_name", "source_group_name": "group_name"}
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    group_name: str = kwargs["group_name"].lower()
    root_id: str = kwargs["id"]
    target_group_name: str = kwargs["target_group_name"].lower()

    new_root_id = await roots_domain.move_root(
        info.context.loaders,
        user_email,
        group_name,
        root_id,
        target_group_name,
    )
    await batch_dal.put_action(
        action_name="move_root",
        entity=f"{target_group_name}/{new_root_id}",
        subject=user_email,
        additional_info=f"{group_name}/{root_id}",
        queue="dedicated_soon",
    )

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Moved a root from {group_name} to {target_group_name}",
    )

    return SimplePayload(success=True)
