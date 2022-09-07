# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload as SimplePayloadType,
)
from ariadne import (
    convert_kwargs_to_snake_case,
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
    token as token_utils,
    validations,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    Any,
    List,
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
    require_report_vulnerabilities,
    require_finding_access,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    open_vulnerabilities: List[str],
    closed_vulnerabilities: List[str],
) -> SimplePayloadType:
    try:
        finding_loader = info.context.loaders.finding
        finding: Finding = await finding_loader.load(finding_id)
        user_info = await token_utils.get_jwt_content(info.context)
        # Validate justification length and vet characters in it
        validations.validate_field_length(
            justification,
            limit=10,
            is_greater_than_limit=True,
        )
        validations.validate_field_length(
            justification,
            limit=10000,
            is_greater_than_limit=False,
        )
        validations.validate_fields([justification])

        success = await findings_domain.verify_vulnerabilities(
            context=info.context,
            finding_id=finding_id,
            user_info=user_info,
            justification=justification,
            open_vulns_ids=open_vulnerabilities,
            closed_vulns_ids=closed_vulnerabilities,
            vulns_to_close_from_file=[],
            loaders=info.context.loaders,
        )
        if success:
            redis_del_by_deps_soon(
                "verify_vulnerabilities_request",
                finding_id=finding.id,
                group_name=finding.group_name,
            )
            await update_unreliable_indicators_by_deps(
                EntityDependency.verify_vulnerabilities_request,
                finding_ids=[finding_id],
                vulnerability_ids=open_vulnerabilities
                + closed_vulnerabilities,
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
