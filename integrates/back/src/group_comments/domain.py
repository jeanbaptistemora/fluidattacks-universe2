from aioextensions import (
    collect,
)
import authz
from comments.dal import (
    get_comments_for_ids,
)
from comments.domain import (
    filter_comments_date,
)
from custom_exceptions import (
    InvalidCommentParent,
)
from custom_types import (
    Comment as CommentType,
)
from datetime import (
    datetime,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_comments import (
    dal as group_comments_dal,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Dict,
    List,
)
from users import (
    domain as users_domain,
)


async def _get_fullname(objective_data: Dict[str, str]) -> str:
    objective_email = objective_data["email"]
    objective_possible_fullname = objective_data.get("fullname", "")
    real_name = objective_possible_fullname or objective_email

    if "@fluidattacks.com" in objective_email:
        return f"{real_name} at Fluid Attacks"

    return real_name


async def _fill_comment_data(data: Dict[str, str]) -> CommentType:
    fullname = await _get_fullname(objective_data=data)
    return {
        "content": data["content"],
        "created": datetime_utils.format_comment_date(data["created"]),
        "email": data["email"],
        "fullname": fullname if fullname else data["email"],
        "id": int(data["user_id"]),
        "modified": datetime_utils.format_comment_date(data["modified"]),
        "parent": int(data["parent"]),
    }


def _is_scope_comment(comment: CommentType) -> bool:
    return str(comment["content"]).strip() not in {"#external", "#internal"}


async def add_comment(
    info: GraphQLResolveInfo,
    group_name: str,
    email: str,
    comment_data: CommentType,
) -> bool:
    """Add comment in a group."""
    parent = str(comment_data["parent"])
    content = str(comment_data["content"])
    await authz.validate_handle_comment_scope(
        content, email, group_name, parent, info.context.store
    )
    if parent != "0":
        group_comments = [
            str(comment.get("user_id"))
            for comment in await get_comments(group_name)
        ]
        if parent not in group_comments:
            raise InvalidCommentParent()
    return await group_comments_dal.add_comment(
        group_name, email, comment_data
    )


async def delete_comment(group_name: str, user_id: str) -> bool:
    return await group_comments_dal.delete_comment(group_name, user_id)


async def get_comments(group_name: str) -> List[Dict[str, str]]:
    comments = await group_comments_dal.get_comments(group_name)
    comments_name_data = await collect(
        [
            users_domain.get_user_name(mail)
            for mail in set(comment["email"] for comment in comments)
        ]
    )
    comments_fullnames = {
        mail: list(fullnames.values())
        for data in comments_name_data
        for mail, fullnames in data.items()
    }
    for comment in comments:
        comment["fullname"] = " ".join(
            filter(None, comments_fullnames[comment["email"]][::-1])
        )
    return comments


async def list_comments(group_name: str, user_email: str) -> List[CommentType]:
    enforcer = await authz.get_group_level_enforcer(user_email)
    comments = await collect(
        [
            _fill_comment_data(comment)
            for comment in await group_comments_dal.get_comments(group_name)
        ]
    )

    if enforcer(group_name, "handle_comment_scope"):
        return comments

    return list(filter(_is_scope_comment, comments))


async def mask_comments(group_name: str) -> bool:
    comments = await get_comments(group_name)
    return all(
        await collect(
            [
                delete_comment(
                    get_key_or_fallback(comment), comment["user_id"]
                )
                for comment in comments
            ]
        )
    )


async def get_total_comments_date(
    findings_ids: List[str],
    group_name: str,
    min_date: datetime,
) -> int:
    """Get the total comments in the group"""
    group_comments_len = len(
        filter_comments_date(await get_comments(group_name), min_date)
    )

    events_ids = await events_domain.list_group_events(group_name)
    events_comments_len = len(
        filter_comments_date(
            await get_comments_for_ids("event", events_ids), min_date
        )
    )

    findings_comments_len = len(
        filter_comments_date(
            await get_comments_for_ids("comment", findings_ids), min_date
        )
    )
    findings_comments_len += len(
        filter_comments_date(
            await get_comments_for_ids("observation", findings_ids), min_date
        )
    )
    findings_comments_len += len(
        filter_comments_date(
            await get_comments_for_ids("zero_risk", findings_ids), min_date
        )
    )

    return group_comments_len + events_comments_len + findings_comments_len
