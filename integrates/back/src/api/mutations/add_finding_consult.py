from aioextensions import (
    schedule,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    PermissionDenied,
)
from custom_types import (
    AddConsultPayload as AddConsultPayloadType,
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
from mailer import (
    findings as findings_mail,
)
from newutils import (
    datetime as datetime_utils,
    logs as logs_utils,
    token as token_utils,
    validations as validations_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from subscriptions.domain import (
    get_users_subscribed_to_consult,
)
from time import (
    time,
)
from typing import (
    Any,
    Tuple,
)


async def send_finding_consult_mail(
    *,
    info: GraphQLResolveInfo,
    comment_data: FindingComment,
    user_email: str,
    group_name: str,
    finding_id: str,
    finding_title: str,
    is_finding_released: bool,
) -> None:
    await findings_mail.send_mail_comment(
        loaders=info.context.loaders,
        comment_data=comment_data,
        user_mail=user_email,
        finding_id=finding_id,
        finding_title=finding_title,
        recipients=await get_users_subscribed_to_consult(
            loaders=info.context.loaders,
            group_name=group_name,
            comment_type=comment_data.comment_type,
            is_finding_released=is_finding_released,
        ),
        group_name=group_name,
        is_finding_released=is_finding_released,
    )


async def _add_finding_consult(
    info: GraphQLResolveInfo, **parameters: Any
) -> Tuple[bool, str]:
    validations_utils.validate_fields([parameters["content"]])
    param_type = parameters.get("type", "").lower()
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    finding_id = str(parameters.get("finding_id"))
    finding: Finding = await info.context.loaders.finding.load(finding_id)
    group_name: str = finding.group_name
    is_finding_released = bool(finding.approval)
    content = parameters["content"]
    comment_id = str(round(time() * 1000))
    current_time = datetime_utils.get_as_utc_iso_format(
        datetime_utils.get_now()
    )
    comment_data = FindingComment(
        finding_id=finding_id,
        id=comment_id,
        comment_type=param_type if param_type != "consult" else "comment",
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

    redis_del_by_deps_soon("add_finding_consult", finding_id=finding_id)
    if content.strip() not in {"#external", "#internal"}:
        schedule(
            send_finding_consult_mail(
                info=info,
                comment_data=comment_data,
                user_email=user_email,
                group_name=group_name,
                finding_id=finding_id,
                finding_title=finding.title,
                is_finding_released=is_finding_released,
            )
        )

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added comment in finding {finding_id} successfully",
    )

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Attempted to add comment in finding {finding_id}",
    )
    return True, comment_id


async def add_finding_consult(
    info: GraphQLResolveInfo, **parameters: Any
) -> Tuple[bool, str]:
    return await _add_finding_consult(info, **parameters)


async def add_finding_observation(
    info: GraphQLResolveInfo, **parameters: Any
) -> Tuple[bool, str]:
    return await _add_finding_consult(info, **parameters)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, **parameters: Any
) -> AddConsultPayloadType:
    success = False
    if parameters.get("type", "").lower() == "observation":
        success, comment_id = await add_finding_observation(info, **parameters)
    else:
        success, comment_id = await add_finding_consult(info, **parameters)

    return AddConsultPayloadType(success=success, comment_id=comment_id)
