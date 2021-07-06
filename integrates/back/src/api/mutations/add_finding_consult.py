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
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
    require_squad,
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
)
from newutils.utils import (
    resolve_kwargs,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from time import (
    time,
)
from typing import (
    Any,
    Tuple,
)


async def _add_finding_consult(
    info: GraphQLResolveInfo, **parameters: Any
) -> Tuple[bool, int]:
    param_type = parameters.get("type", "").lower()
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    finding_id = str(parameters.get("finding_id"))
    finding_loader = info.context.loaders.finding
    finding = await finding_loader.load(finding_id)
    group = resolve_kwargs(finding)
    content = parameters["content"]

    user_email = user_data["user_email"]
    comment_id = int(round(time() * 1000))
    current_time = datetime_utils.get_as_str(datetime_utils.get_now())
    comment_data = {
        "user_id": comment_id,
        "comment_type": param_type if param_type != "consult" else "comment",
        "content": content,
        "fullname": " ".join(
            [user_data["first_name"], user_data["last_name"]]
        ),
        "parent": parameters.get("parent"),
        "created": current_time,
        "modified": current_time,
    }
    try:
        success = await findings_domain.add_comment(
            info, user_email, comment_data, finding_id, group
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Unauthorized role attempted to add observation",
        )
        raise GraphQLError("Access denied")

    if success:
        redis_del_by_deps_soon("add_finding_consult", finding_id=finding_id)
        if content.strip() not in {"#external", "#internal"}:
            schedule(
                findings_mail.send_mail_comment(
                    info.context.loaders, comment_data, user_email, finding
                )
            )

        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added comment in finding {finding_id} successfully",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add comment in finding {finding_id}",
        )
    return success, comment_id


@require_squad
async def add_finding_consult(
    info: GraphQLResolveInfo, **parameters: Any
) -> Tuple[bool, int]:
    return await _add_finding_consult(info, **parameters)


async def add_finding_observation(
    info: GraphQLResolveInfo, **parameters: Any
) -> Tuple[bool, int]:
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

    return AddConsultPayloadType(success=success, comment_id=str(comment_id))
