import authz
from db_model.event_comments.types import (
    EventComment,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from event_comments import (
    dal as comments_dal,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Union,
)


def _is_scope_comment(comment: EventComment) -> bool:
    return str(comment.content).strip() not in {"#external", "#internal"}


async def add(
    finding_id: str,
    comment_data: Dict[str, Any],
    user_info: Stakeholder,
) -> Tuple[Union[str, None], bool]:
    today = datetime_utils.get_as_str(datetime_utils.get_now())
    comment_id = str(comment_data["comment_id"])
    comment_attributes = {
        "comment_type": comment_data["comment_type"],
        "content": str(comment_data.get("content")),
        "created": today,
        "email": user_info.email,
        "fullname": str.join(" ", [user_info.first_name, user_info.last_name])
        if user_info.first_name and user_info.last_name
        else "",
        "modified": today,
        "parent": comment_data.get("parent", "0"),
    }
    success = await comments_dal.create(
        comment_id, comment_attributes, finding_id
    )
    return (comment_id if success else None, success)


async def delete(comment_id: str, finding_id: str) -> bool:
    return await comments_dal.delete(comment_id, finding_id)


async def get(comment_type: str, element_id: str) -> List[Dict[str, Any]]:
    return await comments_dal.get_comments(comment_type, element_id)


async def get_event_comments(
    loaders: Any, group_name: str, finding_id: str, user_email: str
) -> list[EventComment]:
    comments: list[EventComment] = await loaders.event_comments.load(
        finding_id
    )

    enforcer = await authz.get_group_level_enforcer(user_email)
    if enforcer(group_name, "handle_comment_scope"):
        return comments
    return list(filter(_is_scope_comment, comments))
