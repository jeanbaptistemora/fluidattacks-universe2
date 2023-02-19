from .payloads.types import (
    SimplePayload,
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


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_report_vulnerabilities,
    require_finding_access,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, finding_id: str
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    try:
        user_info = await sessions_domain.get_jwt_content(info.context)
        user_email = user_info["user_email"]
        await findings_domain.submit_draft(
            loaders,
            finding_id,
            user_email,
            requests_utils.get_source_new(info.context),
        )
        finding = await findings_domain.get_finding(loaders, finding_id)
        schedule(
            findings_mail.send_mail_new_draft(
                loaders,
                finding.id,
                finding.title,
                finding.group_name,
                user_email,
            )
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Submitted draft {finding_id} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context, f"Security: Attempted to submit draft {finding_id}"
        )
        raise

    return SimplePayload(success=True)
