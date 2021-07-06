from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimpleFindingPayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    utils,
)
from newutils.utils import (
    resolve_kwargs,
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
    _parent: None, info: GraphQLResolveInfo, **parameters: Any
) -> SimpleFindingPayload:
    data = parameters.get("data", dict())
    data = {utils.snakecase_to_camelcase(k): data[k] for k in data}
    finding_id = parameters.get("finding_id", "")
    finding_loader = info.context.loaders.finding
    finding_data = await finding_loader.load(finding_id)
    group_name = resolve_kwargs(finding_data)
    success = False
    success = await findings_domain.save_severity(data)
    if success:
        info.context.loaders.finding.clear(finding_id)
        redis_del_by_deps_soon(
            "update_severity", finding_id=finding_id, group_name=group_name
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated severity in finding {finding_id} successfully",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to update severity in finding {finding_id}",
        )
    finding_loader = info.context.loaders.finding
    finding = await finding_loader.load(finding_id)
    return SimpleFindingPayload(finding=finding, success=success)
