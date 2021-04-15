# Standard libraries
from typing import (
    cast,
    Dict,
    List,
    Tuple,
    Union,
)

# Third party libraries
from aioextensions import collect
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import authz
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    User as UserType
)
from comments import dal as comments_dal
from newutils import (
    datetime as datetime_utils,
    comments as comments_utils,
    findings as findings_utils,
)


def _fill_vuln_info(
    comment: Dict[str, str],
    vulns_ids: List[str],
    vulns: List[Dict[str, FindingType]]
) -> CommentType:
    selected_vulns = [
        vuln.get('where')
        for vuln in vulns
        if vuln.get('UUID') in vulns_ids
    ]
    selected_vulns = list(set(selected_vulns))
    wheres = ', '.join(cast(List[str], selected_vulns))
    comment['content'] = (
        f'Regarding vulnerabilities {wheres}:\n\n' +
        comment.get('content', '')
    )
    return cast(CommentType, comment)


async def _get_comments(
    comment_type: str,
    project_name: str,
    finding_id: str,
    user_email: str
) -> List[CommentType]:
    comments = await collect([
        comments_utils.fill_comment_data(
            project_name,
            user_email,
            cast(Dict[str, str], comment)
        )
        for comment in await comments_dal.get_comments(
            comment_type,
            int(finding_id)
        )
    ])
    return list(comments)


def _is_scope_comment(comment: CommentType) -> bool:
    return str(comment['content']).strip() not in {'#external', '#internal'}


async def create(
    element_id: str,
    comment_data: CommentType,
    user_info: UserType
) -> Tuple[Union[int, None], bool]:
    today = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )
    comment_id = cast(int, comment_data.get('user_id', 0))
    comment_attributes = {
        'comment_type': str(comment_data.get('comment_type')),
        'content': str(comment_data.get('content')),
        'created': today,
        'email': user_info['user_email'],
        'finding_id': int(element_id),
        'fullname': str.join(
            ' ',
            [
                str(user_info['first_name']),
                str(user_info['last_name'])
            ]
        ),
        'modified': today,
        'parent': comment_data.get('parent')
    }
    success = await comments_dal.create(
        comment_id,
        comment_attributes
    )
    return (comment_id if success else None, success)


async def delete(finding_id: int, user_id: int) -> bool:
    return await comments_dal.delete(finding_id, user_id)


async def get(comment_type: str, element_id: int) -> List[CommentType]:
    return await comments_dal.get_comments(comment_type, element_id)


async def get_comments(
    project_name: str,
    finding_id: str,
    user_email: str,
    info: GraphQLResolveInfo
) -> List[CommentType]:
    finding_vulns_loader = info.context.loaders.finding_vulns
    comments = await _get_comments(
        'comment',
        project_name,
        finding_id,
        user_email
    )
    historic_verification = await findings_utils.get_historic_verification(
        finding_id
    )
    verified = [
        verification
        for verification in historic_verification
        if cast(List[str], verification.get('vulns', []))
    ]
    if verified:
        vulns = await finding_vulns_loader.load(finding_id)
        comments = [
            _fill_vuln_info(
                cast(Dict[str, str], comment),
                cast(List[str], verification.get('vulns', [])),
                vulns
            )
            if comment.get('id') == verification.get('comment')
            else comment
            for comment in comments
            for verification in verified
        ]

    new_comments: List[CommentType] = []
    enforcer = await authz.get_group_level_enforcer(user_email)
    if enforcer(project_name, 'handle_comment_scope'):
        new_comments = comments
    else:
        new_comments = list(
            filter(_is_scope_comment, comments)
        )
    return new_comments


async def get_event_comments(
    project_name: str,
    finding_id: str,
    user_email: str
) -> List[CommentType]:
    comments = await _get_comments(
        'event',
        project_name,
        finding_id,
        user_email
    )

    new_comments: List[CommentType] = []
    enforcer = await authz.get_group_level_enforcer(user_email)
    if enforcer(project_name, 'handle_comment_scope'):
        new_comments = comments
    else:
        new_comments = list(
            filter(_is_scope_comment, comments)
        )
    return new_comments


async def get_observations(
    project_name: str,
    finding_id: str,
    user_email: str
) -> List[CommentType]:
    observations = await _get_comments(
        'observation',
        project_name,
        finding_id, user_email
    )

    new_observations: List[CommentType] = []
    enforcer = await authz.get_group_level_enforcer(user_email)
    if enforcer(project_name, 'handle_comment_scope'):
        new_observations = observations
    else:
        new_observations = list(
            filter(_is_scope_comment, observations)
        )
    return new_observations
