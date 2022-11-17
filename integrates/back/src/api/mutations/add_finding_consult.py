# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    AddConsultPayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidDraftConsult,
    PermissionDenied,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
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
from findings import (
    domain as findings_domain,
)
from graphql import (
    GraphQLError,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
    logs as logs_utils,
    validations as validations_utils,
)
from sessions import (
    domain as sessions_domain,
)
from time import (
    time,
)
from typing import (
    Any,
)


async def _add_finding_consult(
    info: GraphQLResolveInfo, **parameters: Any
) -> str:
    validations_utils.validate_fields([parameters["content"]])
    param_type = parameters.get("type", "").lower()
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    finding_id = str(parameters.get("finding_id"))
    finding: Finding = await info.context.loaders.finding.load(finding_id)
    group_name: str = finding.group_name
    is_finding_released = bool(finding.approval)
    content = parameters["content"]
    if param_type == "consult" and not is_finding_released:
        raise InvalidDraftConsult()

    comment_id = str(round(time() * 1000))
    current_time = datetime_utils.get_as_utc_iso_format(
        datetime_utils.get_now()
    )
    comment_data = FindingComment(
        finding_id=finding_id,
        id=comment_id,
        comment_type=CommentType.OBSERVATION
        if param_type != "consult"
        else CommentType.COMMENT,
        parent_id=str(parameters.get("parent_comment")),
        creation_date=current_time,
        full_name=" ".join([user_data["first_name"], user_data["last_name"]]),
        content=content,
        email=user_email,
    )
    try:
        await findings_domain.add_comment(
            info, user_email, comment_data, finding_id, group_name
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Unauthorized role attempted to add observation",
        )
        raise GraphQLError("Access denied") from None

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added comment in finding {finding_id} successfully",
    )
    return comment_id


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, **parameters: Any
) -> AddConsultPayload:
    comment_id = await _add_finding_consult(info, **parameters)
    return AddConsultPayload(success=True, comment_id=comment_id)
