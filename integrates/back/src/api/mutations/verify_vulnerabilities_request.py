from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from api import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
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


@MUTATION.field("verifyVulnerabilitiesRequest")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_report_vulnerabilities,
    require_finding_access,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    open_vulnerabilities: list[str],
    closed_vulnerabilities: list[str],
) -> SimplePayload:
    try:
        user_info = await sessions_domain.get_jwt_content(info.context)

        await findings_domain.verify_vulnerabilities(
            context=info.context,
            finding_id=finding_id,
            user_info=user_info,
            justification=justification,
            open_vulns_ids=open_vulnerabilities,
            closed_vulns_ids=closed_vulnerabilities,
            vulns_to_close_from_file=[],
            loaders=info.context.loaders,
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.verify_vulnerabilities_request,
            finding_ids=[finding_id],
            vulnerability_ids=open_vulnerabilities + closed_vulnerabilities,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Verify vuln verification in finding {finding_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to verify vuln verification in finding "
            f"{finding_id}",
        )
        raise

    return SimplePayload(success=True)
