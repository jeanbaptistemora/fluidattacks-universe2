from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from aioextensions import (
    schedule,
)
from api.types import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
)
from decimal import (
    Decimal,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_report_vulnerabilities,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from mailer import (
    findings as findings_mail,
)
from newutils import (
    logs as logs_utils,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
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
from vulnerabilities.domain.core import (
    get_by_finding_and_vuln_ids,
)


@MUTATION.field("rejectVulnerabilities")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    require_report_vulnerabilities,
    enforce_group_level_auth_async,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerabilities: list[str],
    reasons: list[str],
    **kwargs: Any,
) -> SimplePayload:
    try:
        loaders: Dataloaders = info.context.loaders
        user_data = await sessions_domain.get_jwt_content(info.context)
        stakeholder_email = user_data["user_email"]
        rejection_reasons = {
            VulnerabilityStateReason[reason] for reason in reasons
        }
        await vulns_domain.reject_vulnerabilities(
            loaders=loaders,
            vuln_ids=set(vulnerabilities),
            finding_id=finding_id,
            modified_by=stakeholder_email,
            reasons=rejection_reasons,
            other_reason=kwargs.get("other_reason"),
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.reject_vulnerabilities,
            finding_ids=[finding_id],
        )
        finding = await findings_domain.get_finding(loaders, finding_id)
        severity_score: Decimal = findings_domain.get_severity_score(
            finding.severity
        )
        severity_level: str = findings_domain.get_severity_level(
            severity_score
        )
        vulnerabilities_properties: dict[
            str, Any
        ] = await findings_domain.vulns_properties(
            loaders,
            finding_id,
            list(
                await get_by_finding_and_vuln_ids(
                    loaders, finding_id, set(vulnerabilities)
                )
            ),
        )
        schedule(
            findings_mail.send_mail_reject_vulnerability(
                loaders=loaders,
                finding=finding,
                stakeholder_email=stakeholder_email,
                rejection_reasons=rejection_reasons,
                other_reason=kwargs.get("other_reason"),
                vulnerabilities_properties=vulnerabilities_properties,
                severity_score=severity_score,
                severity_level=severity_level,
            )
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Rejected vulnerabilities in finding {finding_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to reject vulnerabilities in finding "
            f"{finding_id}",
        )
        raise

    return SimplePayload(success=True)
