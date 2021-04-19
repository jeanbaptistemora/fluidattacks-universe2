# Standard libraries
import logging
import logging.config
import re
import secrets
from collections import defaultdict
from contextlib import AsyncExitStack
from datetime import date
from decimal import Decimal
from typing import (
    Any,
    Awaitable,
    cast,
    Dict,
    List,
    Optional,
    Set,
    Union,
)

# Third-party libraries
import bugsnag
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
from backend.dal.helpers.redis import redis_del_by_deps_soon
from backend.exceptions import (
    InvalidCommentParent,
    InvalidParameter,
    InvalidProjectName,
    InvalidProjectServicesConfig,
    RepeatedValues,
    UserNotInOrganization,
)
from backend.domain import project as group_domain
from backend.typing import (
    Comment as CommentType,
    Invitation as InvitationType,
    MailContent as MailContentType,
    Project as GroupType,
    ProjectAccess as GroupAccessType,
    User as UserType,
)
from events import domain as events_domain
from findings import domain as findings_domain
from group_access import domain as group_access_domain
from group_comments import domain as group_comments_domain
from names import domain as names_domain
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
    validate_fields,
    validate_fluidattacks_staff_on_group,
    validate_phone_field,
    validate_project_name,
    validate_string_length_between,
)
from notifications import domain as notifications_domain
from organizations import domain as orgs_domain
from resources import domain as resources_domain
from users import domain as users_domain
from __init__ import (
    BASE_URL,
    FI_DEFAULT_ORG,
)


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


async def complete_register_for_group_invitation(
    group_access: GroupAccessType
) -> bool:
    coroutines: List[Awaitable[bool]] = []
    success: bool = False
    invitation = cast(InvitationType, group_access['invitation'])
    if invitation['is_used']:
        bugsnag.notify(Exception('Token already used'), severity='warning')

    group_name = cast(str, group_access['project_name'])
    phone_number = cast(str, invitation['phone_number'])
    responsibility = cast(str, invitation['responsibility'])
    role = cast(str, invitation['role'])
    user_email = cast(str, group_access['user_email'])
    updated_invitation = invitation.copy()
    updated_invitation['is_used'] = True

    coroutines.extend([
        group_access_domain.update(
            user_email,
            group_name,
            {
                'expiration_time': None,
                'has_access': True,
                'invitation': updated_invitation,
                'responsibility': responsibility,
            }
        ),
        authz.grant_group_level_role(user_email, group_name, role)
    ])

    organization_id = await orgs_domain.get_id_for_group(group_name)
    if not await orgs_domain.has_user_access(organization_id, user_email):
        coroutines.append(
            orgs_domain.add_user(organization_id, user_email, 'customer')
        )

    if await users_domain.get_data(user_email, 'email'):
        coroutines.append(
            users_domain.add_phone_to_user(user_email, phone_number)
        )
    else:
        coroutines.append(
            users_domain.create(user_email, {'phone': phone_number})
        )

    if not await users_domain.is_registered(user_email):
        coroutines.extend([
            users_domain.register(user_email),
            authz.grant_user_level_role(user_email, 'customer')
        ])

    success = all(await collect(coroutines))
    if success:
        redis_del_by_deps_soon(
            'confirm_access',
            group_name=group_name,
            organization_id=organization_id,
        )
    return success


async def create_group(  # pylint: disable=too-many-arguments,too-many-locals
    user_email: str,
    user_role: str,
    group_name: str,
    organization: str,
    description: str,
    has_drills: bool = False,
    has_forces: bool = False,
    subscription: str = 'continuous',
    language: str = 'en',
) -> bool:
    validate_project_name(group_name)
    validate_fields([description])
    validate_field_length(group_name, 20)
    validate_field_length(description, 200)

    is_user_admin = user_role == 'admin'
    is_continuous_type = subscription == 'continuous'

    success: bool = False
    if description.strip() and group_name.strip():
        validate_group_services_config(
            is_continuous_type,
            has_drills,
            has_forces,
            has_integrates=True
        )
        is_group_avail, group_exists = await collect([
            names_domain.exists(group_name, 'group'),
            group_dal.exists(group_name)
        ])

        org_id = await orgs_domain.get_id_by_name(organization)
        if not await orgs_domain.has_user_access(org_id, user_email):
            raise UserNotInOrganization(org_id)

        if is_group_avail and not group_exists:
            group: GroupType = {
                'project_name': group_name,
                'description': description,
                'language': language,
                'historic_configuration': [{
                    'date': datetime_utils.get_now_as_str(),
                    'has_drills': has_drills,
                    'has_forces': has_forces,
                    'requester': user_email,
                    'type': subscription,
                }],
                'project_status': 'ACTIVE',
            }
            success = await group_dal.create(group)
            if success:
                await collect((
                    orgs_domain.add_group(org_id, group_name),
                    names_domain.remove(group_name, 'group')
                ))
                # Admins are not granted access to the project
                # they are omnipresent
                if not is_user_admin:
                    success = (
                        success and
                        all(
                            await collect((
                                group_access_domain.update_has_access(
                                    user_email,
                                    group_name,
                                    True
                                ),
                                authz.grant_group_level_role(
                                    user_email,
                                    group_name,
                                    'group_manager'
                                )
                            ))
                        )
                    )
        else:
            raise InvalidProjectName()
    else:
        raise InvalidParameter()
    # Notify us in case the user wants any Fluid Service
    if success and (has_drills or has_forces):
        await notifications_domain.new_group(
            description=description,
            group_name=group_name,
            has_drills=has_drills,
            has_forces=has_forces,
            requester_email=user_email,
            subscription=subscription,
        )
    return success


