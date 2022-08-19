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


def _is_scope_comment(comment: EventComment) -> bool:
    return str(comment.content).strip() not in {"#external", "#internal"}


async def add(
    comment_data: EventComment,
) -> None:
    await event_comments_model.add(event_comment=comment_data)


async def remove(comment_id: str, event_id: str) -> None:
    await event_comments_model.remove(comment_id=comment_id, event_id=event_id)


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
