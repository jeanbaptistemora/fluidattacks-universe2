
from typing import Dict, List, Tuple, Union, cast
from datetime import datetime

import pytz
from django.conf import settings

from backend.domain import user as user_domain

from backend import util
from backend.dal import comment as comment_dal, finding as finding_dal, vulnerability as vuln_dal
from backend.typing import Comment as CommentType, User as UserType


def _get_comments(
        comment_type: str,
        project_name: str,
        finding_id: str,
        user_email: str) -> List[CommentType]:
    comments = [
        fill_comment_data(project_name, user_email, cast(Dict[str, str], comment))
        for comment in comment_dal.get_comments(comment_type, int(finding_id))
    ]
    return comments


def get_comments(
        project_name: str,
        finding_id: str,
        user_email: str) -> List[CommentType]:
    comments = \
        _get_comments('comment', project_name, finding_id, user_email)

    historic_verification = \
        cast(List[Dict[str, finding_dal.FindingType]], finding_dal.get_attributes(
             finding_id, ['historic_verification']).get('historic_verification', []))
    verified = [verification for verification in historic_verification
                if cast(List[str], verification.get('vulns', []))]
    if verified:
        vulns = vuln_dal.get_vulnerabilities(finding_id)
        comments = [fill_vuln_info(cast(Dict[str, str], comment),
                                   cast(List[str], verification.get('vulns', [])),
                                   vulns)
                    if comment.get('id') == verification.get('comment') else comment
                    for comment in comments
                    for verification in verified]

    return comments


def get_event_comments(project_name: str, finding_id: str, user_email: str) -> List[CommentType]:
    comments = _get_comments('event', project_name, finding_id, user_email)

    return comments


def get_fullname(
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
        objective_role = \
            user_domain.get_group_level_role(objective_email, project_name)

        name_to_show = {
            'analyst': 'Hacker at Fluid Attacks',
            'admin': 'Hacker at Fluid Attacks',
            'customeradmin': real_name,
        }.get(objective_role, 'Someone at Fluid Attacks')

    return name_to_show


def fill_vuln_info(comment: Dict[str, str], vulns_ids: List[str],
                   vulns: List[Dict[str, finding_dal.FindingType]]) -> CommentType:
    selected_vulns = [vuln.get('where') for vuln in vulns if vuln.get('UUID') in vulns_ids]
    selected_vulns = list(set(selected_vulns))
    wheres = ', '.join(cast(List[str], selected_vulns))
    comment['content'] = f'Regarding vulnerabilities {wheres}:\n\n' + comment.get('content', '')

    return cast(CommentType, comment)


def fill_comment_data(
        project_name: str,
        requester_email: str,
        data: Dict[str, str]) -> CommentType:
    fullname = get_fullname(
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


def get_observations(
        project_name: str,
        finding_id: str,
        user_email: str) -> List[CommentType]:
    observations = \
        _get_comments('observation', project_name, finding_id, user_email)

    return observations


def create(element_id: str, comment_data: CommentType,
           user_info: UserType) -> Tuple[Union[int, None], bool]:
    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    comment_id = cast(int, comment_data.get('user_id', 0))
    comment_attributes = {
        'comment_type': str(comment_data.get('comment_type')),
        'content': str(comment_data.get('content')),
        'created': today,
        'email': user_info['user_email'],
        'finding_id': int(element_id),
        'fullname': str.join(
            ' ', [str(user_info['first_name']),
                  str(user_info['last_name'])]),
        'modified': today,
        'parent': comment_data.get('parent')
    }
    success = comment_dal.create(comment_id, cast(CommentType, comment_attributes))

    return (comment_id if success else None, success)
