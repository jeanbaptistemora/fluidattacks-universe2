# pylint:disable=cyclic-import,too-many-lines
"""Domain functions for projects."""

import logging
import re
from collections import namedtuple, defaultdict
from contextlib import AsyncExitStack
from datetime import date
from decimal import Decimal
from typing import Dict, List, NamedTuple, Tuple, Union, cast, Optional

import simplejson as json
from aioextensions import (
    collect,
    in_process,
    schedule,
)

from backend.authz.policy import get_group_level_role
from backend.dal.helpers.dynamodb import start_context
from backend.dal import (
    finding as finding_dal,
    project as project_dal
)
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    Historic as HistoricType,
    Project as ProjectType,
    Vulnerability as VulnerabilityType
)
from backend.domain import (
    comment as comment_domain,
    resources as resources_domain,
    finding as finding_domain,
    user as user_domain,
    notifications as notifications_domain,
    event as event_domain,
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
    NotPendingDeletion,
    PermissionDenied,
    RepeatedValues,
    UserNotInOrganization
)
from backend.utils import (
    datetime as datetime_utils,
    findings as finding_utils,
    validations
)
from backend import authz, mailer
from fluidintegrates.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def add_comment(
        project_name: str,
        email: str,
        comment_data: CommentType) -> bool:
    """Add comment in a project."""
    parent = str(comment_data.get('parent'))
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


