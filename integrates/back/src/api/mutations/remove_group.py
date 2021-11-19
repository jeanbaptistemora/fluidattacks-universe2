from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
import authz
from custom_exceptions import (
    PermissionDenied,
)
from custom_types import (
    SimplePayload,
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
) -> SimplePayload:
    try:
        loaders = info.context.loaders
        group_name = group_name.lower()
        user_info = await token_utils.get_jwt_content(info.context)
        group = await loaders.group.load(group_name)
        requester_email = user_info["user_email"]
        success = False
        success = await groups_domain.update_group_attrs(
            loaders=loaders,
            comments="",
            group_name=group_name,
            has_machine=False,
            has_squad=False,
            has_asm=False,
            reason=reason,
            requester_email=requester_email,
            service=group["service"],
            subscription=group["subscription"],
        )
        if success:
            redis_del_by_deps_soon("remove_group", group_name=group_name)
            await authz.revoke_cached_group_service_policies(group_name)
            logs_utils.cloudwatch_log(
                info.context,
                f"Security: Removed group {group_name} successfully",
            )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Unauthorized role attempted to remove a group",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context, f"Security: Attempted to remove group {group_name}"
        )
        raise
    return SimplePayload(success=success)
