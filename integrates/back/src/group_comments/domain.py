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
from newutils.validations import (
    validate_field_length,
)
from typing import (
    Any,
)


def _is_scope_comment(comment: GroupComment) -> bool:
    return comment.content.strip() not in {"#external", "#internal"}


async def add_comment(
    info: GraphQLResolveInfo,
    group_name: str,
    email: str,
    comment_data: GroupComment,
) -> None:
    """Add comment in a group."""
    loaders = info.context.loaders
    parent_comment = comment_data.parent_id
    content = comment_data.content
    validate_field_length(content, 20000)
    await authz.validate_handle_comment_scope(
        loaders, content, email, group_name, parent_comment
    )
    if parent_comment != "0":
        comments: list[GroupComment] = await loaders.group_comments.load(
            group_name
        )
        group_comments = [comment.id for comment in comments]
        if parent_comment not in group_comments:
            raise InvalidCommentParent()
    await group_comments_dal.add_comment_typed(comment_data)


async def delete_comment(group_name: str, user_id: str) -> bool:
    return await group_comments_dal.delete_comment(group_name, user_id)


async def list_comments(
    loaders: Any, group_name: str, user_email: str
) -> list[GroupComment]:
    enforcer = await authz.get_group_level_enforcer(loaders, user_email)
    comments = await loaders.group_comments.load(group_name)

    if enforcer(group_name, "handle_comment_scope"):
        return comments

    return list(filter(_is_scope_comment, comments))


async def mask_comments(loaders: Any, group_name: str) -> bool:
    comments: list[GroupComment] = await loaders.group_comments.load(
        group_name
    )
    return all(
        await collect(
            [
                delete_comment(comment.group_name, comment.id)
                for comment in comments
            ]
        )
    )
