# pylint:disable=cyclic-import,too-many-lines
"""Domain functions for projects."""

import logging
import re
from collections import defaultdict
from contextlib import AsyncExitStack
from datetime import date
from decimal import Decimal
from itertools import chain
from typing import (
    Any,
    cast,
    Dict,
    List,
    Tuple,
    Union,
    Optional
)

import simplejson as json
from aioextensions import (
    collect,
    in_process,
    schedule,
)
from graphql.type.definition import GraphQLResolveInfo

from back.settings import LOGGING
from backend import (
    authz,
    mailer,
)
from backend.authz.policy import get_group_level_role
from backend.dal import project as project_dal
from backend.dal.helpers.dynamodb import start_context
from backend.domain import (
    resources as resources_domain,
    finding as finding_domain,
    user as user_domain,
    notifications as notifications_domain,
    organization as org_domain,
    vulnerability as vuln_domain,
    available_name as available_name_domain
)
from backend.exceptions import (
    AlreadyPendingDeletion,
    GroupNotFound,
    InvalidCommentParent,
    InvalidParameter,
    InvalidProjectName,
    InvalidProjectServicesConfig,
    RepeatedValues,
    UserNotInOrganization
)
from backend.filters import stakeholder as stakeholder_filters
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    Historic as HistoricType,
    Invitation as InvitationType,
    Stakeholder as StakeholderType,
    Project as ProjectType,
    ProjectAccess as ProjectAccessType,
    Vulnerability as VulnerabilityType
)
from comments import domain as comments_domain
from events import domain as events_domain
from newutils import (
    comments as comments_utils,
    datetime as datetime_utils,
    findings as finding_utils,
    stakeholders as stakeholders_utils,
    validations,
)


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def add_comment(
    info: GraphQLResolveInfo,
    project_name: str,
    email: str,
    comment_data: CommentType
) -> bool:
    """Add comment in a project."""
    parent = str(comment_data['parent'])
    content = str(comment_data['content'])
    await comments_utils.validate_handle_comment_scope(
        content,
        email,
        project_name,
        parent,
        info.context.store
    )
    if parent != '0':
        project_comments = [
            str(comment.get('user_id'))
            for comment in await project_dal.get_comments(
                project_name
            )
        ]
        if parent not in project_comments:
            raise InvalidCommentParent()
    return await project_dal.add_comment(project_name, email, comment_data)


def send_comment_mail(
    user_email: str,
    comment_data: CommentType,
    project_name: str
) -> None:
    schedule(
        mailer.send_comment_mail(
            comment_data,
            'project',
            user_email,
            'project',
            project_name
        )
    )


