# Standard
from typing import Any

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.domain import finding as finding_domain
from backend.typing import SimpleFindingPayload


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> SimpleFindingPayload:
    data = parameters.get('data', dict())
    data = {util.snakecase_to_camelcase(k): data[k] for k in data}
    finding_id = parameters.get('finding_id', '')
    finding_loader = info.context.loaders['finding']
    finding_data = await finding_loader.load(finding_id)
    group_name = finding_data['project_name']
    success = False
    success = await finding_domain.save_severity(data)
    if success:
        util.queue_cache_invalidation(
            f'severity*{finding_id}',
            f'severity*{group_name}'
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Updated severity in finding {finding_id} successfully'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to update severity in finding {finding_id}'
        )
    finding = await info.context.loaders['finding'].load(finding_id)
    return SimpleFindingPayload(finding=finding, success=success)
