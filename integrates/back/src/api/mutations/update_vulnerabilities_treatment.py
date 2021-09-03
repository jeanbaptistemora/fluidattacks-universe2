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
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from vulnerabilities import (
    domain as vulns_domain,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerability_id: str,
    **parameters: str,
) -> SimplePayload:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    finding_loader = info.context.loaders.finding
    finding_data = await finding_loader.load(finding_id)
    group_name = get_key_or_fallback(finding_data)
    group_loader = info.context.loaders.group
    group = await group_loader.load(group_name)
    success: bool = await vulns_domain.update_vulnerabilities_treatment(
        context=info.context.loaders,
        finding_id=finding_id,
        updated_values=parameters,
        organization_id=group["organization"],
        finding_severity=float(finding_data["severity_score"]),
        user_email=user_email,
        vulnerability_id=vulnerability_id,
        group_name=group_name,
    )
    if success:
        await redis_del_by_deps(
            "update_vulnerabilities_treatment",
            finding_id=finding_id,
            group_name=group_name,
        )

    return SimplePayload(success=success)
