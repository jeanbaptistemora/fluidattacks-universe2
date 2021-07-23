from ariadne.utils import (
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
    require_asm,
    require_login,
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
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, group_name: str, reason: str
) -> SimplePayloadType:
    loaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await token_utils.get_jwt_content(info.context)
    requester_email = user_info["user_email"]
    success = False

    try:
        success = await groups_domain.edit(
            context=loaders,
            comments="",
            group_name=group_name,
            has_machine=False,
            has_squad=False,
            has_asm=False,
            reason=reason,
            requester_email=requester_email,
            service="WHITE",
            subscription="continuous",
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Unauthorized role attempted to delete group",
        )

    if success:
        loaders.group.clear(group_name)
        redis_del_by_deps_soon("remove_group", group_name=group_name)
        await authz.revoke_cached_group_service_policies(group_name)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Deleted group {group_name} successfully",
        )

    return SimplePayloadType(success=success)
