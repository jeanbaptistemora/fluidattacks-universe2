from aioextensions import (
    schedule,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    AddConsultPayload,
)
from db_model.event_comments.types import (
    EventComment,
)
from db_model.events.types import (
    Event,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from mailer import (
    events as events_mail,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
    validations,
)
from newutils.datetime import (
    get_as_utc_iso_format,
    get_now,
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
    Dict,
)


async def send_event_consult_mail(
    *,
    info: GraphQLResolveInfo,
    comment_data: EventComment,
    event_id: str,
    user_email: str,
    group_name: str,
) -> None:
    await events_mail.send_mail_comment(
        loaders=info.context.loaders,
        comment_data=comment_data,
        event_id=event_id,
        recipients=await get_users_subscribed_to_consult(
            loaders=info.context.loaders,
            group_name=group_name,
            comment_type="event",
        ),
        user_mail=user_email,
        group_name=group_name,
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
    content: str,
    event_id: str,
    parent_comment: str,
) -> AddConsultPayload:
    validations.validate_fields([content])

    comment_id: str = str(round(time() * 1000))
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    today = get_as_utc_iso_format(get_now())
    user_email = str(user_info["user_email"])

    comment_data = EventComment(
        event_id=event_id,
        parent_id=str(parent_comment),
        creation_date=today,
        content=content,
        id=comment_id,
        email=user_email,
        full_name=str.join(
            " ",
            [user_info.get("first_name", ""), user_info.get("last_name", "")],
        ),
    )
    await events_domain.add_comment(
        info, user_email, comment_data, event_id, parent_comment
    )

    redis_del_by_deps_soon("add_event_consult", event_id=event_id)
    if content.strip() not in {"#external", "#internal"}:
        event_loader = info.context.loaders.event
        event: Event = await event_loader.load(event_id)
        group_name = event.group_name
        schedule(
            send_event_consult_mail(
                info=info,
                comment_data=comment_data,
                event_id=event_id,
                user_email=user_email,
                group_name=group_name,
            )
        )

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added comment to event {event_id} successfully",
    )

    return AddConsultPayload(success=True, comment_id=str(comment_id))
