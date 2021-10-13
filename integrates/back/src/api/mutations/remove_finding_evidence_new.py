from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimpleFindingPayload,
)
from db_model.findings.types import (
    Finding,
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
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, evidence_id: str, finding_id: str
) -> SimpleFindingPayload:
    try:
        await findings_domain.remove_evidence(
            info.context.loaders, evidence_id, finding_id
        )
        redis_del_by_deps_soon(
            "remove_finding_evidence",
            finding_id=finding_id,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Removed evidence in finding {finding_id} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to remove evidence in finding {finding_id}",
        )
        raise
    finding_loader = info.context.loaders.finding_new
    finding_loader.clear(finding_id)
    finding: Finding = await finding_loader.load(finding_id)
    return SimpleFindingPayload(finding=finding, success=True)
