from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from aioextensions import (
    schedule,
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
from db_model.enums import (
    Notification,
    Source,
)
from db_model.findings.enums import (
    DraftRejectionReason,
)
from db_model.findings.types import (
    DraftRejection,
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
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders.domain import (
    get_stakeholder,
)
from typing import (
    Optional,
)


@MUTATION.field("rejectDraft")
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
    reasons: list[str],
    other: Optional[str] = None,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    try:
        # Graphql returns optional string args as "None" instead of None
        other_reason: Optional[str] = other if other != str(None) else None
        user_info = await sessions_domain.get_jwt_content(info.context)
        source = requests_utils.get_source_new(info.context)
        rejection: DraftRejection = await findings_domain.reject_draft(
            loaders=loaders,
            finding_id=finding_id,
            reasons={DraftRejectionReason[reason] for reason in reasons},
            other=other_reason.strip() if other_reason else None,
            reviewer_email=user_info["user_email"],
            source=source,
        )
        stakeholder = await get_stakeholder(loaders, rejection.rejected_by)
        if (
            source != Source.MACHINE
            and Notification.NEW_DRAFT
            in stakeholder.state.notifications_preferences.email
        ):
            finding = await findings_domain.get_finding(loaders, finding_id)
            schedule(
                findings_mail.send_mail_reject_draft(
                    loaders=loaders,
                    draft_id=finding.id,
                    draft_title=finding.title,
                    group_name=finding.group_name,
                    discoverer_email=finding.hacker_email,
                    rejection=rejection,
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
