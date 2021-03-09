# Standard
from typing import List

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.dal.helpers.redis import (
    redis_del_by_deps_soon,
)
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from backend.domain import vulnerability as vuln_domain
from backend.typing import SimplePayload as SimplePayloadType


@convert_kwargs_to_snake_case  # type: ignore
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
    """Resolve reject_zero_risk_vuln mutation."""
    user_info = await util.get_jwt_content(info.context)
    success = await vuln_domain.reject_zero_risk_vulnerabilities(
        finding_id,
        user_info,
        justification,
        vulnerabilities
    )
    if success:
        redis_del_by_deps_soon('reject_zero_risk_vuln', finding_id=finding_id)
        util.cloudwatch_log(
            info.context,
            ('Security: rejected a zero risk vuln '
             f'in finding_id: {finding_id}')  # pragma: no cover
        )
    return SimplePayloadType(success=success)
