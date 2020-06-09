"""Domain functions for projects."""

import asyncio
from typing import Dict, List, NamedTuple, Union, cast
from collections import namedtuple, defaultdict
import re
from datetime import datetime, timedelta
from decimal import Decimal
from asgiref.sync import sync_to_async, async_to_sync
import pytz

from django.conf import settings

from backend.dal import (
    finding as finding_dal,
    project as project_dal,
    vulnerability as vuln_dal
)
from backend.typing import (
    Comment as CommentType, Finding as FindingType, Project as ProjectType
)
from backend.domain import (
    comment as comment_domain, resources as resources_domain,
    finding as finding_domain, user as user_domain,
    notifications as notifications_domain,
    vulnerability as vuln_domain, available_group as available_group_domain
)
from backend.exceptions import (
    AlreadyPendingDeletion, InvalidCommentParent, InvalidParameter, InvalidProjectName,
    NotPendingDeletion, PermissionDenied, RepeatedValues, InvalidProjectServicesConfig
)
from backend.mailer import send_comment_mail
from backend.utils import validations
from backend import authz, util

from __init__ import FI_MAIL_REVIEWERS


def get_email_recipients(project_name: str) -> List[str]:
    """Get the recipients of the comment email."""
    recipients = [str(user) for user in get_users(project_name)]
    approvers = FI_MAIL_REVIEWERS.split(',')
    recipients += approvers

    return recipients


def add_comment(project_name: str, email: str, comment_data: CommentType) -> bool:
    """Add comment in a project."""
    parent = str(comment_data.get('parent'))
    if parent != '0':
        project_comments = \
            [str(comment.get('user_id'))
             for comment in project_dal.get_comments(project_name)]
        if parent not in project_comments:
            raise InvalidCommentParent()
    send_comment_mail(comment_data, 'project', email, 'project', project_name)
    return project_dal.add_comment(project_name, email, comment_data)


def validate_project_services_config(
    is_continuous_type: bool,
    has_drills: bool,
    has_forces: bool,
    has_integrates: bool,
):
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


def create_project(
        user_email: str,
        user_role: str,
        **kwargs: Dict[str, Union[bool, str, List[str]]]) -> bool:
    project_name = str(kwargs.get('project_name', '')).lower()
    description = str(kwargs.get('description', ''))
    validations.validate_project_name(project_name)
    validations.validate_fields([description])
    validations.validate_field_length(project_name, 20)
    validations.validate_field_length(description, 200)
    is_user_admin = user_role == 'admin'
    if is_user_admin or \
       cast(List[str], kwargs.get('companies', [])):
        companies = [company.lower() for company in kwargs.get('companies', [])]
    else:
        companies = [str(user_domain.get_data(user_email, 'company'))]
    validations.validate_fields(companies)
    has_drills = cast(bool, kwargs.get('has_drills', False))
    has_forces = cast(bool, kwargs.get('has_forces', False))
    if kwargs.get('subscription'):
        subscription = str(kwargs.get('subscription'))
    else:
        subscription = 'continuous'

    is_continuous_type = subscription == 'continuous'

    success: bool = False

    if not (not description.strip() or not project_name.strip() or
       not all([company.strip() for company in companies]) or
       not companies):

        validate_project_services_config(
            is_continuous_type,
            has_drills,
            has_forces,
            has_integrates=True)

        is_group_avail = async_to_sync(
            available_group_domain.exists)(project_name)

        if is_group_avail and not project_dal.exists(project_name):
            project: ProjectType = {
                'project_name': project_name,
                'description': description,
                'companies': companies,
                'historic_configuration': [{
                    'date': util.get_current_time_as_iso_str(),
                    'has_drills': has_drills,
                    'has_forces': has_forces,
                    'requester': user_email,
                    'type': subscription,
                }],
                'project_status': 'ACTIVE',
            }

            success = project_dal.create(project)
            if success:
                async_to_sync(
                    available_group_domain.remove)(project_name)
                # Admins are not granted access to the project
                # they are omnipresent
                if not is_user_admin:
                    user_role = {
                        # Internal managers are turned into group_managers
                        'internal_manager': 'group_manager'
                        # Other roles are turned into customeradmins
                    }.get(user_role, 'customeradmin')

                    success = success and all([
                        user_domain.update_project_access(
                            user_email, project_name, True),
                        authz.grant_group_level_role(
                            user_email, project_name, user_role),
                    ])

        else:
            raise InvalidProjectName()
    else:
        raise InvalidParameter()

    # Notify us in case the user wants any Fluid Service
    if success and (has_drills or has_forces):
        notifications_domain.new_group(
            description=description,
            group_name=project_name,
            has_drills=has_drills,
            has_forces=has_forces,
            requester_email=user_email,
            subscription=subscription,
        )

    return success


