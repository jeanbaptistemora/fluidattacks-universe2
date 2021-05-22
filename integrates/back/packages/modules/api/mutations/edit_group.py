from typing import Any

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

import authz
from custom_exceptions import PermissionDenied
from custom_types import SimplePayload as SimplePayloadType
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
    turn_args_into_kwargs,
)
from forces import domain as forces_domain
from groups import domain as groups_domain
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from redis_cluster.operations import redis_del_by_deps
from users import domain as users_domain


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
    has_drills: bool,
    has_forces: bool,
    has_integrates: bool,
    has_skims: bool,
    reason: str,
    subscription: str,
) -> SimplePayloadType:
    loaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await token_utils.get_jwt_content(info.context)
    requester_email = user_info["user_email"]
    success = False

    try:
        success = await groups_domain.edit(
            context=loaders,
            comments=comments,
            group_name=group_name,
            has_drills=has_drills,
            has_forces=has_forces,
            has_integrates=has_integrates,
            has_skims=has_skims,
            reason=reason,
            requester_email=requester_email,
            subscription=subscription,
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context, "Security: Unauthorized role attempted to edit group"
        )

    if success and has_forces:
        await forces_domain.create_forces_user(info, group_name)
    elif (
        success
        and not has_forces
        and has_integrates
        and await users_domain.ensure_user_exists(
            forces_domain.format_forces_user_email(group_name)
        )
    ):
        await groups_domain.remove_user(
            loaders,
            group_name,
            forces_domain.format_forces_user_email(group_name),
        )
    if success:
        loaders.group_all.clear(group_name)
        await redis_del_by_deps("edit_group", group_name=group_name)
        await authz.revoke_cached_group_service_policies(group_name)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Edited group {group_name} successfully",
        )

    return SimplePayloadType(success=success)
