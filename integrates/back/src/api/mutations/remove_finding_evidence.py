from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimpleFindingPayload as SimpleFindingPayloadType,
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
    _parent: None, info: GraphQLResolveInfo, evidence_id: str, finding_id: str
) -> SimpleFindingPayloadType:
    """Resolve remove_evidence mutation."""
    success = await findings_domain.remove_evidence(evidence_id, finding_id)

    if success:
        info.context.loaders.finding.clear(finding_id)
        redis_del_by_deps_soon(
            "remove_finding_evidence",
            finding_id=finding_id,
        )
        logs_utils.cloudwatch_log(
            info.context,
            (
                f"Security: Removed evidence in finding {finding_id}"
            ),  # pragma: no cover
        )
    finding_loader = info.context.loaders.finding
    finding = await finding_loader.load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)
