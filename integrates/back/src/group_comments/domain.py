from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    InvalidCommentParent,
)
from dataloaders import (
    Dataloaders,
)
from db_model.group_comments.types import (
    GroupComment,
)
from group_comments import (
    dal as group_comments_dal,
)
from newutils.validations import (
    validate_field_length,
)


def _is_scope_comment(comment: GroupComment) -> bool:
    return comment.content.strip() not in {"#external", "#internal"}


async def add_comment(
    loaders: Dataloaders,
    group_name: str,
    email: str,
    comment_data: GroupComment,
) -> None:
    """Add comment in a group."""
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
    await group_comments_dal.add(group_comment=comment_data)


async def remove_comment(group_name: str, comment_id: str) -> None:
    await group_comments_dal.remove(
        group_name=group_name, comment_id=comment_id
    )


async def list_comments(
    loaders: Dataloaders, group_name: str, user_email: str
) -> tuple[GroupComment, ...]:
    enforcer = await authz.get_group_level_enforcer(loaders, user_email)
    comments: tuple[GroupComment, ...] = await loaders.group_comments.load(
        group_name
    )

    if enforcer(group_name, "handle_comment_scope"):
        return comments

    return tuple(filter(_is_scope_comment, comments))


async def mask_comments(loaders: Dataloaders, group_name: str) -> None:
    comments: tuple[GroupComment, ...] = await loaders.group_comments.load(
        group_name
    )
    await collect(
        [
            remove_comment(comment.group_name, comment.id)
            for comment in comments
        ]
    )