def edit(
    *,
    comments: str,
    group_name: str,
    has_drills: bool,
    has_forces: bool,
    has_integrates: bool,
    requester_email: str,
    subscription: str,
) -> bool:
    is_continuous_type: bool = subscription == 'continuous'

    validations.validate_fields([comments])
    validations.validate_string_length_between(comments, 0, 250)
    validate_project_services_config(
        is_continuous_type,
        has_drills,
        has_forces,
        has_integrates)

    item = cast(Dict[str, List[dict]], project_dal.get_attributes(
        project_name=group_name,
        attributes=[
            'historic_configuration',
        ]
    ))
    item.setdefault('historic_configuration', [])

    success: bool = project_dal.update(
        data={
            'historic_configuration': item['historic_configuration'] + [{
                'comments': comments,
                'date': util.get_current_time_as_iso_str(),
                'has_drills': has_drills,
                'has_forces': has_forces,
                'requester': requester_email,
                'type': subscription,
            }],
        },
        project_name=group_name,
    )
    if not has_integrates:
        success = success and request_deletion(
            project_name=group_name,
            user_email=requester_email,
        )

    if success:
        notifications_domain.edit_group(
            comments=comments,
            group_name=group_name,
            has_drills=has_drills,
            has_forces=has_forces,
            has_integrates=has_integrates,
            requester_email=requester_email,
            subscription=subscription,
        )

    return success


def add_access(user_email: str, project_name: str,
               project_attr: str, attr_value: Union[str, bool]) -> bool:
    return project_dal.add_access(user_email, project_name, project_attr, attr_value)


def remove_access(user_email: str, project_name: str) -> bool:
    return project_dal.remove_access(user_email, project_name)


def get_pending_to_delete() -> List[Dict[str, ProjectType]]:
    return project_dal.get_pending_to_delete()


def get_historic_deletion(project_name: str) -> Union[str, List[str]]:
    historic_deletion = project_dal.get_attributes(
        project_name.lower(), ['historic_deletion'])
    return historic_deletion.get('historic_deletion', [])


def request_deletion(project_name: str, user_email: str) -> bool:
    project = project_name.lower()
    response = False
    if user_domain.get_group_access(user_email, project) and project_name == project:
        data = project_dal.get_attributes(project, ['project_status', 'historic_deletion'])
        historic_deletion = cast(List[Dict[str, str]], data.get('historic_deletion', []))
        if data.get('project_status') not in ['DELETED', 'PENDING_DELETION']:
            tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
            today = datetime.now(tz=tzn).today()
            deletion_date = (today + timedelta(days=30)).strftime('%Y-%m-%d') + ' 23:59:59'
            new_state = {
                'date': today.strftime('%Y-%m-%d %H:%M:%S'),
                'deletion_date': deletion_date,
                'user': user_email.lower(),
            }
            historic_deletion.append(new_state)
            new_data: ProjectType = {
                'historic_deletion': historic_deletion,
                'project_status': 'PENDING_DELETION'
            }
            response = project_dal.update(project, new_data)
        else:
            raise AlreadyPendingDeletion()
    else:
        raise PermissionDenied()

    if response:
        authz.revoke_cached_group_service_attributes_policies(project_name)

    return response


