from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
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
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    evidence_id: str,
    description: str,
) -> SimplePayload:
    try:
        await findings_domain.update_evidence_description(
            info.context.loaders, finding_id, evidence_id, description
        )
        redis_del_by_deps_soon(
            "update_evidence_description",
            finding_id=finding_id,
        )
        logs_utils.cloudwatch_log(
            info.context,
            (
                "Security: Evidence description successfully updated in "
                f"finding {finding_id}"
            ),
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            (
                "Security: Attempted to update evidence description in "
                f"{finding_id}"
            ),
        )
        raise
    return SimplePayload(success=True)
