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
    token as token_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
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
    """Resolve reject_vulnerabilities_zero_risk mutation."""
    user_info = await token_utils.get_jwt_content(info.context)
    success = await vulns_domain.reject_vulnerabilities_zero_risk(
        finding_id, user_info, justification, vulnerabilities
    )
    if success:
        redis_del_by_deps_soon(
            "reject_vulnerabilities_zero_risk", finding_id=finding_id
        )
        logs_utils.cloudwatch_log(
            info.context,
            (
                "Security: rejected a zero risk vuln "
                f"in finding_id: {finding_id}"
            ),  # pragma: no cover
        )
    return SimplePayloadType(success=success)