def validate_project_services_config(
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


async def create_group(  # pylint: disable=too-many-arguments,too-many-locals
    user_email: str,
    user_role: str,
    project_name: str,
    organization: str,
    description: str,
    has_drills: bool = False,
    has_forces: bool = False,
    subscription: str = 'continuous',
    language: str = 'en',
) -> bool:
    validations.validate_project_name(project_name)
    validations.validate_fields([description])
    validations.validate_field_length(project_name, 20)
    validations.validate_field_length(description, 200)
    is_user_admin = user_role == 'admin'

    is_continuous_type = subscription == 'continuous'

    success: bool = False

    if description.strip() and project_name.strip():

        validate_project_services_config(
            is_continuous_type,
            has_drills,
            has_forces,
            has_integrates=True)

        is_group_avail, group_exists = await collect([
            available_name_domain.exists(project_name, 'group'),
            project_dal.exists(project_name)
        ])

        org_id = await org_domain.get_id_by_name(organization)
        if not await org_domain.has_user_access(org_id, user_email):
            raise UserNotInOrganization(org_id)

        if is_group_avail and not group_exists:
            project: ProjectType = {
                'project_name': project_name,
                'description': description,
                'language': language,
                'historic_configuration': [{
                    'date': datetime_utils.get_as_str(
                        datetime_utils.get_now()
                    ),
                    'has_drills': has_drills,
                    'has_forces': has_forces,
                    'requester': user_email,
                    'type': subscription,
                }],
                'project_status': 'ACTIVE',
            }

            success = await project_dal.create(project)
            if success:
                await collect((
                    org_domain.add_group(org_id, project_name),
                    available_name_domain.remove(project_name, 'group')
                ))
                # Admins are not granted access to the project
                # they are omnipresent
                if not is_user_admin:
                    success = success and all(await collect((
                        update_has_access(
                            user_email,
                            project_name,
                            True
                        ),
                        authz.grant_group_level_role(
                            user_email, project_name,
                            'group_manager'
                        )))
                    )

        else:
            raise InvalidProjectName()
    else:
        raise InvalidParameter()

    # Notify us in case the user wants any Fluid Service
    if success and (has_drills or has_forces):
        await notifications_domain.new_group(
            description=description,
            group_name=project_name,
            has_drills=has_drills,
            has_forces=has_forces,
            requester_email=user_email,
            subscription=subscription,
        )

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

    validations.validate_fields([comments])
    validations.validate_string_length_between(comments, 0, 250)
    validate_project_services_config(
        is_continuous_type,
        has_drills,
        has_forces,
        has_integrates)

    item = await project_dal.get_attributes(
        project_name=group_name,
        attributes=[
            'historic_configuration',
            'project_name'
        ]
    )
    item.setdefault('historic_configuration', [])

    if item.get('project_name'):
        success = await project_dal.update(
            data={
                'historic_configuration': cast(
                    List[Dict[str, Union[bool, str]]],
                    item['historic_configuration']
                ) + [{
                    'comments': comments,
                    'date': datetime_utils.get_as_str(
                        datetime_utils.get_now()
                    ),
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
        success = success and await org_domain.remove_group(
            context,
            organization_id=org_id,
            group_name=group_name,
            email=requester_email,
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
            deletion_date=datetime_utils.get_as_str(
                datetime_utils.get_now()
            ),
            group_name=group_name,
            requester_email=requester_email,
        )

    return success


async def update_access(
    user_email: str,
    group_name: str,
    data: ProjectAccessType
) -> bool:
    return await project_dal.update_access(
        user_email, group_name, data
    )


async def update_has_access(
    user_email: str,
    group_name: str,
    access: bool
) -> bool:
    return await update_access(
        user_email, group_name, {'has_access': access}
    )


async def add_user_access(email: str, group: str, role: str) -> bool:
    return (
        await update_has_access(email, group, True) and
        await authz.grant_group_level_role(email, group, role)
    )


async def remove_access(user_email: str, project_name: str) -> bool:
    return await project_dal.remove_access(user_email, project_name)


async def get_historic_deletion(project_name: str) -> HistoricType:
    historic_deletion = await project_dal.get_attributes(
        project_name.lower(), ['historic_deletion'])
    return cast(HistoricType, historic_deletion.get('historic_deletion', []))


async def remove_resources(context: Any, project_name: str) -> bool:
    are_users_removed = await remove_all_users_access(context, project_name)
    group_findings = await finding_domain.list_findings(
        context,
        [project_name],
        include_deleted=True
    )
    group_drafts = await finding_domain.list_drafts(
        [project_name], include_deleted=True
    )
    findings_and_drafts = (
        group_findings[0] + group_drafts[0]
    )
    are_findings_masked = all(await collect(
        finding_domain.mask_finding(context, finding_id)
        for finding_id in findings_and_drafts
    ))
    events = await list_events(project_name)
    are_events_masked = all(await collect(
        events_domain.mask(event_id)
        for event_id in events
    ))
    is_group_masked = await mask(project_name)
    are_resources_masked = all(
        list(
            cast(List[bool], await resources_domain.mask(project_name))
        )
    )

    response = all(
        [
            are_findings_masked,
            are_users_removed,
            is_group_masked,
            are_events_masked,
            are_resources_masked
        ]
    )

    return response


async def delete_project(
    context: Any,
    project_name: str,
    user_email: str
) -> bool:
    response = False
    data = await project_dal.get_attributes(
        project_name,
        ['project_status', 'historic_deletion']
    )
    historic_deletion = cast(
        List[Dict[str, str]],
        data.get('historic_deletion', [])
    )
    if data.get('project_status') != 'DELETED':
        all_resources_removed = await remove_resources(context, project_name)
        today = datetime_utils.get_now()
        new_state = {
            'date': datetime_utils.get_as_str(today),
            'deletion_date': datetime_utils.get_as_str(today),
            'user': user_email.lower(),
        }
        historic_deletion.append(new_state)
        new_data: ProjectType = {
            'historic_deletion': historic_deletion,
            'project_status': 'DELETED'
        }
        response = all(
            [
                all_resources_removed,
                await project_dal.update(project_name, new_data)
            ]
        )
    else:
        raise AlreadyPendingDeletion()

    if response:
        await authz.revoke_cached_group_service_attributes_policies(
            project_name
        )

    return response


async def mask(group_name: str) -> bool:
    today = datetime_utils.get_now()
    comments = await project_dal.get_comments(group_name)
    comments_result = all(await collect([
        project_dal.delete_comment(comment['project_name'], comment['user_id'])
        for comment in comments
    ]))

    update_data: Dict[str, Union[str, List[str], object]] = {
        'project_status': 'FINISHED',
        'deletion_date': datetime_utils.get_as_str(today)
    }
    is_group_finished = await project_dal.update(
        group_name, update_data
    )
    return comments_result and is_group_finished


async def remove_all_users_access(context: Any, project: str) -> bool:
    """Remove user access to project."""
    user_active, user_suspended = await collect([
        get_users(project, True),
        get_users(project, False)
    ])
    all_users = user_active + user_suspended
    are_users_removed = all(await collect([
        remove_user_access(context, project, user)
        for user in all_users
    ]))

    return are_users_removed


async def remove_user_access(
    context: Any,
    group_name: str,
    email: str,
    check_org_access: bool = True
) -> bool:
    """Remove user access to project."""
    success: bool = all(
        await collect([
            authz.revoke_group_level_role(email, group_name),
            remove_access(email, group_name)
        ])
    )
    if success and check_org_access:
        group_loader = context.group
        group = await group_loader.load(group_name)
        org_id = group['organization']
        has_org_access = await org_domain.has_user_access(org_id, email)
        has_groups_in_org = bool(
            await user_domain.get_projects(email, organization_id=org_id)
        )
        if has_org_access and not has_groups_in_org:
            success = success and await org_domain.remove_user(
                context,
                org_id,
                email
            )

        has_groups = bool(
            await user_domain.get_projects(email)
        )
        if not has_groups:
            success = success and await stakeholders_utils.remove(email)

    return success


async def _has_repeated_tags(project_name: str, tags: List[str]) -> bool:
    has_repeated_inputs = len(tags) != len(set(tags))

    project_info = await get_attributes(
        project_name.lower(), ['tag'])
    existing_tags = project_info.get('tag', [])
    all_tags = list(existing_tags) + tags
    has_repeated_tags = len(all_tags) != len(set(all_tags))

    return has_repeated_inputs or has_repeated_tags


async def validate_tags(project_name: str, tags: List[str]) -> List[str]:
    """Validate tags array."""
    tags_validated = []
    pattern = re.compile('^[a-z0-9]+(?:-[a-z0-9]+)*$')
    if await _has_repeated_tags(project_name, tags):
        raise RepeatedValues()

    for tag in tags:
        if pattern.match(tag):
            tags_validated.append(tag)
        else:
            # Invalid tag
            pass
    return tags_validated


async def is_alive(project: str) -> bool:
    return await project_dal.is_alive(project)


async def total_vulnerabilities(
    context: Any,
    finding_id: str
) -> Dict[str, int]:
    """Get total vulnerabilities in new format."""
    finding = {'openVulnerabilities': 0, 'closedVulnerabilities': 0}
    finding_vulns_loader = context.finding_vulns
    if await finding_domain.validate_finding(finding_id):
        vulnerabilities = await finding_vulns_loader.load(finding_id)
        last_approved_status = await collect([
            in_process(vuln_domain.get_last_status, vuln)
            for vuln in vulnerabilities
        ])
        for current_state in last_approved_status:
            if current_state == 'open':
                finding['openVulnerabilities'] += 1
            elif current_state == 'closed':
                finding['closedVulnerabilities'] += 1
            else:
                # Vulnerability does not have a valid state
                pass
    return finding


async def get_pending_verification_findings(
    context: Any,
    project_name: str
) -> List[Dict[str, FindingType]]:
    """Gets findings pending for verification"""
    findings_ids = await finding_domain.list_findings(
        context,
        [project_name]
    )
    are_pending_verifications = await collect([
        finding_domain.is_pending_verification(context, finding_id)
        for finding_id in findings_ids[0]
    ])
    pending_to_verify_ids = [
        finding_id
        for finding_id, are_pending_verification in zip(
            findings_ids[0],
            are_pending_verifications
        )
        if are_pending_verification
    ]
    pending_to_verify = await collect(
        finding_utils.get_attributes(
            finding_id,
            ['finding', 'finding_id', 'project_name']
        ) for finding_id in pending_to_verify_ids
    )

    return cast(List[Dict[str, FindingType]], pending_to_verify)


async def get_pending_closing_check(context: Any, project: str) -> int:
    """Check for pending closing checks."""
    pending_closing = len(
        await get_pending_verification_findings(context, project))
    return pending_closing


async def get_last_closing_vuln_info(
    context: Any,
    findings: List[Dict[str, FindingType]]
) -> Tuple[Decimal, VulnerabilityType]:
    """Get day since last vulnerability closing."""
    finding_vulns_loader = context.finding_vulns_nzr

    validate_findings = await collect(
        finding_domain.validate_finding(str(finding['finding_id']))
        for finding in findings
    )
    validated_findings = [
        finding for finding, is_valid in zip(findings, validate_findings)
        if is_valid
    ]
    vulns = await finding_vulns_loader.load_many_chained([
        str(finding['finding_id']) for finding in validated_findings
    ])
    are_vuln_closed = await collect([
        in_process(is_vulnerability_closed, vuln)
        for vuln in vulns
    ])
    closed_vulns = [
        vuln
        for vuln, is_vuln_closed in zip(vulns, are_vuln_closed)
        if is_vuln_closed
    ]
    closing_vuln_dates = await collect([
        in_process(get_last_closing_date, vuln)
        for vuln in closed_vulns
    ])
    if closing_vuln_dates:
        current_date, date_index = max(
            (v, i)
            for i, v in enumerate(closing_vuln_dates)
        )
        last_closing_vuln = closed_vulns[date_index]
        current_date = max(closing_vuln_dates)
        last_closing_days = (
            Decimal((datetime_utils.get_now().date() - current_date).days)
            .quantize(Decimal('0.1'))
        )
    else:
        last_closing_days = Decimal(0)
        last_closing_vuln = {}
    return last_closing_days, cast(VulnerabilityType, last_closing_vuln)


def get_last_closing_date(
    vulnerability: Dict[str, FindingType],
    min_date: Optional[date] = None
) -> Optional[date]:
    """Get last closing date of a vulnerability."""
    current_state = vuln_domain.get_last_approved_state(vulnerability)
    last_closing_date = None

    if current_state and current_state.get('state') == 'closed':
        last_closing_date = datetime_utils.get_from_str(
            current_state.get('date', '').split(' ')[0],
            date_format='%Y-%m-%d'
        ).date()

        if min_date and min_date > last_closing_date:
            return None

    return last_closing_date


def is_vulnerability_closed(vuln: Dict[str, FindingType]) -> bool:
    """Return if a vulnerability is closed."""
    return vuln_domain.get_last_status(vuln) == 'closed'


async def get_max_open_severity(
    context: Any,
    findings: List[Dict[str, FindingType]]
) -> Tuple[Decimal, Dict[str, FindingType]]:
    """Get maximum severity of project with open vulnerabilities."""
    total_vulns = await collect(
        total_vulnerabilities(context, str(fin.get('finding_id', '')))
        for fin in findings
    )
    opened_findings = [
        finding
        for finding, total_vuln in zip(findings, total_vulns)
        if int(total_vuln.get('openVulnerabilities', '')) > 0
    ]
    total_severity: List[float] = cast(
        List[float],
        [
            finding.get('cvss_temporal', '')
            for finding in opened_findings
        ]
    )
    if total_severity:
        severity, severity_index = max(
            (v, i)
            for i, v in enumerate(total_severity)
        )
        max_severity = Decimal(severity).quantize(Decimal('0.1'))
        max_severity_finding = opened_findings[severity_index]
    else:
        max_severity = Decimal(0).quantize(Decimal('0.1'))
        max_severity_finding = {}
    return max_severity, max_severity_finding


def get_open_vulnerability_date(
    vulnerability: Dict[str, FindingType],
    min_date: Optional[date] = None
) -> Optional[date]:
    """Get open vulnerability date of a vulnerability."""
    all_states = cast(
        List[Dict[str, str]],
        vulnerability.get('historic_state', [{}])
    )
    open_states = [state for state in all_states if state['state'] == 'open']
    if open_states:
        open_vulnerability_date = datetime_utils.get_from_str(
            open_states[-1]['date'].split(' ')[0],
            date_format='%Y-%m-%d'
        ).date()

        if min_date and min_date > open_vulnerability_date:
            return None

        return open_vulnerability_date

    return None


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

    return await get_mean_remediate_vulnerabilities(vulns, min_date)


async def get_mean_remediate_vulnerabilities(
    vulns: List[Dict[str, FindingType]],
    min_date: Optional[date] = None
) -> Decimal:
    """Get mean time to remediate a vulnerability."""
    total_vuln = 0
    total_days = 0
    open_vuln_dates = await collect(
        in_process(get_open_vulnerability_date, vuln, min_date)
        for vuln in vulns
    )
    filtered_open_vuln_dates = [
        vuln
        for vuln in open_vuln_dates
        if vuln
    ]
    closed_vuln_dates = await collect(
        in_process(get_last_closing_date, vuln, min_date)
        for vuln, open_vuln in zip(vulns, open_vuln_dates)
        if open_vuln
    )
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


async def get_mean_remediate_severity(  # pylint: disable=too-many-locals
    context: Any,
    project_name: str,
    min_severity: float,
    max_severity: float
) -> Decimal:
    """Get mean time to remediate."""
    total_days = 0
    finding_vulns_loader = context.finding_vulns_nzr
    group_findings_loader = context.group_findings

    group_findings = await group_findings_loader.load(project_name.lower())
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
        in_process(get_open_vulnerability_date, vuln)
        for vuln in findings_vulns
    ])
    filtered_open_vuln_dates = [
        vuln for vuln in open_vuln_dates
        if vuln
    ]
    closed_vuln_dates = await collect([
        in_process(get_last_closing_date, vuln)
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


async def get_total_treatment(
    context: Any,
    findings: List[Dict[str, FindingType]]
) -> Dict[str, int]:
    """Get the total treatment of all the vulnerabilities"""
    accepted_vuln: int = 0
    indefinitely_accepted_vuln: int = 0
    in_progress_vuln: int = 0
    undefined_treatment: int = 0
    finding_vulns_loader = context.finding_vulns_nzr

    validate_findings = await collect(
        finding_domain.validate_finding(str(finding['finding_id']))
        for finding in findings
    )
    validated_findings = [
        finding
        for finding, validate_finding in zip(findings, validate_findings)
        if validate_finding
    ]
    vulns = await finding_vulns_loader.load_many_chained([
        str(finding['finding_id']) for finding in validated_findings
    ])

    for vuln in vulns:
        vuln_treatment = cast(
            List[Dict[str, str]],
            vuln.get('historic_treatment', [{}])
        )[-1].get('treatment')
        current_state = vuln_domain.get_last_status(vuln)
        open_vulns: int = 1 if current_state == 'open' else 0
        if vuln_treatment == 'ACCEPTED':
            accepted_vuln += open_vulns
        elif vuln_treatment == 'ACCEPTED_UNDEFINED':
            indefinitely_accepted_vuln += open_vulns
        elif vuln_treatment == 'IN PROGRESS':
            in_progress_vuln += open_vulns
        else:
            undefined_treatment += open_vulns
    treatment = {
        'accepted': accepted_vuln,
        'acceptedUndefined': indefinitely_accepted_vuln,
        'inProgress': in_progress_vuln,
        'undefined': undefined_treatment
    }
    return treatment


async def get_mean_remediate_non_treated(
    group_name: str,
    min_date: Optional[date] = None
) -> Decimal:
    findings = await finding_domain.get_findings_by_group(group_name)
    vulnerabilities = await vuln_domain.list_vulnerabilities_async(
        [str(finding['finding_id']) for finding in findings],
        include_requested_zero_risk=True,
    )

    return await get_mean_remediate_vulnerabilities(
        [
            vuln for vuln in vulnerabilities
            if not vuln_domain.is_accepted_undefined_vulnerability(vuln)
        ],
        min_date
    )


async def get_closers(
        project_name: str,
        active: bool = True) -> List[str]:
    users = await get_users(project_name, active)
    user_roles = await collect(
        get_group_level_role(user, project_name)
        for user in users
    )
    return [
        str(user)
        for user, user_role in zip(users, user_roles)
        if user_role == 'closer'
    ]


async def get_open_findings(
        finding_vulns: List[List[Dict[str, FindingType]]]) -> int:
    last_approved_status = await collect(
        in_process(vuln_domain.get_last_status, vuln)
        for vulns in finding_vulns
        for vuln in vulns
    )
    open_findings = [
        vulns
        for vulns, last_approved in zip(finding_vulns, last_approved_status)
        if [
            vuln for vuln in vulns
            if last_approved == 'open'
        ]
    ]
    return len(open_findings)


async def update(project_name: str, data: ProjectType) -> bool:
    return await project_dal.update(project_name, data)


def _is_scope_comment(comment: CommentType):
    return str(comment['content']).strip() not in {'#external', '#internal'}


async def list_comments(
        project_name: str,
        user_email: str) -> List[CommentType]:
    enforcer = await authz.get_group_level_enforcer(user_email)

    comments = await collect([
        comments_domain.fill_comment_data(project_name, user_email, comment)
        for comment in await project_dal.get_comments(project_name)
    ])

    new_comments: List[CommentType] = []

    if enforcer(project_name, 'handle_comment_scope'):
        new_comments = cast(
            List[CommentType],
            comments
        )
    else:
        new_comments = cast(
            List[CommentType],
            list(filter(_is_scope_comment, comments))
        )

    return cast(List[CommentType], new_comments)


async def get_active_projects() -> List[str]:
    projects = await project_dal.get_active_projects()

    return projects


async def get_groups_with_forces() -> List[str]:
    return await project_dal.get_groups_with_forces()


async def get_alive_groups(
    attributes: List[str] = None
) -> List[ProjectType]:
    data_attr = ','.join(attributes or [])
    projects = await project_dal.get_alive_groups(data_attr)

    return projects


async def get_alive_group_names() -> List[str]:
    attributes = {'project_name'}
    groups = await get_alive_groups(attributes)

    return cast(
        List[str],
        [group['project_name'] for group in groups]
    )


async def list_events(project_name: str) -> List[str]:
    """ Returns the list of event ids associated with the project"""
    return await project_dal.list_events(project_name)


async def get_attributes(
        project_name: str,
        attributes: List[str]) -> Dict[str, Union[str, List[str]]]:
    return await project_dal.get_attributes(project_name, attributes)


async def get_all(attributes: List[str] = None) -> List[ProjectType]:
    data_attr = ','.join(attributes or [])
    return await project_dal.get_all(data_attr=data_attr)


async def get_description(project_name: str) -> str:
    return await project_dal.get_description(project_name)


async def get_users(project_name: str, active: bool = True) -> List[str]:
    return await project_dal.get_users(project_name, active)


async def get_many_groups(
        groups_name: List[str]) -> List[ProjectType]:
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(project_dal.TABLE_NAME)
        groups = await collect(
            project_dal.get_group(group_name, table)
            for group_name in groups_name
        )
    return cast(List[ProjectType], groups)


async def get_users_to_notify(
        project_name: str,
        active: bool = True) -> List[str]:
    users = await get_users(project_name, active)
    user_roles = await collect(
        get_group_level_role(user, project_name)
        for user in users
    )
    return [
        str(user)
        for user, user_role in zip(users, user_roles)
        if user_role != 'executive'
    ]


async def get_managers(project_name: str) -> List[str]:
    users = await get_users(project_name, active=True)
    users_roles = await collect([
        authz.get_group_level_role(user, project_name)
        for user in users
    ])
    return [
        user_email
        for user_email, role in zip(users, users_roles)
        if role == 'customeradmin'
    ]


async def get_open_vulnerabilities(context: Any, group_name: str) -> int:
    group_findings_loader = context.group_findings
    group_findings_loader.clear(group_name)
    finding_vulns_loader = context.finding_vulns_nzr

    group_findings = await group_findings_loader.load(group_name)
    findings_vulns = await finding_vulns_loader.load_many_chained([
        finding['finding_id'] for finding in group_findings
    ])

    last_approved_status = await collect([
        in_process(vuln_domain.get_last_status, vuln)
        for vuln in findings_vulns
    ])
    open_vulnerabilities = 0
    for status in last_approved_status:
        if status == 'open':
            open_vulnerabilities += 1
    return open_vulnerabilities


async def get_closed_vulnerabilities(context: Any, group_name: str) -> int:
    group_findings_loader = context.group_findings
    group_findings_loader.clear(group_name)
    finding_vulns_loader = context.finding_vulns_nzr

    group_findings = await group_findings_loader.load(group_name)
    findings_vulns = await finding_vulns_loader.load_many_chained([
        finding['finding_id'] for finding in group_findings
    ])

    last_approved_status = await collect([
        in_process(vuln_domain.get_last_status, vuln)
        for vuln in findings_vulns
    ])
    closed_vulnerabilities = 0
    for status in last_approved_status:
        if status == 'closed':
            closed_vulnerabilities += 1
    return closed_vulnerabilities


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
    return await get_open_findings(finding_vulns)


async def get_by_name(name: str) -> ProjectType:
    group: dict = await project_dal.get_attributes(name)

    if group and 'deletion_date' not in group:
        return {
            'closed_vulnerabilities': group.get('closed_vulnerabilities', 0),
            'deletion_date': (
                group['historic_deletion'][-1].get('deletion_date', '')
                if 'historic_deletion' in group else ''
            ),
            'description': group.get('description', ''),
            'has_drills': group['historic_configuration'][-1]['has_drills'],
            'has_forces': group['historic_configuration'][-1]['has_forces'],
            'has_integrates': group['project_status'] == 'ACTIVE',
            'last_closing_vuln': group.get('last_closing_date', 0),
            'last_closing_vuln_finding': group.get(
                'last_closing_vuln_finding'
            ),
            'max_open_severity': group.get('max_open_severity', 0),
            'max_open_severity_finding': group.get(
                'max_open_severity_finding'
            ),
            'mean_remediate_critical_severity': group.get(
                'mean_remediate_critical_severity',
                0
            ),
            'mean_remediate_high_severity': group.get(
                'mean_remediate_high_severity',
                0
            ),
            'mean_remediate_low_severity': group.get(
                'mean_remediate_low_severity',
                0
            ),
            'mean_remediate_medium_severity': group.get(
                'mean_remediate_medium_severity',
                0
            ),
            'mean_remediate': group.get('mean_remediate', 0),
            'name': group['project_name'],
            'open_findings': group.get('open_findings', 0),
            'open_vulnerabilities': group.get('open_vulnerabilities', 0),
            'subscription': group['historic_configuration'][-1]['type'],
            'tags': group.get('tag', []),
            'total_treatment': json.dumps(
                group.get('total_treatment', {}),
                use_decimal=True
            ),
            'user_deletion': (
                group['historic_deletion'][-1].get('user', '')
                if 'historic_deletion' in group else ''
            )
        }

    raise GroupNotFound()


async def get_user_access(email: str, group_name: str) -> ProjectAccessType:
    access: List[Dict[str, ProjectType]] = \
        await project_dal.get_user_access(email, group_name)

    return cast(ProjectAccessType, access[0]) if access else {}


async def get_access_by_url_token(url_token: str) -> ProjectAccessType:
    access: List[Dict[str, ProjectType]] = \
        await project_dal.get_access_by_url_token(url_token)

    return cast(ProjectAccessType, access[0]) if access else {}


async def format_stakeholder(
    email: str,
    group_name: str
) -> StakeholderType:
    stakeholder: StakeholderType = await user_domain.get_by_email(email)
    project_access = await get_user_access(
        email,
        group_name
    )
    invitation = cast(InvitationType, project_access.get('invitation'))
    invitation_state = (
        'PENDING' if invitation and not invitation['is_used'] else
        'UNREGISTERED' if not stakeholder.get('is_registered', False) else
        'CONFIRMED'
    )
    if invitation_state == 'PENDING':
        responsibility = invitation['responsibility']
        group_role = invitation['role']
        phone_number = invitation['phone_number']
    else:
        responsibility = cast(str, project_access.get('responsibility', ''))
        group_role = await authz.get_group_level_role(email, group_name)
        phone_number = cast(str, stakeholder['phone_number'])

    return {
        **stakeholder,
        'responsibility': responsibility,
        'invitation_state': invitation_state,
        'phone_number': phone_number,
        'role': group_role
    }


async def get_stakeholders(
    group_name: str,
    exclude_fluid_staff: bool = False,
) -> List[StakeholderType]:
    group_stakeholders_emails = cast(List[str], list(chain.from_iterable(
        await collect([
            get_users(group_name),
            get_users(group_name, False)
        ])
    )))

    if exclude_fluid_staff:
        group_stakeholders_emails = (
            await stakeholder_filters.filter_non_fluid_staff(
                group_stakeholders_emails,
                group_name
            )
        )

    group_stakeholders = cast(
        List[StakeholderType],
        await collect(
            format_stakeholder(email, group_name)
            for email in group_stakeholders_emails
        )
    )

    return group_stakeholders


async def update_pending_deletion_date(
    group_name: str,
    pending_deletion_date: Optional[str]
) -> bool:
    """ Update pending deletion date """
    values: ProjectType = {
        'pending_deletion_date': pending_deletion_date
    }
    success = await project_dal.update(
        group_name,
        values
    )

    return success