def reject_deletion(project_name: str, user_email: str) -> bool:
    response = False
    project = project_name.lower()
    if project_name == project:
        data = project_dal.get_attributes(project, ['project_status', 'historic_deletion'])
        historic_deletion = cast(List[Dict[str, str]], data.get('historic_deletion', []))
        if data.get('project_status') == 'PENDING_DELETION':
            tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
            today = datetime.now(tz=tzn).today()
            new_state = {
                'date': today.strftime('%Y-%m-%d %H:%M:%S'),
                'user': user_email.lower(),
                'state': 'REJECTED'
            }
            historic_deletion.append(new_state)
            new_data = {
                'project_status': 'ACTIVE',
                'historic_deletion': historic_deletion
            }
            response = project_dal.update(project, new_data)
        else:
            raise NotPendingDeletion()
    else:
        raise PermissionDenied()
    return response


def remove_project(project_name: str, user_email: str) -> NamedTuple:
    """Delete project information."""
    project = project_name.lower()
    Status: NamedTuple = namedtuple(
        'Status',
        'are_findings_masked are_users_removed is_project_finished are_resources_removed'
    )
    response = Status(False, False, False, False)
    data = project_dal.get_attributes(project, ['project_status'])
    validation = False
    if user_email:
        validation = is_alive(project) and user_domain.get_group_access(user_email, project)
    if (not user_email and data.get('project_status') == 'PENDING_DELETION') or validation:
        tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
        today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
        are_users_removed = remove_all_users_access(project)
        are_findings_masked: Union[bool, List[bool]] = [
            finding_domain.mask_finding(finding_id)
            for finding_id in list_findings(project) + list_drafts(project)]
        if are_findings_masked == []:
            are_findings_masked = True
        update_data: Dict[str, Union[str, List[str], object]] = {
            'project_status': 'FINISHED',
            'deletion_date': today
        }
        is_project_finished = project_dal.update(project, update_data)
        are_resources_removed = all(list(cast(List[bool], resources_domain.mask(project))))
        util.invalidate_cache(project)
        response = Status(
            are_findings_masked, are_users_removed, is_project_finished, are_resources_removed
        )
    else:
        raise PermissionDenied()
    return cast(NamedTuple, response)


def remove_all_users_access(project: str) -> bool:
    """Remove user access to project."""
    user_active = get_users(project)
    user_suspended = get_users(project, active=False)
    all_users = user_active + user_suspended
    are_users_removed = True
    for user in all_users:
        is_user_removed = remove_user_access(project, user)
        if is_user_removed:
            are_users_removed = True
        else:
            are_users_removed = False
            break
    return are_users_removed


def remove_user_access(group: str, email: str) -> bool:
    """Remove user access to project."""
    return authz.revoke_group_level_role(email, group) \
        and project_dal.remove_access(email, group)


def _has_repeated_tags(project_name: str, tags: List[str]) -> bool:
    has_repeated_inputs = len(tags) != len(set(tags))

    existing_tags = get_attributes(
        project_name.lower(), ['tag']).get('tag', [])
    all_tags = list(existing_tags) + tags
    has_repeated_tags = len(all_tags) != len(set(all_tags))

    return has_repeated_inputs or has_repeated_tags


def validate_tags(project_name: str, tags: List[str]) -> List[str]:
    """Validate tags array."""
    tags_validated = []
    pattern = re.compile('^[a-z0-9]+(?:-[a-z0-9]+)*$')
    if _has_repeated_tags(project_name, tags):
        raise RepeatedValues()

    for tag in tags:
        if pattern.match(tag):
            tags_validated.append(tag)
        else:
            # Invalid tag
            pass
    return tags_validated


def is_alive(project: str) -> bool:
    return project_dal.is_alive(project)


def can_user_access_pending_deletion(project: str, role: str) -> bool:
    return project_dal.can_user_access_pending_deletion(project, role)


