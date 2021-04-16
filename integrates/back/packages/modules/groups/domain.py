# Standard libraries
import logging
import logging.config
import re
import secrets
from contextlib import AsyncExitStack
from datetime import date
from decimal import Decimal
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Set,
    Union,
)

# Third-party libraries
from aioextensions import (
    collect,
    in_process,
    schedule,
)
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from back.settings import LOGGING
from backend import (
    authz,
    mailer,
)
from backend.dal import project as group_dal
from backend.dal.helpers.dynamodb import start_context
from backend.exceptions import (
    InvalidCommentParent,
    InvalidProjectServicesConfig,
    RepeatedValues,
)
from backend.typing import (
    Comment as CommentType,
    MailContent as MailContentType,
    Project as GroupType,
)
from group_access import domain as group_access_domain
from group_comments import domain as group_comments_domain
from newutils import (
    apm,
    comments as comments_utils,
    datetime as datetime_utils,
    vulnerabilities as vulns_utils,
)
from newutils.validations import (
    validate_alphanumeric_field,
    validate_email_address,
    validate_field_length,
    validate_fluidattacks_staff_on_group,
    validate_phone_field,
)
from organizations import domain as orgs_domain
from __init__ import BASE_URL


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _has_repeated_tags(group_name: str, tags: List[str]) -> bool:
    has_repeated_tags = len(tags) != len(set(tags))
    if not has_repeated_tags:
        group_info = await get_attributes(group_name.lower(), ['tag'])
        existing_tags = group_info.get('tag', [])
        all_tags = list(existing_tags) + tags
        has_repeated_tags = len(all_tags) != len(set(all_tags))
    return has_repeated_tags


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
            for comment in await group_comments_domain.get_comments(group_name)
        ]
        if parent not in group_comments:
            raise InvalidCommentParent()
    return await group_dal.add_comment(group_name, email, comment_data)


async def can_user_access(group: str, role: str) -> bool:
    return await group_dal.can_user_access(group, role)


async def get_active_groups() -> List[str]:
    groups = await group_dal.get_active_projects()
    return groups


async def get_alive_group_names() -> List[str]:
    attributes = ['project_name']
    groups = await get_alive_groups(attributes)
    return [group['project_name'] for group in groups]


async def get_all(attributes: Optional[List[str]] = None) -> List[GroupType]:
    data_attr = ','.join(attributes or [])
    return await group_dal.get_all(data_attr=data_attr)


async def get_alive_groups(
    attributes: Optional[List[str]] = None
) -> List[GroupType]:
    data_attr = ','.join(attributes or [])
    groups = await group_dal.get_alive_groups(data_attr)
    return groups


async def get_attributes(
    group_name: str,
    attributes: List[str]
) -> Dict[str, Union[str, List[str]]]:
    return await group_dal.get_attributes(group_name, attributes)


async def get_description(group_name: str) -> str:
    return await group_dal.get_description(group_name)


@apm.trace()
async def get_groups_by_user(
    user_email: str,
    active: bool = True,
    organization_id: str = ''
) -> List[str]:
    user_groups: List[str] = []
    groups = await group_access_domain.get_user_groups(user_email, active)
    group_level_roles = await authz.get_group_level_roles(user_email, groups)
    can_access_list = await collect(
        can_user_access(group, role)
        for role, group in zip(group_level_roles.values(), groups)
    )
    user_groups = [
        group
        for can_access, group in zip(can_access_list, groups)
        if can_access
    ]

    if organization_id:
        org_groups = await orgs_domain.get_groups(organization_id)
        user_groups = [
            group
            for group in user_groups
            if group in org_groups
        ]
    return user_groups


async def get_groups_with_forces() -> List[str]:
    return await group_dal.get_groups_with_forces()


async def get_many_groups(groups_name: List[str]) -> List[GroupType]:
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(group_dal.TABLE_NAME)
        groups = await collect(
            group_dal.get_group(group_name, table)
            for group_name in groups_name
        )
    return cast(List[GroupType], groups)


async def get_mean_remediate(
    context: Any,
    group_name: str,
    min_date: Optional[date] = None
) -> Decimal:
    group_findings_loader = context.group_findings
    finding_vulns_loaders = context.finding_vulns

    group_findings = await group_findings_loader.load(group_name)
    vulns = await finding_vulns_loaders.load_many_chained([
        str(finding['finding_id']) for finding in group_findings
    ])
    return await vulns_utils.get_mean_remediate_vulnerabilities(
        vulns,
        min_date
    )


