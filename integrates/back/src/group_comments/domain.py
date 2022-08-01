from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    InvalidCommentParent,
)
from db_model.group_comments.types import (
    GroupComment,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_comments import (
    dal as group_comments_dal,
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


def _is_scope_comment(comment: GroupComment) -> bool:
    return comment.content.strip() not in {"#external", "#internal"}


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
    loaders: Any, group_name: str, user_email: str
) -> List[GroupComment]:
    enforcer = await authz.get_group_level_enforcer(user_email)
    comments = await loaders.group_comments.load(group_name)

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
