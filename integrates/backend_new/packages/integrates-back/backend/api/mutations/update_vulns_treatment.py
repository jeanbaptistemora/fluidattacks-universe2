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
from backend.exceptions import MaxNumberOfVulns
from backend.domain.organization import get_id_for_group
from backend.domain.vulnerability import update_vulns_treatment
from backend.typing import SimplePayload
# Constants
MAX_VULNS = 100


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
    vulnerabilities: List[str],
    **parameters: str,
) -> SimplePayload:
    if len(vulnerabilities) > MAX_VULNS:
        raise MaxNumberOfVulns(MAX_VULNS)
    user_info = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']
    finding_data = await info.context.loaders['finding'].load(finding_id)
    group_name: str = finding_data['project_name']
    success: bool = await update_vulns_treatment(
        finding_id=finding_id,
        updated_values=parameters,
        organization_name=await get_id_for_group(group_name),
        finding_severity=float(finding_data['severity_score']),
        user_email=user_email,
        vuln_ids=vulnerabilities,
        group_name=group_name,
    )
    if success:
        util.queue_cache_invalidation(
            f'vuln*{finding_id}',
            f'vuln*{group_name}',
            *[f'vuln*{vuln}' for vuln in vulnerabilities]
        )
        util.forces_trigger_deployment(group_name)

    return SimplePayload(success=success)