async def get_mean_remediate_severity(  # pylint: disable=too-many-locals
    context: Any,
    group_name: str,
    min_severity: float,
    max_severity: float
) -> Decimal:
    """Get mean time to remediate."""
    total_days = 0
    finding_vulns_loader = context.finding_vulns_nzr
    group_findings_loader = context.group_findings

    group_findings = await group_findings_loader.load(group_name.lower())
    group_findings_ids = [
        finding['finding_id'] for finding in group_findings
        if (
            min_severity <=
            cast(float, finding.get('cvss_temporal', 0)) <=
            max_severity
        )
    ]
    findings_vulns = await finding_vulns_loader.load_many_chained(
        group_findings_ids
    )
    open_vuln_dates = await collect([
        in_process(vulns_utils.get_open_vulnerability_date, vuln)
        for vuln in findings_vulns
    ])
    filtered_open_vuln_dates = [
        vuln
        for vuln in open_vuln_dates
        if vuln
    ]
    closed_vuln_dates = await collect([
        in_process(vulns_utils.get_last_closing_date, vuln)
        for vuln, open_vuln_date in zip(findings_vulns, open_vuln_dates)
        if open_vuln_date
    ])
    for index, closed_vuln_date in enumerate(closed_vuln_dates):
        if closed_vuln_date:
            total_days += int(
                (closed_vuln_date - filtered_open_vuln_dates[index]).days
            )
        else:
            current_day = datetime_utils.get_now().date()
            total_days += int(
                (current_day - filtered_open_vuln_dates[index]).days
            )

    total_vuln = len(filtered_open_vuln_dates)
    if total_vuln:
        mean_vulnerabilities = Decimal(
            round(total_days / float(total_vuln))
        ).quantize(Decimal('0.1'))
    else:
        mean_vulnerabilities = Decimal(0).quantize(Decimal('0.1'))
    return mean_vulnerabilities


async def get_open_vulnerabilities(context: Any, group_name: str) -> int:
    group_findings_loader = context.group_findings
    group_findings_loader.clear(group_name)
    finding_vulns_loader = context.finding_vulns_nzr

    group_findings = await group_findings_loader.load(group_name)
    findings_vulns = await finding_vulns_loader.load_many_chained([
        finding['finding_id'] for finding in group_findings
    ])

    last_approved_status = await collect([
        in_process(vulns_utils.get_last_status, vuln)
        for vuln in findings_vulns
    ])
    open_vulnerabilities = 0
    for status in last_approved_status:
        if status == 'open':
            open_vulnerabilities += 1
    return open_vulnerabilities


async def invite_to_group(
    email: str,
    responsibility: str,
    role: str,
    phone_number: str,
    group_name: str,
) -> bool:
    success = False
    if (
        validate_field_length(responsibility, 50) and
        validate_alphanumeric_field(responsibility) and
        validate_phone_field(phone_number) and
        validate_email_address(email) and
        await validate_fluidattacks_staff_on_group(group_name, email, role)
    ):
        expiration_time = datetime_utils.get_as_epoch(
            datetime_utils.get_now_plus_delta(weeks=1)
        )
        url_token = secrets.token_urlsafe(64)
        success = await group_access_domain.update(
            email,
            group_name,
            {
                'expiration_time': expiration_time,
                'has_access': False,
                'invitation': {
                    'is_used': False,
                    'phone_number': phone_number,
                    'responsibility': responsibility,
                    'role': role,
                    'url_token': url_token,
                },

            }
        )
        description = await get_description(group_name.lower())
        group_url = f'{BASE_URL}/confirm_access/{url_token}'
        mail_to = [email]
        email_context: MailContentType = {
            'admin': email,
            'project': group_name,
            'project_description': description,
            'project_url': group_url,
        }
        schedule(mailer.send_mail_access_granted(mail_to, email_context))
    return success


async def is_alive(group: str) -> bool:
    return await group_dal.is_alive(group)


async def mask(group_name: str) -> bool:
    today = datetime_utils.get_now()
    comments = await group_comments_domain.get_comments(group_name)
    comments_result = all(
        await collect([
            group_dal.delete_comment(
                comment['project_name'],
                comment['user_id']
            )
            for comment in comments
        ])
    )
    update_data: Dict[str, Union[str, List[str], object]] = {
        'project_status': 'FINISHED',
        'deletion_date': datetime_utils.get_as_str(today)
    }
    is_group_finished = await group_dal.update(group_name, update_data)
    return comments_result and is_group_finished


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


async def update(group_name: str, data: GroupType) -> bool:
    return await group_dal.update(group_name, data)


async def update_tags(
    group_name: str,
    group_tags: GroupType,
    tags: List[str]
) -> bool:
    success: bool = False
    if not group_tags['tag']:
        group_tags = {'tag': set(tags)}
    else:
        cast(Set[str], group_tags.get('tag')).update(tags)
    success = await update(group_name, group_tags)
    if not success:
        LOGGER.error('Couldn\'t add tags', extra={'extra': locals()})
    return success


def validate_group_services_config(
    is_continuous_type: bool,
    has_drills: bool,
    has_forces: bool,
    has_integrates: bool,
) -> None:
    if is_continuous_type:
        if has_drills:
            if not has_integrates:
                raise InvalidProjectServicesConfig(
                    'Drills is only available when Integrates is too')

        if has_forces:
            if not has_integrates:
                raise InvalidProjectServicesConfig(
                    'Forces is only available when Integrates is too')
            if not has_drills:
                raise InvalidProjectServicesConfig(
                    'Forces is only available when Drills is too')

    else:
        if has_forces:
            raise InvalidProjectServicesConfig(
                'Forces is only available in projects of type Continuous')


async def validate_group_tags(group_name: str, tags: List[str]) -> List[str]:
    """Validate tags array."""
    pattern = re.compile('^[a-z0-9]+(?:-[a-z0-9]+)*$')
    if await _has_repeated_tags(group_name, tags):
        raise RepeatedValues()
    tags_validated = [tag for tag in tags if pattern.match(tag)]
    return tags_validated
