from aioextensions import (
    schedule,
)
import authz
from dataloaders import (
    Dataloaders,
)
from db_model import (
    event_comments as event_comments_model,
)
from db_model.event_comments.types import (
    EventComment,
)
from group_access.domain import (
    get_stakeholders_subscribed_to_consult,
)
from mailer import (
    events as events_mail,
)


def _is_scope_comment(comment: EventComment) -> bool:
    return str(comment.content).strip() not in {"#external", "#internal"}


async def add(
    loaders: Dataloaders,
    comment_data: EventComment,
    group_name: str,
) -> None:
    await event_comments_model.add(event_comment=comment_data)
    if _is_scope_comment(comment_data):
        schedule(
            events_mail.send_mail_comment(
                loaders=loaders,
                comment_data=comment_data,
                event_id=comment_data.event_id,
                recipients=await get_stakeholders_subscribed_to_consult(
                    loaders=loaders,
                    group_name=group_name,
                    comment_type="event",
                ),
                user_mail=comment_data.email,
                group_name=group_name,
            )
        )


async def remove_comments(event_id: str) -> None:
    await event_comments_model.remove_event_comments(event_id=event_id)


async def get_comments(
    loaders: Dataloaders, group_name: str, event_id: str, email: str
) -> tuple[EventComment, ...]:
    comments: tuple[EventComment, ...] = await loaders.event_comments.load(
        event_id
    )
    enforcer = await authz.get_group_level_enforcer(loaders, email)
    if enforcer(group_name, "handle_comment_scope"):
        return comments

    return tuple(filter(_is_scope_comment, comments))
