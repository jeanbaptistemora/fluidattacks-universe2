# Standard libraries
from typing import (
    Dict,
    List,
)

# Third-party liibraries
from aioextensions import (
    collect,
    schedule,
)
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import (
    authz,
    mailer,
)
from backend.typing import Comment as CommentType
from custom_exceptions import InvalidCommentParent
from group_comments import dal as group_comments_dal
from newutils import comments as comments_utils
from users import domain as users_domain


def _is_scope_comment(comment: CommentType) -> bool:
    return str(comment['content']).strip() not in {'#external', '#internal'}


async def add_comment(
    info: GraphQLResolveInfo,
    group_name: str,
    email: str,
    comment_data: CommentType
) -> bool:
    """Add comment in a group."""
    parent = str(comment_data['parent'])
    content = str(comment_data['content'])
    await comments_utils.validate_handle_comment_scope(
        content,
        email,
        group_name,
        parent,
        info.context.store
    )
    if parent != '0':
        group_comments = [
            str(comment.get('user_id'))
            for comment in await get_comments(group_name)
        ]
        if parent not in group_comments:
            raise InvalidCommentParent()
    return await group_comments_dal.add_comment(
        group_name,
        email,
        comment_data
    )


async def delete_comment(group_name: str, user_id: str) -> bool:
    return await group_comments_dal.delete_comment(group_name, user_id)


async def get_comments(group_name: str) -> List[Dict[str, str]]:
    comments = await group_comments_dal.get_comments(group_name)
    comments_name_data = await collect([
        users_domain.get_user_name(mail)
        for mail in set(comment['email'] for comment in comments)
    ])
    comments_fullnames = {
        mail: list(fullnames.values())
        for data in comments_name_data for mail, fullnames in data.items()
    }
    for comment in comments:
        comment['fullname'] = ' '.join(
            filter(None, comments_fullnames[comment['email']][::-1])
        )
    return comments


async def list_comments(group_name: str, user_email: str) -> List[CommentType]:
    enforcer = await authz.get_group_level_enforcer(user_email)
    comments = await collect([
        comments_utils.fill_comment_data(group_name, user_email, comment)
        for comment in await group_comments_dal.get_comments(group_name)
    ])

    new_comments: List[CommentType] = []
    if enforcer(group_name, 'handle_comment_scope'):
        new_comments = comments
    else:
        new_comments = list(filter(_is_scope_comment, comments))
    return new_comments


async def mask_comments(group_name: str) -> bool:
    comments = await get_comments(group_name)
    are_comments_masked = all(
        await collect([
            delete_comment(comment['project_name'], comment['user_id'])
            for comment in comments
        ])
    )
    return are_comments_masked


def send_comment_mail(
    user_email: str,
    comment_data: CommentType,
    group_name: str
) -> None:
    schedule(
        mailer.send_comment_mail(
            comment_data,
            'project',
            user_email,
            'project',
            group_name
        )
    )