async def total_vulnerabilities(finding_id: str) -> Dict[str, int]:
    """Get total vulnerabilities in new format."""
    finding = {'openVulnerabilities': 0, 'closedVulnerabilities': 0}
    if await sync_to_async(finding_domain.validate_finding)(finding_id):
        vulnerabilities = await sync_to_async(vuln_dal.get_vulnerabilities)(finding_id)
        last_approved_status = await asyncio.gather(*[
            asyncio.create_task(
                sync_to_async(vuln_domain.get_last_approved_status)(
                    vuln
                )
            )
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


def get_vulnerabilities(findings: List[Dict[str, FindingType]], vuln_type: str) -> int:
    """Get total vulnerabilities by type."""
    vulnerabilities = \
        [async_to_sync(total_vulnerabilities)(str(fin.get('finding_id', ''))).get(vuln_type)
         for fin in findings]
    vulnerabilities_sum = sum(vulnerabilities)
    return vulnerabilities_sum if vulnerabilities_sum else 0


def get_pending_closing_check(project: str) -> int:
    """Check for pending closing checks."""
    pending_closing = len(
        project_dal.get_pending_verification_findings(project))
    return pending_closing


def get_released_findings(project_name: str, attrs: str = '') -> List[Dict[str, FindingType]]:
    return project_dal.get_released_findings(project_name, attrs)


async def get_last_closing_vuln(findings: List[Dict[str, FindingType]]) -> Decimal:
    """Get day since last vulnerability closing."""
    validate_findings = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(finding_domain.validate_finding)(
                str(finding['finding_id']))
        )
        for finding in findings
    ])
    validated_findings = [
        finding for finding in findings
        if validate_findings.pop(0)
    ]
    finding_vulns = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(vuln_dal.get_vulnerabilities)(
                str(finding['finding_id']))
        )
        for finding in validated_findings
    ])
    are_vuln_closed = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(is_vulnerability_closed)(
                vuln)
        )
        for vulns in finding_vulns for vuln in vulns
    ])
    closing_vuln_dates = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(get_last_closing_date)(
                vuln)
        )
        for vulns in finding_vulns for vuln in vulns
        if are_vuln_closed.pop(0)
    ])
    if closing_vuln_dates:
        current_date = max(closing_vuln_dates)
        tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
        last_closing = \
            Decimal((datetime.now(tz=tzn).date() -
                     current_date).days).quantize(Decimal('0.1'))
    else:
        last_closing = Decimal(0)
    return last_closing


def get_last_closing_date(vulnerability: Dict[str, FindingType]) -> datetime:
    """Get last closing date of a vulnerability."""
    current_state = vuln_domain.get_last_approved_state(vulnerability)
    last_closing_date = None

    if current_state and current_state.get('state') == 'closed':
        last_closing_date = datetime.strptime(
            current_state.get('date', '').split(' ')[0],
            '%Y-%m-%d'
        )
        tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
        last_closing_date = cast(datetime, last_closing_date.replace(tzinfo=tzn).date())
    return cast(datetime, last_closing_date)


def is_vulnerability_closed(vuln: Dict[str, FindingType]) -> bool:
    """Return if a vulnerability is closed."""
    return vuln_domain.get_last_approved_status(vuln) == 'closed'


async def get_max_open_severity(findings: List[Dict[str, FindingType]]) -> Decimal:
    """Get maximum severity of project with open vulnerabilities."""
    total_vulns = await asyncio.gather(*[
        asyncio.create_task(
            total_vulnerabilities(str(fin.get('finding_id', '')))
        )
        for fin in findings
    ])
    total_severity: List[float] = \
        cast(List[float],
             [fin.get('cvss_temporal', '') for fin in findings
              if int(total_vulns.pop(0)
              .get('openVulnerabilities', '')) > 0])
    if total_severity:
        max_severity = Decimal(max(total_severity)).quantize(Decimal('0.1'))
    else:
        max_severity = Decimal(0).quantize(Decimal('0.1'))
    return max_severity


def get_open_vulnerability_date(vulnerability: Dict[str, FindingType]) -> Union[datetime, None]:
    """Get open vulnerability date of a vulnerability."""
    all_states = cast(List[Dict[str, str]], vulnerability.get('historic_state', [{}]))
    current_state: Dict[str, str] = all_states[0]
    open_date = None
    if current_state.get('state') == 'open' and \
       not current_state.get('approval_status'):
        open_date = datetime.strptime(
            current_state.get('date', '').split(' ')[0],
            '%Y-%m-%d'
        )
        tzn = pytz.timezone('America/Bogota')
        open_date = cast(datetime, open_date.replace(tzinfo=tzn).date())
    return open_date