async def create_without_group(
    email: str,
    role: str,
    phone_number: str = '',
    should_add_default_org: bool = True,
) -> bool:
    success = False
    if (
        validate_phone_field(phone_number) and
        validate_email_address(email)
    ):
        new_user_data: UserType = {}
        new_user_data['email'] = email
        new_user_data['authorized'] = True
        new_user_data['registered'] = True
        if phone_number:
            new_user_data['phone'] = phone_number

        success = all(
            await collect([
                authz.grant_user_level_role(email, role),
                users_domain.create(email, new_user_data)
            ])
        )
        org = await orgs_domain.get_or_create(FI_DEFAULT_ORG)
        if (
            should_add_default_org and
            not await orgs_domain.has_user_access(str(org['id']), email)
        ):
            await orgs_domain.add_user(str(org['id']), email, 'customer')
    return success


async def edit(
    *,
    context: Any,
    comments: str,
    group_name: str,
    has_drills: bool,
    has_forces: bool,
    has_integrates: bool,
    reason: str,
    requester_email: str,
    subscription: str,
) -> bool:
    success: bool = False
    is_continuous_type: bool = subscription == 'continuous'

    validate_fields([comments])
    validate_string_length_between(comments, 0, 250)
    validate_group_services_config(
        is_continuous_type,
        has_drills,
        has_forces,
        has_integrates)

    item = await group_dal.get_attributes(
        project_name=group_name,
        attributes=[
            'historic_configuration',
            'project_name'
        ]
    )
    item.setdefault('historic_configuration', [])

    if item.get('project_name'):
        success = await group_dal.update(
            data={
                'historic_configuration': cast(
                    List[Dict[str, Union[bool, str]]],
                    item['historic_configuration']
                ) +
                [{
                    'comments': comments,
                    'date': datetime_utils.get_now_as_str(),
                    'has_drills': has_drills,
                    'has_forces': has_forces,
                    'reason': reason,
                    'requester': requester_email,
                    'type': subscription,
                }],
            },
            project_name=group_name,
        )

    if not has_integrates:
        group_loader = context.group_all
        group = await group_loader.load(group_name)
        org_id = group['organization']
        success = (
            success and
            await orgs_domain.remove_group(
                context,
                organization_id=org_id,
                group_name=group_name,
                email=requester_email,
            )
        )

    if success and has_integrates:
        await notifications_domain.edit_group(
            comments=comments,
            group_name=group_name,
            had_drills=(
                cast(
                    bool,
                    cast(
                        List[Dict[str, Union[bool, str]]],
                        item['historic_configuration']
                    )[-1]['has_drills']
                )
                if item['historic_configuration'] else False
            ),
            had_forces=(
                cast(
                    bool,
                    cast(
                        List[Dict[str, Union[bool, str]]],
                        item['historic_configuration']
                    )[-1]['has_forces']
                )
                if item['historic_configuration'] else False
            ),
            had_integrates=True,
            has_drills=has_drills,
            has_forces=has_forces,
            has_integrates=has_integrates,
            reason=reason,
            requester_email=requester_email,
            subscription=subscription,
        )
    elif success and not has_integrates:
        await notifications_domain.delete_group(
            deletion_date=datetime_utils.get_now_as_str(),
            group_name=group_name,
            requester_email=requester_email,
        )
    return success


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


async def get_closed_vulnerabilities(context: Any, group_name: str) -> int:
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
    closed_vulnerabilities = 0
    for status in last_approved_status:
        if status == 'closed':
            closed_vulnerabilities += 1
    return closed_vulnerabilities


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


async def get_open_finding(context: Any, group_name: str) -> int:
    finding_vulns_loader = context.finding_vulns_nzr
    group_findings_loader = context.group_findings

    group_findings = await group_findings_loader.load(group_name)
    vulns = await finding_vulns_loader.load_many_chained([
        finding['finding_id'] for finding in group_findings
    ])

    finding_vulns_dict = defaultdict(list)
    for vuln in vulns:
        finding_vulns_dict[vuln['finding_id']].append(vuln)
    finding_vulns = list(finding_vulns_dict.values())
    return await vulns_utils.get_open_findings(finding_vulns)


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


async def remove_resources(context: Any, group_name: str) -> bool:
    are_users_removed = await group_domain.remove_all_users_access(
        context,
        group_name
    )
    group_findings = await findings_domain.list_findings(
        context,
        [group_name],
        include_deleted=True
    )
    group_drafts = await findings_domain.list_drafts(
        [group_name],
        include_deleted=True
    )
    findings_and_drafts = group_findings[0] + group_drafts[0]
    are_findings_masked = all(
        await collect(
            findings_domain.mask_finding(context, finding_id)
            for finding_id in findings_and_drafts
        )
    )
    events = await events_domain.list_group_events(group_name)
    are_events_masked = all(
        await collect(
            events_domain.mask(event_id)
            for event_id in events
        )
    )
    is_group_masked = await mask(group_name)
    are_resources_masked = all(
        list(
            cast(List[bool], await resources_domain.mask(group_name))
        )
    )
    response = all([
        are_findings_masked,
        are_users_removed,
        is_group_masked,
        are_events_masked,
        are_resources_masked
    ])
    return response


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


async def update_pending_deletion_date(
    group_name: str,
    pending_deletion_date: Optional[str]
) -> bool:
    """ Update pending deletion date """
    values: GroupType = {'pending_deletion_date': pending_deletion_date}
    success = await update(group_name, values)
    return success


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
