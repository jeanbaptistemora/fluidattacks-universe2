from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
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


@MUTATION.field("requestVulnerabilitiesZeroRisk")
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
    justification: str,
    vulnerabilities: list[str],
) -> SimplePayload:
    try:
        loaders: Dataloaders = info.context.loaders
        user_info = await sessions_domain.get_jwt_content(info.context)
        await vulns_domain.request_vulnerabilities_zero_risk(
            loaders=loaders,
            vuln_ids=set(vulnerabilities),
            finding_id=finding_id,
            user_info=user_info,
            justification=justification,
        )
        email: str = user_info["user_email"]
        reattack_just = "Reattack cancelled due to zero risk request"
        treatment_just = "Treatment change cancelled due to zero risk request"
        finding_vulns_loader = loaders.finding_vulnerabilities_all
        vulns_info: list[Vulnerability] = [
            vuln
            for vuln in await finding_vulns_loader.load(finding_id)
            if vuln.id in vulnerabilities
        ]
        reattacked_vulns = [
            vuln.id
            for vuln in vulns_info
            if (
                vuln.verification
                and vuln.verification.status
                == VulnerabilityVerificationStatus.REQUESTED
                and vuln.state.status is VulnerabilityStateStatus.VULNERABLE
            )
        ]
        treatment_changed_vulns = [
            vuln.id
            for vuln in vulns_info
            if (
                vuln.treatment
                and vuln.treatment.acceptance_status
                == VulnerabilityAcceptanceStatus.SUBMITTED
            )
        ]
        if reattacked_vulns:
            loaders.finding_vulnerabilities_all.clear(finding_id)
            for vuln_id in vulnerabilities:
                loaders.vulnerability.clear(vuln_id)
            await findings_domain.verify_vulnerabilities(
                context=info.context,
                finding_id=finding_id,
                user_info=user_info,
                justification=reattack_just,
                open_vulns_ids=reattacked_vulns,
                closed_vulns_ids=[],
                vulns_to_close_from_file=[],
                loaders=loaders,
            )
        if treatment_changed_vulns:
            loaders.finding_vulnerabilities_all.clear(finding_id)
            for vuln_id in vulnerabilities:
                loaders.vulnerability.clear(vuln_id)
            await vulns_domain.handle_vulnerabilities_acceptance(
                loaders=loaders,
                accepted_vulns=[],
                finding_id=finding_id,
                justification=treatment_just,
                rejected_vulns=treatment_changed_vulns,
                user_email=email,
            )
        await update_unreliable_indicators_by_deps(
            EntityDependency.request_vulnerabilities_zero_risk,
            finding_ids=[finding_id],
            vulnerability_ids=vulnerabilities,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Requested a zero risk vuln in finding {finding_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to request a zero risk vuln in finding "
            f"{finding_id}",
        )
        raise

    return SimplePayload(success=True)
