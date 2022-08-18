from aioextensions import (
    schedule,
)
from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    ApproveDraftPayload,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_asm,
    require_finding_access,
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
    requests as requests_utils,
    token as token_utils,
)
from newutils.datetime import (
    convert_from_iso_str,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    Any,
    Tuple,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)


@convert_kwargs_to_snake_case
@rename_kwargs({"draft_id": "finding_id"})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_report_vulnerabilities,
    require_finding_access,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, finding_id: str
) -> ApproveDraftPayload:
    try:
        loaders: Dataloaders = info.context.loaders
        finding: Finding = await loaders.finding.load(finding_id)
        vulnerabilities: Tuple[
            Vulnerability, ...
        ] = await loaders.finding_vulnerabilities_all.load(finding_id)
        severity_score: Decimal = findings_domain.get_severity_score(
            finding.severity
        )
        severity_level: str = findings_domain.get_severity_level(
            severity_score
        )
        group_name = finding.group_name
        group_findings: Tuple[
            Finding, ...
        ] = await loaders.group_findings.load(group_name)
        user_info = await token_utils.get_jwt_content(info.context)
        user_email = user_info["user_email"]
        approval_date = await findings_domain.approve_draft(
            info.context.loaders,
            finding_id,
            user_email,
            requests_utils.get_source_new(info.context),
        )
        redis_del_by_deps_soon(
            "approve_draft",
            finding_id=finding_id,
            group_name=group_name,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Approved draft {finding_id} in {group_name} "
            "group successfully",
        )
        # Update indicators in two steps as new vulns report dates are needed
        await update_unreliable_indicators_by_deps(
            EntityDependency.approve_draft,
            finding_ids=[],
            vulnerability_ids=[vuln.id for vuln in vulnerabilities],
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.approve_draft,
            finding_ids=[finding_id],
            vulnerability_ids=[],
        )

        vulns_props: dict[str, Any] = {
            vuln.id: {
                "Location": vuln.where,
            }
            for vuln in vulnerabilities
            if vuln.state.status == VulnerabilityStateStatus.OPEN
        }

        if severity_score >= 7.0 or not group_findings:
            schedule(
                findings_mail.send_mail_vulnerability_report(
                    loaders=loaders,
                    group_name=group_name,
                    finding_title=finding.title,
                    finding_id=finding_id,
                    vulnerabilities_properties=vulns_props,
                    severity_score=severity_score,
                    severity_level=severity_level,
                )
            )

    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context, f"Security: Attempted to approve draft {finding_id}"
        )
        raise
    return ApproveDraftPayload(
        release_date=convert_from_iso_str(approval_date), success=True
    )