async def get_mean_remediate(findings: List[Dict[str, FindingType]]) -> Decimal:
    """Get mean time to remediate a vulnerability."""
    total_vuln = 0
    total_days = 0
    tzn = pytz.timezone('America/Bogota')
    validate_findings = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(finding_domain.validate_finding)(
                str(finding['finding_id']))
        )
        for finding in findings
    ])
    validated_findings = [
        finding for finding in findings
        if validate_findings.pop(0)
    ]
    finding_vulns = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(vuln_dal.get_vulnerabilities)(
                str(finding['finding_id']))
        )
        for finding in validated_findings
    ])
    open_vuln_dates = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(get_open_vulnerability_date)(
                vuln)
        )
        for vulns in finding_vulns for vuln in vulns
    ])
    filtered_open_vuln_dates = [
        vuln for vuln in open_vuln_dates
        if vuln
    ]
    closed_vuln_dates = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(get_last_closing_date)(
                vuln)
        )
        for vulns in finding_vulns for vuln in vulns
        if open_vuln_dates.pop(0)
    ])
    for index, closed_vuln_date in enumerate(closed_vuln_dates):
        if closed_vuln_date:
            total_days += int(
                (closed_vuln_date - filtered_open_vuln_dates[index]).days)
        else:
            current_day = datetime.now(tz=tzn).date()
            total_days += int((current_day - filtered_open_vuln_dates[index]).days)
    total_vuln = len(filtered_open_vuln_dates)
    if total_vuln:
        mean_vulnerabilities = Decimal(
            round(total_days / float(total_vuln))).quantize(Decimal('0.1'))
    else:
        mean_vulnerabilities = Decimal(0).quantize(Decimal('0.1'))
    return mean_vulnerabilities


async def get_mean_remediate_severity(project_name: str, min_severity: float,
                                      max_severity: float) -> Decimal:
    """Get mean time to remediate."""
    total_days = 0
    tzn = pytz.timezone('America/Bogota')
    finding_ids = await sync_to_async(list_findings)(project_name.lower())
    finding_vulns = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(vuln_dal.get_vulnerabilities)(
                str(finding.get('findingId', '')))
        )
        for finding in await sync_to_async(finding_domain.get_findings)(finding_ids)
        if min_severity <= cast(float, finding.get('severityCvss', 0)) <= max_severity
    ])
    open_vuln_dates = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(get_open_vulnerability_date)(
                vuln)
        )
        for vulns in finding_vulns for vuln in vulns
    ])
    filtered_open_vuln_dates = [
        vuln for vuln in open_vuln_dates
        if vuln
    ]
    closed_vuln_dates = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(get_last_closing_date)(
                vuln)
        )
        for vulns in finding_vulns for vuln in vulns
        if open_vuln_dates.pop(0)
    ])
    for index, closed_vuln_date in enumerate(closed_vuln_dates):
        if closed_vuln_date:
            total_days += int(
                (closed_vuln_date - filtered_open_vuln_dates[index]).days)
        else:
            current_day = datetime.now(tz=tzn).date()
            total_days += int((current_day - filtered_open_vuln_dates[index]).days)
    total_vuln = len(filtered_open_vuln_dates)
    if total_vuln:
        mean_vulnerabilities = Decimal(
            round(total_days / float(total_vuln))).quantize(Decimal('0.1'))
    else:
        mean_vulnerabilities = Decimal(0).quantize(Decimal('0.1'))
    return mean_vulnerabilities


async def get_total_treatment(findings: List[Dict[str, FindingType]]) -> Dict[str, int]:
    """Get the total treatment of all the vulnerabilities"""
    accepted_vuln: int = 0
    indefinitely_accepted_vuln: int = 0
    in_progress_vuln: int = 0
    undefined_treatment: int = 0
    validate_findings = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(finding_domain.validate_finding)(
                str(finding['finding_id']))
        )
        for finding in findings
    ])
    validated_findings = [
        finding for finding in findings
        if validate_findings.pop(0)
    ]
    total_vulns = await asyncio.gather(*[
        asyncio.create_task(
            total_vulnerabilities(str(finding['finding_id']))
        )
        for finding in validated_findings
    ])
    for finding in validated_findings:
        fin_treatment = cast(List[Dict[str, str]],
                             finding.get('historic_treatment', [{}]))[-1].get('treatment')
        open_vulns = int(total_vulns.pop(0).get('openVulnerabilities', ''))
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


