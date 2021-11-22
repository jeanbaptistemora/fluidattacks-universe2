from api import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
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
    get_key_or_fallback,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
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


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayloadType:
    try:
        finding_id = kwargs["finding_id"]
        finding_loader = info.context.loaders.finding
        finding: Finding = await finding_loader.load(finding_id)
        user_info = await token_utils.get_jwt_content(info.context)
        success = await findings_domain.verify_vulnerabilities(
            context=info.context,
            finding_id=finding_id,
            user_info=user_info,
            justification=kwargs.get("justification", ""),
            open_vulns_ids=get_key_or_fallback(
                kwargs, "open_vulnerabilities", "open_vulns", []
            ),
            closed_vulns_ids=get_key_or_fallback(
                kwargs, "closed_vulnerabilities", "closed_vulns", []
            ),
            vulns_to_close_from_file=[],
        )
        if success:
            redis_del_by_deps_soon(
                "verify_vulnerabilities_request",
                finding_id=finding.id,
                group_name=finding.group_name,
            )
            await update_unreliable_indicators_by_deps(
                EntityDependency.verify_vulnerabilities_request,
                finding_id=finding.id,
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
    return SimplePayloadType(success=success)
