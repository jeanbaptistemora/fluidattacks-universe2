# Standard library
from typing import Any

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.dal.helpers.redis import (
    redis_del_by_deps_soon,
)
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_finding_access,
    require_integrates,
    require_login
)
from backend.domain import finding as finding_domain
from backend.typing import SimpleFindingPayload as SimpleFindingPayloadType


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    finding_id: str,
    **parameters: Any
) -> SimpleFindingPayloadType:
    success = await finding_domain.update_description(
        finding_id, parameters
    )
    if success:
        redis_del_by_deps_soon(
            'update_finding_description',
            finding_id=finding_id,
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Updated description in finding '
            f'{finding_id} with success'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Tried to update description in finding {finding_id}'
        )

    finding_loader = info.context.loaders.finding
    finding = await finding_loader.load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)
