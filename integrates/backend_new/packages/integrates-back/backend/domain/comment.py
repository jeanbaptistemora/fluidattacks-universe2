
from typing import Dict, List, Tuple, Union, cast

from aioextensions import collect
from backend import authz, util
from backend.dal import (
    comment as comment_dal,
    finding as finding_dal
)
from backend.domain import vulnerability as vuln_domain
from backend.typing import (
    Comment as CommentType,
    User as UserType
)
from backend.utils import (
    datetime as datetime_utils,
)


async def _get_comments(
        comment_type: str,
        project_name: str,
        finding_id: str,
        user_email: str) -> List[CommentType]:
    comments = await collect([
        fill_comment_data(
            project_name,
            user_email,
            cast(Dict[str, str], comment)
        )
        for comment in await comment_dal.get_comments(
            comment_type,
            int(finding_id)
        )
    ])
    return list(comments)


async def get_comments(
        project_name: str,
        finding_id: str,
        user_email: str) -> List[CommentType]:
    comments = await _get_comments(
        'comment',
        project_name,
        finding_id,
        user_email
    )

    finding_attr = await finding_dal.get_attributes(
        finding_id,
        ['historic_verification']
    )
    historic_verification = cast(
        List[Dict[str, finding_dal.FindingType]],
        finding_attr.get('historic_verification', [])
    )
    verified = [
        verification
        for verification in historic_verification
        if cast(List[str], verification.get('vulns', []))
    ]
    if verified:
        vulns = await vuln_domain.list_vulnerabilities_async([finding_id])
        comments = [
            fill_vuln_info(
                cast(Dict[str, str], comment),
                cast(List[str], verification.get('vulns', [])),
                vulns
            )
            if comment.get('id') == verification.get('comment')
            else comment
            for comment in comments
            for verification in verified
        ]

    return comments


async def get_event_comments(
        project_name: str,
        finding_id: str,
        user_email: str) -> List[CommentType]:
    comments = await _get_comments(
        'event',
        project_name,
        finding_id,
        user_email
    )

    return comments


async def get_fullname(
        project_name: str,
        requester_email: str,
        objective_data: Dict[str, str]) -> str:
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
            objective_email, project_name
        )

        name_to_show = {
            'analyst': 'Hacker at Fluid Attacks',
            'admin': 'Hacker at Fluid Attacks',
            'customeradmin': real_name,
        }.get(objective_role, 'Someone at Fluid Attacks')

    return name_to_show


def fill_vuln_info(
        comment: Dict[str, str],
        vulns_ids: List[str],
        vulns: List[Dict[str, finding_dal.FindingType]]) -> CommentType:
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


async def fill_comment_data(
        project_name: str,
        requester_email: str,
        data: Dict[str, str]) -> CommentType:
    fullname = await get_fullname(
        project_name=project_name,
        requester_email=requester_email,
        objective_data=data)

    return {
        'content': data['content'],
        'created': util.format_comment_date(data['created']),
        'email': data['email'],
        'fullname': fullname if fullname else data['email'],
        'id': int(data['user_id']),
        'modified': util.format_comment_date(data['modified']),
        'parent': int(data['parent'])}


async def get_observations(
        project_name: str,
        finding_id: str,
        user_email: str) -> List[CommentType]:
    observations = await _get_comments(
        'observation',
        project_name,
        finding_id, user_email
    )

    return observations


async def create(
        element_id: str, comment_data: CommentType,
        user_info: UserType) -> Tuple[Union[int, None], bool]:
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
    success = await comment_dal.create(
        comment_id,
        comment_attributes
    )

    return (comment_id if success else None, success)


async def edit_scope(
    comment_id: str,
    comment_scope: str,
    element_id: str,
) -> bool:
    success = await comment_dal.edit_scope(
        int(comment_id),
        comment_scope,
        int(element_id)
    )
    return success
