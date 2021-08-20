from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimpleFindingPayload as SimpleFindingPayloadType,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
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
)
from newutils.utils import (
    duplicate_dict_keys,
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
    require_finding_access,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, finding_id: str, **parameters: Any
) -> SimpleFindingPayloadType:
    if (
        "attack_vector_desc" in parameters
        or "attack_vector_description" in parameters
    ):
        parameters = duplicate_dict_keys(
            parameters, "attack_vector_description", "attack_vector_desc"
        )
    success = await findings_domain.update_description(finding_id, parameters)
    if success:
        info.context.loaders.finding.clear(finding_id)
        redis_del_by_deps_soon(
            "update_finding_description",
            finding_id=finding_id,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated description in finding "
            f"{finding_id} with success",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update description in finding {finding_id}",
        )

    finding_loader = info.context.loaders.finding
    finding = await finding_loader.load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)
