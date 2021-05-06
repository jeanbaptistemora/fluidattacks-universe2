# Standard libraries
from datetime import datetime
from typing import (
    Dict,
    List,
)

# Third-party liibraries
from aioextensions import collect
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
import authz
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
)
from comments.domain import (
    fill_comment_data,
    filter_comments_date,
)
from comments.dal import get_comments_for_ids
from custom_exceptions import InvalidCommentParent
from events import domain as events_domain
from group_comments import dal as group_comments_dal
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
    await authz.validate_handle_comment_scope(
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
        fill_comment_data(group_name, user_email, comment)
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


async def get_total_comments_date(
    findings: List[Dict[str, FindingType]],
    group_name: str,
    min_date: datetime,
) -> int:
    """Get the total comments in the group"""
    group_comments_len = len(
        filter_comments_date(
            await get_comments(group_name), min_date))

    events_ids = await events_domain.list_group_events(group_name)
    events_comments_len = len(
        filter_comments_date(
            await get_comments_for_ids(
                'event', events_ids), min_date))

    findings_ids = [str(finding['finding_id']) for finding in findings]
    findings_comments_len = len(
        filter_comments_date(
            await get_comments_for_ids(
                'comment', findings_ids), min_date))
    findings_comments_len += len(
        filter_comments_date(
            await get_comments_for_ids(
                'observation', findings_ids), min_date))
    findings_comments_len += len(
        filter_comments_date(
            await get_comments_for_ids(
                'zero_risk', findings_ids), min_date))

    return group_comments_len + events_comments_len + findings_comments_len
