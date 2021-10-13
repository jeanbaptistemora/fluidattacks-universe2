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
    SimplePayload,
)
from db_model.findings.enums import (
    FindingStateJustification,
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
from mailer import (
    findings as findings_mail,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
) -> SimplePayload:
    try:
        finding_loader = info.context.loaders.finding_new
        user_info = await token_utils.get_jwt_content(info.context)
        user_email = user_info["user_email"]
        state_justification = FindingStateJustification[justification]
        finding: Finding = await finding_loader.load(finding_id)
        await findings_domain.remove_finding(
            info.context,
            finding_id,
            state_justification,
            user_email,
        )
        redis_del_by_deps_soon(
            "remove_finding",
            finding_id=finding_id,
            group_name=finding.group_name,
        )
        schedule(
            findings_mail.send_mail_remove_finding(
                finding.id,
                finding.title,
                finding.group_name,
                finding.hacker_email,
                state_justification,
            )
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Removed finding {finding_id} successfully ",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context, f"Security: Attempted to remove finding {finding_id}"
        )
        raise
    return SimplePayload(success=True)
