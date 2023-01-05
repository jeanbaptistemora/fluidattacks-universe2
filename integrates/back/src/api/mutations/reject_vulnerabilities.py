from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_report_vulnerabilities,
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
    justification: str,
    **kwargs: Any,
) -> SimplePayload:
    try:
        user_data = await sessions_domain.get_jwt_content(info.context)
        stakeholder_email = user_data["user_email"]
        await vulns_domain.reject_vulnerabilities(
            loaders=info.context.loaders,
            vuln_ids=set(vulnerabilities),
            finding_id=finding_id,
            modified_by=stakeholder_email,
            justification=VulnerabilityStateReason[justification],
            other_justification=kwargs.get("other_justification"),
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.reject_vulnerabilities,
            finding_ids=[finding_id],
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