async def create_project(  # pylint: disable=too-many-arguments
    user_email: str,
    user_role: str,
    project_name: str,
    organization: str,
    description: str,
    has_drills: bool = False,
    has_forces: bool = False,
    subscription: str = 'continuous'
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
                    user_role = {
                        # Internal managers are turned into group_managers
                        'internal_manager': 'group_manager'
                        # Other roles are turned into customeradmins
                    }.get(user_role, 'customeradmin')

                    success = success and all(await collect((
                        user_domain.update_project_access(
                            user_email,
                            project_name,
                            True
                        ),
                        authz.grant_group_level_role(
                            user_email, project_name,
                            user_role
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
        success = success and await request_deletion(
            project_name=group_name,
            user_email=requester_email,
        )

    if success:
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

    return success


async def add_access(
        user_email: str,
        project_name: str,
        project_attr: str,
        attr_value: Union[str, bool]) -> bool:
    return await project_dal.update_access(
        user_email, project_name, project_attr, attr_value
    )


async def add_user_access(email: str, group: str, role: str) -> bool:
    return (
        await add_access(email, group, 'has_access', True) and
        await authz.grant_group_level_role(email, group, role)
    )


async def remove_access(user_email: str, project_name: str) -> bool:
    return await project_dal.remove_access(user_email, project_name)


async def get_pending_to_delete() -> List[ProjectType]:
    return await project_dal.get_pending_to_delete()


async def get_historic_deletion(project_name: str) -> HistoricType:
    historic_deletion = await project_dal.get_attributes(
        project_name.lower(), ['historic_deletion'])
    return cast(HistoricType, historic_deletion.get('historic_deletion', []))


async def remove_resources(project_name: str) -> bool:
    are_users_removed = await remove_all_users_access(project_name)
    group_findings = await list_findings(
        [project_name], should_list_deleted=True
    )
    group_drafts = await list_drafts(
        [project_name], should_list_deleted=True
    )
    findings_and_drafts = (
        group_findings[0] + group_drafts[0]
    )
    are_findings_masked = all(await collect(
        finding_domain.mask_finding(finding_id)
        for finding_id in findings_and_drafts
    ))
    events = await list_events(project_name)
    are_events_masked = all(await collect(
        event_domain.mask(event_id)
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


async def delete_project(project_name: str, user_email: str) -> bool:
    response = False
    data = await project_dal.get_attributes(
        project_name,
        ['project_status', 'historic_deletion']
    )
    historic_deletion = cast(
        List[Dict[str, str]],
        data.get('historic_deletion', [])
    )
    if data.get('project_status') not in ['DELETED', 'PENDING_DELETION']:
        all_resources_removed = await remove_resources(project_name)
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


async def request_deletion(project_name: str, user_email: str) -> bool:
    project = project_name.lower()
    response = False
    if (await user_domain.get_group_access(user_email, project) and
            project_name == project):
        data = await project_dal.get_attributes(
            project,
            ['project_status', 'historic_deletion']
        )
        historic_deletion = cast(
            List[Dict[str, str]],
            data.get('historic_deletion', [])
        )
        if data.get('project_status') not in ['DELETED', 'PENDING_DELETION']:
            today = datetime_utils.get_now()
            deletion_date = datetime_utils.get_as_str(
                datetime_utils.get_now_plus_delta(days=30),
                date_format='%Y-%m-%d'
            ) + ' 23:59:59'
            new_state = {
                'date': datetime_utils.get_as_str(today),
                'deletion_date': deletion_date,
                'user': user_email.lower(),
            }
            historic_deletion.append(new_state)
            new_data: ProjectType = {
                'historic_deletion': historic_deletion,
                'project_status': 'PENDING_DELETION'
            }
            response = await project_dal.update(project, new_data)
        else:
            raise AlreadyPendingDeletion()
    else:
        raise PermissionDenied()

    if response:
        await authz.revoke_cached_group_service_attributes_policies(
            project_name
        )

    return response


async def reject_deletion(project_name: str, user_email: str) -> bool:
    response = False
    project = project_name.lower()
    if project_name == project:
        data = await project_dal.get_attributes(
            project,
            ['project_status', 'historic_deletion']
        )
        historic_deletion = cast(
            List[Dict[str, str]],
            data.get('historic_deletion', [])
        )
        if data.get('project_status') == 'PENDING_DELETION':
            today = datetime_utils.get_now()
            new_state = {
                'date': datetime_utils.get_as_str(today),
                'user': user_email.lower(),
                'state': 'REJECTED'
            }
            historic_deletion.append(new_state)
            new_data = {
                'project_status': 'ACTIVE',
                'historic_deletion': historic_deletion
            }
            response = await project_dal.update(project, new_data)
        else:
            raise NotPendingDeletion()
    else:
        raise PermissionDenied()

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


async def remove_project(project_name: str) -> NamedTuple:
    """Delete project information."""
    LOGGER.warning(
        'Removing %s project',
        project_name,
        extra={'extra': locals()}
    )
    Status: NamedTuple = namedtuple(
        'Status',
        'are_findings_masked are_users_removed is_group_masked '
        'are_events_masked are_resources_removed'
    )
    data = await project_dal.get_attributes(
        project_name, ['project_status'])
    if data.get('project_status') == 'PENDING_DELETION':
        are_users_removed = await remove_all_users_access(project_name)
        group_findings = await list_findings(
            [project_name], should_list_deleted=True
        )
        group_drafts = await list_drafts(
            [project_name], should_list_deleted=True
        )
        findings_and_drafts = (
            group_findings[0] + group_drafts[0]
        )
        are_findings_masked = all(await collect(
            finding_domain.mask_finding(finding_id)
            for finding_id in findings_and_drafts
        ))
        events = await list_events(project_name)
        are_events_masked = all(await collect(
            event_domain.mask(event_id)
            for event_id in events
        ))
        is_group_masked = await mask(project_name)
        are_resources_removed = all(
            list(cast(List[bool], await resources_domain.mask(project_name))))
        response = Status(
            are_findings_masked,
            are_users_removed,
            is_group_masked,
            are_events_masked,
            are_resources_removed
        )
    else:
        raise PermissionDenied()
    return cast(NamedTuple, response)


async def remove_all_users_access(project: str) -> bool:
    """Remove user access to project."""
    user_active, user_suspended = await collect([
        get_users(project, True),
        get_users(project, False)
    ])
    all_users = user_active + user_suspended
    are_users_removed = all(await collect([
        remove_user_access(project, user)
        for user in all_users
    ]))

    return are_users_removed


async def remove_user_access(
        group: str,
        email: str,
        check_org_access: bool = True) -> bool:
    """Remove user access to project."""
    success: bool = all(
        await collect([
            authz.revoke_group_level_role(email, group),
            remove_access(email, group)
        ])
    )
    if success and check_org_access:
        org_id = await org_domain.get_id_for_group(group)
        if not await user_domain.get_projects(email, organization_id=org_id):
            await org_domain.remove_user(org_id, email)
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


async def total_vulnerabilities(finding_id: str) -> Dict[str, int]:
    """Get total vulnerabilities in new format."""
    finding = {'openVulnerabilities': 0, 'closedVulnerabilities': 0}
    if await finding_domain.validate_finding(finding_id):
        vulnerabilities = await vuln_domain.list_vulnerabilities_async(
            [finding_id]
        )
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
        project_name: str) -> List[Dict[str, FindingType]]:
    """Gets findings pending for verification"""
    findings_ids = await list_findings([project_name])
    are_pending_verifications = await collect(
        map(finding_domain.is_pending_verification, findings_ids[0])
    )
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


async def get_pending_closing_check(project: str) -> int:
    """Check for pending closing checks."""
    pending_closing = len(
        await get_pending_verification_findings(project))
    return pending_closing


async def get_released_findings(
        project_name: str,
        attrs: str = '') -> List[Dict[str, FindingType]]:
    return await project_dal.get_released_findings(project_name, attrs)


async def get_last_closing_vuln_info(
        findings: List[Dict[str, FindingType]]) -> \
        Tuple[Decimal, VulnerabilityType]:
    """Get day since last vulnerability closing."""

    validate_findings = await collect(
        finding_domain.validate_finding(str(finding['finding_id']))
        for finding in findings
    )
    validated_findings = [
        finding for finding, is_valid in zip(findings, validate_findings)
        if is_valid
    ]
    vulns = await vuln_domain.list_vulnerabilities_async(
        [str(finding['finding_id']) for finding in validated_findings]
    )
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
        vulnerability: Dict[str, FindingType]) -> Optional[date]:
    """Get last closing date of a vulnerability."""
    current_state = vuln_domain.get_last_approved_state(vulnerability)
    last_closing_date = None

    if current_state and current_state.get('state') == 'closed':
        last_closing_date = datetime_utils.get_from_str(
            current_state.get('date', '').split(' ')[0],
            date_format='%Y-%m-%d'
        ).date()
    return last_closing_date


def is_vulnerability_closed(vuln: Dict[str, FindingType]) -> bool:
    """Return if a vulnerability is closed."""
    return vuln_domain.get_last_status(vuln) == 'closed'


async def get_max_open_severity(
        findings: List[Dict[str, FindingType]]) -> \
        Tuple[Decimal, Dict[str, FindingType]]:
    """Get maximum severity of project with open vulnerabilities."""
    total_vulns = await collect(
        total_vulnerabilities(str(fin.get('finding_id', '')))
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
        vulnerability: Dict[str, FindingType]) -> Optional[date]:
    """Get open vulnerability date of a vulnerability."""
    all_states = cast(
        List[Dict[str, str]],
        vulnerability.get('historic_state', [{}])
    )
    current_state: Dict[str, str] = all_states[0]
    open_date = None
    if (current_state.get('state') == 'open' and
            not current_state.get('approval_status')):
        open_date = datetime_utils.get_from_str(
            current_state.get('date', '').split(' ')[0],
            date_format='%Y-%m-%d'
        ).date()
    return open_date


async def get_mean_remediate(findings: List[Dict[str, FindingType]]) -> \
        Decimal:
    """Get mean time to remediate a vulnerability."""
    total_vuln = 0
    total_days = 0
    validate_findings = await collect(
        finding_domain.validate_finding(str(finding['finding_id']))
        for finding in findings
    )
    validated_findings = [
        finding
        for finding, validate_finding in zip(findings, validate_findings)
        if validate_finding
    ]
    vulns = await vuln_domain.list_vulnerabilities_async(
        [str(finding['finding_id']) for finding in validated_findings]
    )
    open_vuln_dates = await collect(
        in_process(get_open_vulnerability_date, vuln)
        for vuln in vulns
    )
    filtered_open_vuln_dates = [
        vuln
        for vuln in open_vuln_dates
        if vuln
    ]
    closed_vuln_dates = await collect(
        in_process(get_last_closing_date, vuln)
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


async def get_mean_remediate_severity(
        project_name: str,
        min_severity: float,
        max_severity: float) -> Decimal:
    """Get mean time to remediate."""
    total_days = 0
    finding_ids = await list_findings([project_name.lower()])
    vulns = await vuln_domain.list_vulnerabilities_async([
        str(finding['findingId'])
        for finding in await finding_domain.get_findings_async(finding_ids[0])
        if (
            min_severity <=
            cast(float, finding.get('severityCvss', 0)) <=
            max_severity
        )
    ])
    open_vuln_dates = await collect([
        in_process(get_open_vulnerability_date, vuln)
        for vuln in vulns
    ])
    filtered_open_vuln_dates = [
        vuln for vuln in open_vuln_dates
        if vuln
    ]
    closed_vuln_dates = await collect([
        in_process(get_last_closing_date, vuln)
        for vuln, open_vuln_date in zip(vulns, open_vuln_dates)
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
        findings: List[Dict[str, FindingType]]) -> Dict[str, int]:
    """Get the total treatment of all the vulnerabilities"""
    accepted_vuln: int = 0
    indefinitely_accepted_vuln: int = 0
    in_progress_vuln: int = 0
    undefined_treatment: int = 0
    validate_findings = await collect(
        finding_domain.validate_finding(str(finding['finding_id']))
        for finding in findings
    )
    validated_findings = [
        finding
        for finding, validate_finding in zip(findings, validate_findings)
        if validate_finding
    ]
    total_vulns = await collect(
        total_vulnerabilities(str(finding['finding_id']))
        for finding in validated_findings
    )
    for finding, total_vuln in zip(validated_findings, total_vulns):
        fin_treatment = cast(
            List[Dict[str, str]],
            finding.get('historic_treatment', [{}])
        )[-1].get('treatment')
        open_vulns = int(total_vuln.get('openVulnerabilities', ''))
        if fin_treatment == 'ACCEPTED':
            accepted_vuln += open_vulns
        elif fin_treatment == 'ACCEPTED_UNDEFINED':
            indefinitely_accepted_vuln += open_vulns
        elif fin_treatment == 'IN PROGRESS':
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


async def list_drafts(
        groups_name: List[str],
        should_list_deleted: bool = False) -> List[List[str]]:
    """Returns a list the list of finding ids associated with the groups"""
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(finding_dal.TABLE_NAME)
        drafts = await collect(
            project_dal.list_drafts(group_name, table, should_list_deleted)
            for group_name in groups_name
        )
    return cast(List[List[str]], drafts)


async def list_comments(
        project_name: str,
        user_email: str) -> List[CommentType]:
    comments = await collect([
        comment_domain.fill_comment_data(project_name, user_email, comment)
        for comment in await project_dal.get_comments(project_name)
    ])

    return cast(List[CommentType], comments)


async def get_active_projects() -> List[str]:
    projects = await project_dal.get_active_projects()

    return projects


async def get_alive_projects() -> List[str]:
    projects = await project_dal.get_alive_projects()

    return projects


async def list_findings(
        groups_name: List[str],
        should_list_deleted: bool = False) -> List[List[str]]:
    """Returns a list of the list of finding ids associated with the groups"""
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(finding_dal.TABLE_NAME)
        findings = await collect(
            project_dal.list_findings(group_name, table, should_list_deleted)
            for group_name in groups_name
        )
    return cast(List[List[str]], findings)


async def list_events(project_name: str) -> List[str]:
    """ Returns the list of event ids associated with the project"""
    return await project_dal.list_events(project_name)


async def get_attributes(
        project_name: str,
        attributes: List[str]) -> Dict[str, Union[str, List[str]]]:
    return await project_dal.get_attributes(project_name, attributes)


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


async def get_open_vulnerabilities(project_name: str) -> int:
    findings = await list_findings([project_name])
    vulns = await vuln_domain.list_vulnerabilities_async(findings[0])
    last_approved_status = await collect([
        in_process(vuln_domain.get_last_status, vuln)
        for vuln in vulns
    ])
    open_vulnerabilities = 0
    for status in last_approved_status:
        if status == 'open':
            open_vulnerabilities += 1
    return open_vulnerabilities


async def get_closed_vulnerabilities(project_name: str) -> int:
    findings = await list_findings([project_name])
    vulns = await vuln_domain.list_vulnerabilities_async(findings[0])
    last_approved_status = await collect([
        in_process(vuln_domain.get_last_status, vuln)
        for vuln in vulns
    ])
    closed_vulnerabilities = 0
    for status in last_approved_status:
        if status == 'closed':
            closed_vulnerabilities += 1
    return closed_vulnerabilities


async def get_open_finding(project_name: str) -> int:
    findings = await list_findings([project_name])
    vulns = await vuln_domain.list_vulnerabilities_async(findings[0])
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


async def get_user_access(email: str, group_name: str) -> Dict[str, str]:
    access: List[Dict[str, ProjectType]] = \
        await project_dal.get_user_access(email, group_name)

    return cast(Dict[str, str], access[0]) if access else {}


def is_fluid_user(email: str) -> bool:
    return email.endswith('@fluidattacks.com')


async def is_manager(email: str, group_name: str) -> bool:
    role: str = await authz.get_group_level_role(email, group_name)

    return role == 'group_manager'


async def filter_stakeholders(
    emails: List[str],
    group_name: str,
    user_email: str,
) -> List[str]:
    if is_fluid_user(user_email):
        return emails

    return [
        email
        for email in emails
        if not is_fluid_user(email)
        or await is_manager(email, group_name)
    ]
