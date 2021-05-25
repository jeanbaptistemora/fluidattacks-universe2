from time import time
from typing import Dict

from aioextensions import schedule
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import AddConsultPayload
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from events import domain as events_domain
from mailer import events as events_mail
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from redis_cluster.operations import redis_del_by_deps_soon


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    content: str,
    event_id: str,
    parent: str,
) -> AddConsultPayload:
    random_comment_id = int(round(time() * 1000))
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email = str(user_info["user_email"])
    comment_data = {
        "comment_type": "event",
        "parent": parent,
        "content": content,
        "user_id": random_comment_id,
    }
    comment_id, success = await events_domain.add_comment(
        info, user_email, comment_data, event_id, parent
    )
    if success:
        redis_del_by_deps_soon("add_event_consult", event_id=event_id)
        if content.strip() not in {"#external", "#internal"}:
            schedule(
                events_mail.send_mail_comment(
                    info.context, comment_data, user_email, event_id
                )
            )

        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added comment to event {event_id} successfully",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add comment in event {event_id}",
        )

    return AddConsultPayload(success=success, comment_id=str(comment_id))
