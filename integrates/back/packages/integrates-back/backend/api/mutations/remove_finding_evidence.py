
# Third party libraries
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.dal.helpers.redis import redis_del_by_deps_soon
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.typing import SimpleFindingPayload as SimpleFindingPayloadType
from findings import domain as findings_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    evidence_id: str,
    finding_id: str
) -> SimpleFindingPayloadType:
    """Resolve remove_evidence mutation."""
    success = await findings_domain.remove_evidence(evidence_id, finding_id)

    if success:
        info.context.loaders.finding.clear(finding_id)
        redis_del_by_deps_soon(
            'remove_finding_evidence',
            finding_id=finding_id,
        )
        util.cloudwatch_log(
            info.context,
            ('Security: Removed evidence '
             f'in finding {finding_id}')  # pragma: no cover
        )
    finding_loader = info.context.loaders.finding
    finding = await finding_loader.load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)