async def get_open_findings(finding_vulns: List[List[Dict[str, FindingType]]]) -> int:
    last_approved_status = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(vuln_domain.get_last_approved_status)(
                vuln
            )
        )
        for vulns in finding_vulns for vuln in vulns
    ])
    open_findings = [
        vulns for vulns in finding_vulns
        if [vuln for vuln in vulns
            if last_approved_status.pop(0) == 'open']
    ]
    return len(open_findings)


def get_current_month_authors(project_name: str) -> str:
    return project_dal.get_current_month_authors(project_name)


def get_current_month_commits(project_name: str) -> str:
    return project_dal.get_current_month_commits(project_name)


def update(project_name: str, data: ProjectType) -> bool:
    return project_dal.update(project_name, data)


def list_drafts(project_name: str) -> List[str]:
    return project_dal.list_drafts(project_name)


async def list_comments(project_name: str, user_email: str) -> List[CommentType]:
    comments = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(comment_domain.fill_comment_data)(
                project_name, user_email, comment
            )
        )
        for comment in project_dal.get_comments(project_name)
    ])

    return comments


def get_active_projects() -> List[str]:
    projects = project_dal.get_active_projects()

    return projects


def get_alive_projects() -> List[str]:
    projects = project_dal.get_alive_projects()

    return projects


def list_findings(project_name: str) -> List[str]:
    """ Returns the list of finding ids associated with the project"""
    return project_dal.list_findings(project_name)


def list_events(project_name: str) -> List[str]:
    """ Returns the list of event ids associated with the project"""
    return project_dal.list_events(project_name)


def get_attributes(project_name: str, attributes: List[str]) -> Dict[str, Union[str, List[str]]]:
    return project_dal.get_attributes(project_name, attributes)


def get_finding_project_name(finding_id: str) -> str:
    return str(finding_dal.get_attributes(finding_id, ['project_name']).get('project_name', ''))


def list_internal_managers(project_name: str) -> List[str]:
    return project_dal.list_internal_managers(project_name.lower())


def get_description(project_name: str) -> str:
    return project_dal.get_description(project_name)


def get_users(project_name: str, active: bool = True) -> List[str]:
    return project_dal.get_users(project_name, active)


def add_all_access_to_project(project: str) -> bool:
    return project_dal.add_all_access_to_project(project)


def remove_all_project_access(project: str) -> bool:
    return project_dal.remove_all_project_access(project)


def get_project_info(project: str) -> List[ProjectType]:
    return project_dal.get(project)


def get_managers(project_name: str) -> List[str]:
    return [
        user_email
        for user_email in get_users(project_name, active=True)
        if authz.get_group_level_role(
            user_email, project_name) == 'customeradmin'
    ]


async def get_open_vulnerabilities(project_name: str) -> int:
    findings = await sync_to_async(list_findings)(project_name)
    vulns = await sync_to_async(vuln_domain.list_vulnerabilities)(findings)
    last_approved_status = await asyncio.gather(*[
        sync_to_async(vuln_domain.get_last_approved_status)(
            vuln
        )
        for vuln in vulns
    ])
    open_vulnerabilities = [
        1 for vuln in vulns
        if last_approved_status.pop(0) == 'open'
    ]
    return len(open_vulnerabilities)


async def get_closed_vulnerabilities(project_name: str) -> int:
    findings = await sync_to_async(list_findings)(project_name)
    vulns = await sync_to_async(vuln_domain.list_vulnerabilities)(findings)
    last_approved_status = await asyncio.gather(*[
        sync_to_async(vuln_domain.get_last_approved_status)(
            vuln
        )
        for vuln in vulns
    ])
    closed_vulnerabilities = [
        1 for vuln in vulns
        if last_approved_status.pop(0) == 'closed'
    ]
    return len(closed_vulnerabilities)


async def get_open_finding(project_name: str) -> int:
    findings = await sync_to_async(list_findings)(project_name)
    vulns = await sync_to_async(vuln_domain.list_vulnerabilities)(findings)
    finding_vulns_dict = defaultdict(list)
    for vuln in vulns:
        finding_vulns_dict[vuln['finding_id']].append(vuln)
    finding_vulns = list(finding_vulns_dict.values())
    return await get_open_findings(finding_vulns)
