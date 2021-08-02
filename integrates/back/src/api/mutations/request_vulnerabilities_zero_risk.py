from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
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
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from typing import (
    List,
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
) -> SimplePayloadType:
    """Resolve request_vulnerabilities_zero_risk mutation."""
    success = await vulns_domain.request_vulnerabilities_zero_risk(
        info, finding_id, justification, vulnerabilities
    )
    if success:
        info.context.loaders.finding.clear(finding_id)
        info.context.loaders.finding_vulns_all.clear(finding_id)
        for vuln_id in vulnerabilities:
            info.context.loaders.vulnerability.clear(vuln_id)
        await redis_del_by_deps(
            "request_vulnerabilities_zero_risk",
            finding_id=finding_id,
        )
        logs_utils.cloudwatch_log(
            info.context,
            (
                "Security: Requested a zero risk vuln "
                f"in finding_id: {finding_id}"
            ),  # pragma: no cover
        )
    return SimplePayloadType(success=success)
