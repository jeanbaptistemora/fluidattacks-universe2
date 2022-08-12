import authz
from db_model.event_comments.types import (
    EventComment,
)
from event_comments import (
    dal as comments_dal,
)
from typing import (
    Any,
)


def _is_scope_comment(comment: EventComment) -> bool:
    return str(comment.content).strip() not in {"#external", "#internal"}


async def add(
    comment_data: EventComment,
) -> None:
    await comments_dal.create_typed(comment_data)


async def delete(comment_id: str, event_id: str) -> bool:
    return await comments_dal.delete(comment_id, event_id)


async def get_event_comments(
    loaders: Any, group_name: str, event_id: str, user_email: str
) -> list[EventComment]:
    comments: list[EventComment] = await loaders.event_comments.load(event_id)

    enforcer = await authz.get_group_level_enforcer(loaders, user_email)
    if enforcer(group_name, "handle_comment_scope"):
        return comments
    return list(filter(_is_scope_comment, comments))
