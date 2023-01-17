from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
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
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
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
)
from sessions import (
    domain as sessions_domain,
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
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerability_id: str,
    **parameters: str,
) -> SimplePayload:
    try:
        user_info = await sessions_domain.get_jwt_content(info.context)
        user_email: str = user_info["user_email"]
        loaders: Dataloaders = info.context.loaders
        finding: Finding = await loaders.finding.load(finding_id)
        group_name: str = finding.group_name
        severity_score = findings_domain.get_severity_score(finding.severity)

        await vulns_domain.update_vulnerabilities_treatment(
            loaders=loaders,
            finding_id=finding_id,
            updated_values=parameters,
            finding_severity=severity_score,
            user_email=user_email,
            vulnerability_id=vulnerability_id,
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

        justification: str = parameters["justification"]
        assigned: str = parameters.get("assigned", "")
        if (
            parameters.get("treatment")
            == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ):
            await vulns_domain.send_treatment_report_mail(
                loaders=loaders,
                modified_by=user_email,
                justification=justification,
                vulnerability_id=vulnerability_id,
            )

        # Clearing cache
        loaders.finding_vulnerabilities_all.clear(finding_id)

        await vulns_domain.send_treatment_change_mail(
            loaders=loaders,
            assigned=assigned,
            finding_id=finding_id,
            finding_title=finding.title,
            group_name=group_name,
            justification=justification,
            min_date=datetime.now(timezone.utc) - timedelta(days=1),
            modified_by=user_email,
        )

    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to update vulnerabilities treatment in "
            f"finding {finding_id}",
        )
        raise

    return SimplePayload(success=True)
