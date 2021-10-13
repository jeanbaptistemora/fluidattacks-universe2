from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps,
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
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerability_id: str,
    **parameters: str,
) -> SimplePayload:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        user_email: str = user_info["user_email"]
        finding_new_loader = info.context.loaders.finding_new
        finding: Finding = await finding_new_loader.load(finding_id)
        group_name: str = finding.group_name
        group_loader = info.context.loaders.group
        group = await group_loader.load(group_name)
        severity_score = findings_domain.get_severity_score(finding.severity)
        success: bool = await vulns_domain.update_vulnerabilities_treatment(
            loaders=info.context.loaders,
            finding_id=finding_id,
            updated_values=parameters,
            organization_id=group["organization"],
            finding_severity=float(severity_score),
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
            await update_unreliable_indicators_by_deps(
                EntityDependency.update_vulnerabilities_treatment,
                finding_id=finding_id,
            )
            logs_utils.cloudwatch_log(
                info.context,
                "Security: Vulnerabilities treatment successfully updated in "
                f"finding {finding_id}",
            )

    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to update vulnerabilities treatment in "
            f"finding {finding_id}",
        )
        raise

    return SimplePayload(success=success)
