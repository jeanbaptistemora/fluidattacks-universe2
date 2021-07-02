from ariadne import (
    convert_kwargs_to_snake_case,
)
import authz
from custom_exceptions import (
    PermissionDenied,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
    turn_args_into_kwargs,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from newutils.utils import (
    resolve_kwargs,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
@turn_args_into_kwargs
async def mutate(  # pylint: disable=too-many-arguments
    _: Any,
    info: GraphQLResolveInfo,
    comments: str,
    group_name: str,
    reason: str,
    subscription: str,
    **kwargs: Any,
) -> SimplePayloadType:
    loaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await token_utils.get_jwt_content(info.context)
    requester_email = user_info["user_email"]
    success = False

    # Compatibility with old API
    has_asm: bool = resolve_kwargs(kwargs, "has_asm", "has_integrates")
    has_machine: bool = resolve_kwargs(kwargs, "has_machine", "has_skims")
    has_squad: bool = resolve_kwargs(kwargs, "has_squad", "has_drills")

    try:
        success = await groups_domain.edit(
            context=loaders,
            comments=comments,
            group_name=group_name,
            has_squad=has_squad,
            has_asm=has_asm,
            has_machine=has_machine,
            reason=reason,
            requester_email=requester_email,
            subscription=subscription,
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context, "Security: Unauthorized role attempted to edit group"
        )

    if success:
        loaders.group.clear(group_name)
        await redis_del_by_deps("edit_group", group_name=group_name)
        await authz.revoke_cached_group_service_policies(group_name)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Edited group {group_name} successfully",
        )

    return SimplePayloadType(success=success)
