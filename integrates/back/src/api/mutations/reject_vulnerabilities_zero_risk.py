# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
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
    token as token_utils,
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
    justification: str,
    vulnerabilities: list[str],
) -> SimplePayload:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        await vulns_domain.reject_vulnerabilities_zero_risk(
            loaders=info.context.loaders,
            vuln_ids=set(vulnerabilities),
            finding_id=finding_id,
            user_info=user_info,
            justification=justification,
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.reject_vulnerabilities_zero_risk,
            finding_ids=[finding_id],
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Rejected a zero risk vuln in finding {finding_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to reject a zero risk vuln in finding "
            f"{finding_id}",
        )
        raise

    return SimplePayload(success=True)
