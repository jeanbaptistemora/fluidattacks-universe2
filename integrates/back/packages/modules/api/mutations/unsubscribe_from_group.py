
from typing import Any

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import SimplePayload as SimplePayloadType
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from groups import domain as groups_domain
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from organizations import domain as orgs_domain
from redis_cluster.operations import redis_del_by_deps_soon


@convert_kwargs_to_snake_case
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
    stakeholder_info = await token_utils.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info['user_email']
    success = await groups_domain.remove_user(
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
        logs_utils.cloudwatch_log(info.context, msg)
    else:
        msg = (
            'Security: Attempted to unsubscribe stakeholder: '
            f'{stakeholder_email} from {group_name} group'
        )
        logs_utils.cloudwatch_log(info.context, msg)

    return SimplePayloadType(
        success=success
    )
