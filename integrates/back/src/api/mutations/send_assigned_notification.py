from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
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
)
from sessions import (
    domain as sessions_domain,
)
from vulnerabilities.domain.treatment import (
    validate_and_send_notification_request,
)


@MUTATION.field("sendAssignedNotification")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerabilities: list[str],
    **_kwargs: None,
) -> SimplePayload:
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    responsible: str = user_info["user_email"]
    loaders: Dataloaders = info.context.loaders
    try:
        finding = await findings_domain.get_finding(loaders, finding_id)
        await validate_and_send_notification_request(
            loaders=loaders,
            finding=finding,
            responsible=responsible,
            vulnerabilities=vulnerabilities,
        )
        logs_utils.cloudwatch_log(
            info.context,
            (
                "Security: Notifications pertaining to a change in "
                f"treatment of vulns in finding {finding_id} have "
                "been successfully sent"
            ),
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to send notifications pertaining to a change "
            f"in treatment of vulns in finding {finding_id} ",
        )
        raise

    return SimplePayload(success=True)
