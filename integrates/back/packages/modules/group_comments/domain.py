# Standard libraries
from typing import (
    Dict,
    List,
)

# Third-party liibraries
from aioextensions import collect

# Local libraries
from backend import authz
from backend.typing import Comment as CommentType
from group_comments import dal as group_comments_dal
from newutils import comments as comments_utils
from users import domain as users_domain


def _is_scope_comment(comment: CommentType) -> bool:
    return str(comment['content']).strip() not in {'#external', '#internal'}


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
