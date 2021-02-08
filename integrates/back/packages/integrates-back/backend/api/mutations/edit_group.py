# Standard library
from typing import Any

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import authz, util
from backend.dal.helpers.redis import (
    redis_del_by_deps,
)
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_integrates,
    turn_args_into_kwargs
)
from backend.domain import (
    project as group_domain,
    user as user_domain
)
from backend.exceptions import PermissionDenied
from backend.typing import SimplePayload as SimplePayloadType
from backend.utils.user import create_forces_user


@convert_kwargs_to_snake_case  # type: ignore
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
    reason: str,
    subscription: str
) -> SimplePayloadType:
    group_name = group_name.lower()
    user_info = await util.get_jwt_content(info.context)
    requester_email = user_info['user_email']
    success = False

    try:
        success = await group_domain.edit(
            context=info.context.loaders,
            comments=comments,
            group_name=group_name,
            has_drills=has_drills,
            has_forces=has_forces,
            has_integrates=has_integrates,
            reason=reason,
            requester_email=requester_email,
            subscription=subscription,
        )
    except PermissionDenied:
        util.cloudwatch_log(
            info.context,
            f'Security: Unauthorized role attempted to edit group'
        )

    if success and has_forces:
        await create_forces_user(info, group_name)
    elif (
        success and not has_forces and has_integrates and
        await user_domain.ensure_user_exists(
            user_domain.format_forces_user_email(group_name)
        )
    ):
        await group_domain.remove_user_access(
            group_name, user_domain.format_forces_user_email(group_name))
    if success:
        await redis_del_by_deps('edit_group', group_name=group_name)
        await authz.revoke_cached_group_service_attributes_policies(group_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Edited group {group_name} successfully',
        )

    return SimplePayloadType(success=success)
