from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
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
from newutils.utils import (
    duplicate_dict_keys,
)
from organizations import (
    domain as orgs_domain,
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
        loaders: Dataloaders = info.context.loaders
        finding: Finding = await loaders.finding.load(finding_id)
        group_name: str = finding.group_name
        group: Group = await loaders.group_typed.load(group_name)
        organization_id: str = await orgs_domain.get_id_by_name(
            group.organization_name
        )
        severity_score = findings_domain.get_severity_score(finding.severity)
        if parameters.get("treatment_manager"):
            parameters = duplicate_dict_keys(
                parameters, "treatment_manager", "assigned"
            )
            del parameters["treatment_manager"]
        success: bool = await vulns_domain.update_vulnerabilities_treatment(
            loaders=loaders,
            finding_id=finding_id,
            updated_values=parameters,
            organization_id=organization_id,
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
                finding_ids=[finding_id],
                vulnerability_ids=[vulnerability_id],
            )
            logs_utils.cloudwatch_log(
                info.context,
                "Security: Vulnerabilities treatment successfully updated in "
                f"finding {finding_id}",
            )
        await vulns_domain.send_treatment_change_mail(
            loaders,
            finding_id,
            finding.title,
            group_name,
            datetime.now(timezone.utc) - timedelta(days=1),
            user_email,
        )

    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to update vulnerabilities treatment in "
            f"finding {finding_id}",
        )
        raise

    return SimplePayload(success=success)
