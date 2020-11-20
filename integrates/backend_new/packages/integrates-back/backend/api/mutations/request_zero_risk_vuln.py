# Standard
from typing import List

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from backend.domain import vulnerability as vuln_domain
from backend.typing import SimplePayload as SimplePayloadType


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
    vulnerabilities: List[str]
) -> SimplePayloadType:
    """Resolve request_zero_risk_vuln mutation."""
    success = await vuln_domain.request_zero_risk_vulnerabilities(
        info,
        finding_id,
        justification,
        vulnerabilities
    )
    if success:
        attrs_to_clean = {
            'finding': finding_id,
            'zero_risk': finding_id,
        }
        to_clean = util.format_cache_keys_pattern(attrs_to_clean)
        util.queue_cache_invalidation(*to_clean)
        util.cloudwatch_log(
            info.context,
            ('Security: Requested a zero risk vuln '
             f'in finding_id: {finding_id}')  # pragma: no cover
        )
    return SimplePayloadType(success=success)
