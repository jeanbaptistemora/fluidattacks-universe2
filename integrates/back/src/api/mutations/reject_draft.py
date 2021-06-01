from aioextensions import (
    schedule,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_finding_access,
    require_integrates,
    require_login,
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
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, finding_id: str
) -> SimplePayloadType:
    user_info = await token_utils.get_jwt_content(info.context)
    reviewer_email = user_info["user_email"]
    success = await findings_domain.reject_draft(
        info.context, finding_id, reviewer_email
    )
    if success:
        redis_del_by_deps_soon("reject_draft", finding_id=finding_id)
        if requests_utils.get_source(info.context) != "skims":
            finding_loader = info.context.loaders.finding
            finding = await finding_loader.load(finding_id)
            schedule(
                findings_mail.send_mail_reject_draft(
                    info.context.loaders,
                    finding_id,
                    str(finding.get("title", "")),
                    str(finding.get("project_name", "")),
                    str(finding.get("analyst", "")),
                    reviewer_email,
                )
            )
        logs_utils.cloudwatch_log(
            info.context, f"Security: Draft {finding_id} rejected successfully"
        )
    else:
        logs_utils.cloudwatch_log(
            info.context, f"Security: Attempted to reject draft {finding_id}"
        )

    return SimplePayloadType(success=success)
