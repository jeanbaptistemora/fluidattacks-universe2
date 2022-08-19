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
from db_model.enums import (
    Notification,
    Source,
)
from db_model.findings.enums import (
    DraftRejectionReason,
)
from db_model.findings.types import (
    Finding,
)
from db_model.stakeholders.types import (
    Stakeholder,
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
    Optional,
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
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    reason: str,
    other: Optional[str] = None,
) -> SimplePayload:
    try:
        # Graphql returns optional string args as "None" instead of None
        other_reason: Optional[str] = other if other != str(None) else None

        finding_loader = info.context.loaders.finding
        user_info = await token_utils.get_jwt_content(info.context)
        reviewer_email = user_info["user_email"]
        await findings_domain.reject_draft(
            context=info.context,
            finding_id=finding_id,
            reason=DraftRejectionReason[reason],
            other=other_reason.strip() if other_reason else None,
            reviewer_email=reviewer_email,
        )
        redis_del_by_deps_soon(
            "reject_draft",
            finding_id=finding_id,
        )
        stakeholder: Stakeholder = await info.context.loaders.stakeholder.load(
            reviewer_email
        )
        if (
            requests_utils.get_source_new(info.context) != Source.MACHINE
            and Notification.NEW_DRAFT
            in stakeholder.notifications_preferences.email
        ):
            finding: Finding = await finding_loader.load(finding_id)
            schedule(
                findings_mail.send_mail_reject_draft(
                    info.context.loaders,
                    finding.id,
                    finding.title,
                    finding.group_name,
                    finding.hacker_email,
                    reviewer_email,
                )
            )
        logs_utils.cloudwatch_log(
            info.context, f"Security: Rejected draft {finding_id} successfully"
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context, f"Security: Attempted to reject draft {finding_id}"
        )
        raise
    return SimplePayload(success=True)
