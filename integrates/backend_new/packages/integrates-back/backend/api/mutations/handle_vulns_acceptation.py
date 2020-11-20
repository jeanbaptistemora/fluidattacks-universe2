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
    require_integrates,
    require_login,
)
from backend.domain.vulnerability import handle_vulns_acceptation
from backend.typing import SimplePayload


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    accepted_vulns: List[str],
    rejected_vulns: List[str],
) -> SimplePayload:
    user_info = await util.get_jwt_content(info.context)
    email: str = user_info['user_email']
    finding = await info.context.loaders['finding'].load(finding_id)
    group_name: str = finding['project_name']
    success: bool = await handle_vulns_acceptation(
        accepted_vulns=accepted_vulns,
        finding_id=finding_id,
        justification=justification,
        rejected_vulns=rejected_vulns,
        user_email=email,
    )
    if success:
        util.queue_cache_invalidation(
            f'vuln*{finding_id}',
            f'vuln*{group_name}',
            *[f'vuln*{vuln}' for vuln in accepted_vulns + rejected_vulns]
        )
        util.forces_trigger_deployment(group_name)

    return SimplePayload(success=success)
