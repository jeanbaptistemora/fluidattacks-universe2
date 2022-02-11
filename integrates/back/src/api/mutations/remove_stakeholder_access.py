from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    RemoveStakeholderAccessPayload as RemoveStakeholderAccessPayloadType,
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
    _: Any,
    info: GraphQLResolveInfo,
    user_email: str,
    group_name: str,
) -> RemoveStakeholderAccessPayloadType:
    success = await groups_domain.remove_user(
        info.context.loaders, group_name, user_email
    )
    removed_email = user_email if success else ""
    if success:
        redis_del_by_deps_soon(
            "remove_stakeholder_access",
            group_name=group_name,
        )
        msg = (
            f"Security: Removed stakeholder: {user_email} from {group_name} "
            f"group successfully"
        )
        logs_utils.cloudwatch_log(info.context, msg)
    else:
        msg = (
            f"Security: Attempted to remove stakeholder: {user_email} "
            f"from {group_name} group"
        )
        logs_utils.cloudwatch_log(info.context, msg)

    return RemoveStakeholderAccessPayloadType(
        success=success, removed_email=removed_email
    )
