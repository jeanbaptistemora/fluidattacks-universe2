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
import authz
from backend import util
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    User as UserType
)
from comments import dal as comments_dal
from newutils import (
    datetime as datetime_utils,
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
        fill_comment_data(
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


async def _get_fullname(
    group_name: str,
    requester_email: str,
    objective_data: Dict[str, str]
) -> str:
    objective_email = objective_data['email']
    objective_possible_fullname = objective_data.get('fullname', '')
    real_name = objective_possible_fullname or objective_email
    is_requester_at_fluid: bool = '@fluidattacks.com' in requester_email
    is_objective_at_fluid: bool = '@fluidattacks.com' in objective_email

    # Only Fluid Attacks' staff is masked
    if is_requester_at_fluid or not is_objective_at_fluid:
        name_to_show = real_name
    else:
        objective_role = await authz.get_group_level_role(
            objective_email,
            group_name
        )
        name_to_show = {
            'analyst': 'Hacker at Fluid Attacks',
            'admin': 'Hacker at Fluid Attacks',
            'customeradmin': real_name,
        }.get(objective_role, 'Someone at Fluid Attacks')
    return name_to_show


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


async def fill_comment_data(
    group_name: str,
    requester_email: str,
    data: Dict[str, str]
) -> CommentType:
    fullname = await _get_fullname(
        group_name=group_name,
        requester_email=requester_email,
        objective_data=data
    )
    return {
        'content': data['content'],
        'created': util.format_comment_date(data['created']),
        'email': data['email'],
        'fullname': fullname if fullname else data['email'],
        'id': int(data['user_id']),
        'modified': util.format_comment_date(data['modified']),
        'parent': int(data['parent'])
    }


async def get(comment_type: str, element_id: int) -> List[CommentType]:
    return await comments_dal.get_comments(comment_type, element_id)


async def get_comments(
    project_name: str,
    finding_id: str,
    user_email: str,
    info: GraphQLResolveInfo
) -> List[CommentType]:
    finding_loader = info.context.loaders.finding
    finding_vulns_loader = info.context.loaders.finding_vulns

    comments = await _get_comments(
        'comment',
        project_name,
        finding_id,
        user_email
    )
    finding = await finding_loader.load(finding_id)
    historic_verification = finding.get('historic_verification', [])
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
