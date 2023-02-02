from aioextensions import (
    schedule,
)
from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.enums import (
    StateRemovalJustification,
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
    require_finding_access,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
) -> SimplePayload:
    try:
        loaders: Dataloaders = info.context.loaders
        user_info = await sessions_domain.get_jwt_content(info.context)
        user_email = user_info["user_email"]
        state_justification = StateRemovalJustification[justification]
        finding = await findings_domain.get_finding(loaders, finding_id)
        source = requests_utils.get_source_new(info.context)
        await findings_domain.remove_finding(
            loaders=loaders,
            email=user_email,
            finding_id=finding_id,
            justification=state_justification,
            source=source,
        )
        schedule(
            findings_mail.send_mail_remove_finding(
                loaders,
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
