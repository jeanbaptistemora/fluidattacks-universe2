from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from typing import (
    List,
)
from vulnerabilities.domain.treatment import (
    validate_and_send_notification_request,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerabilities: List[str],
    **_parameters: str,
) -> SimplePayload:
    try:
        finding_loader = info.context.loaders.finding
        finding: Finding = await finding_loader.load(finding_id)
        success: bool = await validate_and_send_notification_request(
            loaders=info.context.loaders,
            finding=finding,
            vulnerabilities=vulnerabilities,
        )
        if success:
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

    return SimplePayload(success=success)
