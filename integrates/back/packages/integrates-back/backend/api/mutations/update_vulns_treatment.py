# Third party libraries
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from backend.typing import SimplePayload
from redis_cluster.operations import redis_del_by_deps
from vulnerabilities import domain as vulns_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerability_id: str,
    **parameters: str,
) -> SimplePayload:
    user_info = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']
    finding_loader = info.context.loaders.finding
    group_loader = info.context.loaders.group_all
    finding_data = await finding_loader.load(finding_id)
    group_name: str = finding_data['project_name']
    group = await group_loader.load(group_name)
    success: bool = await vulns_domain.update_vulns_treatment(
        context=info.context.loaders,
        finding_id=finding_id,
        updated_values=parameters,
        organization_id=group['organization'],
        finding_severity=float(finding_data['severity_score']),
        user_email=user_email,
        vulnerability_id=vulnerability_id,
        group_name=group_name,
    )
    if success:
        await redis_del_by_deps(
            'update_vulns_treatment',
            finding_id=finding_id,
            group_name=group_name,
        )

    return SimplePayload(success=success)
