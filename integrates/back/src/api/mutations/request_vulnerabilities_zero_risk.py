from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
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
from typing import (
    List,
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
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    vulnerabilities: List[str],
) -> SimplePayload:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        success = await vulns_domain.request_vulnerabilities_zero_risk(
            loaders=info.context.loaders,
            vuln_ids=set(vulnerabilities),
            finding_id=finding_id,
            user_info=user_info,
            justification=justification,
        )
        email: str = user_info["user_email"]
        reattack_just = "Reattack cancelled due to zero risk request"
        treatment_just = "Treatment change cancelled due to zero risk request"
        finding_vulns_loader = info.context.loaders.finding_vulns_all_typed
        vulns_info: List[Vulnerability] = [
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
                and vuln.state.status != VulnerabilityStateStatus.CLOSED
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
        if success:
            if reattacked_vulns:
                await findings_domain.verify_vulnerabilities(
                    context=info.context,
                    finding_id=finding_id,
                    user_info=user_info,
                    justification=reattack_just,
                    open_vulns_ids=reattacked_vulns,
                    closed_vulns_ids=[],
                    vulns_to_close_from_file=[],
                )
            if treatment_changed_vulns:
                await vulns_domain.handle_vulnerabilities_acceptance(
                    loaders=info.context.loaders,
                    accepted_vulns=[],
                    finding_id=finding_id,
                    justification=treatment_just,
                    rejected_vulns=treatment_changed_vulns,
                    user_email=email,
                )
            await redis_del_by_deps(
                "request_vulnerabilities_zero_risk",
                finding_id=finding_id,
            )
            await update_unreliable_indicators_by_deps(
                EntityDependency.request_vulnerabilities_zero_risk,
                finding_id=finding_id,
            )
            logs_utils.cloudwatch_log(
                info.context,
                "Security: Requested a zero risk vuln in finding "
                f"{finding_id}",
            )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to request a zero risk vuln in finding "
            f"{finding_id}",
        )
        raise
    return SimplePayload(success=success)
