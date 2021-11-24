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
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    List,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerabilities import (
    domain as vulns_domain,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    vulnerabilities: List[str],
) -> SimplePayload:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        success = await vulns_domain.reject_vulnerabilities_zero_risk(
            loaders=info.context.loaders,
            vuln_ids=set(vulnerabilities),
            finding_id=finding_id,
            user_info=user_info,
            justification=justification,
        )
        if success:
            redis_del_by_deps_soon(
                "reject_vulnerabilities_zero_risk", finding_id=finding_id
            )
            await update_unreliable_indicators_by_deps(
                EntityDependency.reject_vulnerabilities_zero_risk,
                finding_id=finding_id,
            )
            logs_utils.cloudwatch_log(
                info.context,
                f"Security: Rejected a zero risk vuln in finding {finding_id}",
            )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to reject a zero risk vuln in finding "
            f"{finding_id}",
        )
        raise
    return SimplePayload(success=success)
