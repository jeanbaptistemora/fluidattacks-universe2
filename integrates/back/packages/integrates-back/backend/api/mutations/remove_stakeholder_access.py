# Standard library
from typing import Any

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.dal.helpers.redis import redis_del_by_deps_soon
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.typing import (
    RemoveStakeholderAccessPayload as RemoveStakeholderAccessPayloadType
)
from groups import domain as groups_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    project_name: str,
    user_email: str
) -> RemoveStakeholderAccessPayloadType:
    success = await groups_domain.remove_user(
        info.context.loaders,
        project_name,
        user_email
    )
    removed_email = user_email if success else ''
    if success:
        redis_del_by_deps_soon(
            'remove_stakeholder_access',
            group_name=project_name,
        )
        msg = (
            f'Security: Removed stakeholder: {user_email} from {project_name} '
            f'project successfully'
        )
        util.cloudwatch_log(info.context, msg)
    else:
        msg = (
            f'Security: Attempted to remove stakeholder: {user_email} '
            f'from {project_name} project'
        )
        util.cloudwatch_log(info.context, msg)

    return RemoveStakeholderAccessPayloadType(
        success=success,
        removed_email=removed_email
    )
