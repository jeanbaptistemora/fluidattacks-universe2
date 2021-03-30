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
from backend.domain import project as group_domain
from backend.typing import SimplePayload as SimplePayloadType
from organizations import domain as orgs_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str
) -> SimplePayloadType:
    stakeholder_info = await util.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info['user_email']
    success = await group_domain.remove_user_access(
        info.context.loaders,
        group_name,
        stakeholder_email
    )

    if success:
        group_org_id = await orgs_domain.get_id_for_group(group_name)
        redis_del_by_deps_soon(
            'unsubscribe_from_group',
            group_name=group_name,
            organization_id=group_org_id
        )
        msg = (
            f'Security: Unsubscribed stakeholder: {stakeholder_email} '
            f'from {group_name} group successfully'
        )
        util.cloudwatch_log(info.context, msg)
    else:
        msg = (
            'Security: Attempted to unsubscribe stakeholder: '
            f'{stakeholder_email} from {group_name} group'
        )
        util.cloudwatch_log(info.context, msg)

    return SimplePayloadType(
        success=success
    )
