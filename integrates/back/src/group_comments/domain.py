from aioextensions import (
    schedule,
)
import authz
from custom_exceptions import (
    InvalidCommentParent,
)
from dataloaders import (
    Dataloaders,
)
from db_model import (
    group_comments as group_comments_model,
)
from db_model.group_comments.types import (
    GroupComment,
)
from group_access.domain import (
    get_stakeholders_subscribed_to_consult,
)
from mailer import (
    groups as groups_mail,
)
from newutils.validations import (
    validate_field_length,
)


def _is_scope_comment(comment: GroupComment) -> bool:
    return comment.content.strip() not in {"#external", "#internal"}


async def send_group_consult_mail(
    loaders: Dataloaders,
    comment_data: GroupComment,
    group_name: str,
) -> None:
    await groups_mail.send_mail_comment(
        loaders=loaders,
        comment_data=comment_data,
        user_mail=comment_data.email,
        recipients=await get_stakeholders_subscribed_to_consult(
            loaders=loaders,
            group_name=group_name,
            comment_type="group",
        ),
        group_name=group_name,
    )


async def add_comment(
    loaders: Dataloaders,
    group_name: str,
    comment_data: GroupComment,
) -> None:
    """Add comment in a group."""
    parent_comment = comment_data.parent_id
    content = comment_data.content
    email = comment_data.email
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
    await group_comments_model.add(group_comment=comment_data)
    if _is_scope_comment(comment_data):
        schedule(
            send_group_consult_mail(
                loaders,
                comment_data,
                group_name,
            )
        )


async def remove_comments(group_name: str) -> None:
    await group_comments_model.remove_group_comments(group_name=group_name)


async def get_comments(
    loaders: Dataloaders, group_name: str, email: str
) -> tuple[GroupComment, ...]:
    enforcer = await authz.get_group_level_enforcer(loaders, email)
    comments: tuple[GroupComment, ...] = await loaders.group_comments.load(
        group_name
    )

    if enforcer(group_name, "handle_comment_scope"):
        return comments

    return tuple(filter(_is_scope_comment, comments))
