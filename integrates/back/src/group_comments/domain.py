from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    InvalidCommentParent,
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
from newutils.validations import (
    validate_field_length,
)
from typing import (
    Any,
    Dict,
    List,
)


async def _get_fullname(objective_data: Dict[str, Any]) -> str:
    objective_email = str(objective_data["email"])
    objective_possible_fullname = str(objective_data.get("fullname", ""))
    real_name = objective_possible_fullname or objective_email

    if "@fluidattacks.com" in objective_email:
        return f"{real_name} at Fluid Attacks"

    return real_name


async def _fill_comment_data(data: Dict[str, Any]) -> Dict[str, Any]:
    fullname = await _get_fullname(objective_data=data)
    return {
        "content": data["content"],
        "created": datetime_utils.format_comment_date(str(data["created"])),
        "email": data["email"],
        "fullname": fullname if fullname else data["email"],
        "id": int(str(data["user_id"])),
        "modified": datetime_utils.format_comment_date(str(data["modified"])),
        "parent": int(str(data["parent"])),
    }


def _is_scope_comment(comment: Dict[str, Any]) -> bool:
    return str(comment["content"]).strip() not in {"#external", "#internal"}


async def add_comment(
    info: GraphQLResolveInfo,
    group_name: str,
    email: str,
    comment_data: Dict[str, Any],
) -> bool:
    """Add comment in a group."""
    parent_comment = str(comment_data["parent"])
    content = str(comment_data["content"])
    validate_field_length(content, 20000)
    await authz.validate_handle_comment_scope(
        content, email, group_name, parent_comment, info.context.store
    )
    if parent_comment != "0":
        comments = await group_comments_dal.get_comments(group_name)
        group_comments = [str(comment.get("user_id")) for comment in comments]
        if parent_comment not in group_comments:
            raise InvalidCommentParent()
    return await group_comments_dal.add_comment(
        group_name, email, comment_data
    )


async def delete_comment(group_name: str, user_id: str) -> bool:
    return await group_comments_dal.delete_comment(group_name, user_id)


async def list_comments(
    group_name: str, user_email: str
) -> List[Dict[str, Any]]:
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
    comments = await group_comments_dal.get_comments(group_name)
    return all(
        await collect(
            [
                delete_comment(
                    get_key_or_fallback(comment), str(comment["user_id"])
                )
                for comment in comments
            ]
        )
    )
