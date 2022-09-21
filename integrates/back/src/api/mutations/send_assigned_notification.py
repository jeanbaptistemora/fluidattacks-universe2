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
from dataloaders import (
    Dataloaders,
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
    token as token_utils,
)
from typing import (
    Dict,
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
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerabilities: list[str],
    **_kwargs: None,
) -> SimplePayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    responsible: str = user_info["user_email"]
    loaders: Dataloaders = info.context.loaders
    try:
        finding: Finding = await loaders.finding.load(finding_id)
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
