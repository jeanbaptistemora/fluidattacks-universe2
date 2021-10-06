from aioextensions import (
    schedule,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    AddConsultPayload as AddConsultPayloadType,
    Comment,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
    require_squad,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_comments import (
    domain as group_comments_domain,
)
from mailer import (
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
    logs as logs_utils,
    token as token_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from subscriptions.domain import (
    get_users_subscribed_to_consult,
)
import time
from typing import (
    Any,
)


async def send_group_consult_mail(
    *,
    info: GraphQLResolveInfo,
    comment_data: Comment,
    user_email: str,
    group_name: str,
) -> None:
    await groups_mail.send_mail_comment(
        loaders=info.context.loaders,
        comment_data=comment_data,
        user_mail=user_email,
        recipients=await get_users_subscribed_to_consult(
            group_name=group_name, comment_type="group"
        ),
        group_name=group_name,
    )


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_squad,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, **parameters: Any
) -> AddConsultPayloadType:
    group_name: str = get_key_or_fallback(parameters, fallback="").lower()
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    current_time = datetime_utils.get_as_str(datetime_utils.get_now())
    comment_id = int(round(time.time() * 1000))
    content = parameters["content"]
    comment_data = {
        "user_id": comment_id,
        "content": content,
        "created": current_time,
        "fullname": str.join(
            " ", [user_info["first_name"], user_info["last_name"]]
        ),
        "modified": current_time,
        "parent": parameters.get("parent"),
    }
    success = await group_comments_domain.add_comment(
        info, group_name, user_email, comment_data
    )
    if success:
        redis_del_by_deps_soon("add_group_consult", group_name=group_name)
        if content.strip() not in {"#external", "#internal"}:
            schedule(
                send_group_consult_mail(
                    info=info,
                    comment_data=comment_data,
                    user_email=user_email,
                    group_name=group_name,
                )
            )

        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added comment to {group_name} group successfully",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add a comment in {group_name} group",
        )

    return AddConsultPayloadType(success=success, comment_id=str(comment_id))
