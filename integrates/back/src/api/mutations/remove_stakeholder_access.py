from api.mutations import (
    RemoveStakeholderAccessPayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
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


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    user_email: str,
    group_name: str,
) -> RemoveStakeholderAccessPayload:
    user_data = await token_utils.get_jwt_content(info.context)
    requester_email = user_data["user_email"]
    await groups_domain.remove_user(
        info.context.loaders, group_name, user_email, requester_email
    )
    redis_del_by_deps_soon(
        "remove_stakeholder_access",
        group_name=group_name,
    )
    msg = (
        f"Security: Removed stakeholder: {user_email} from {group_name} "
        "group successfully"
    )
    logs_utils.cloudwatch_log(info.context, msg)

    return RemoveStakeholderAccessPayload(
        success=True, removed_email=user_email
    )
