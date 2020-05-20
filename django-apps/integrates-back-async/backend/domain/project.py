"""Domain functions for projects."""

from typing import Dict, List, NamedTuple, Union, cast
from collections import namedtuple
import re
from datetime import datetime, timedelta
from decimal import Decimal
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
    vulnerability as vuln_domain, internal_project as internal_project_domain
)
from backend.exceptions import (
    AlreadyPendingDeletion, InvalidCommentParent, InvalidParameter, InvalidProjectName,
    NotPendingDeletion, PermissionDenied, RepeatedValues, InvalidProjectServicesConfig
)
from backend.mailer import send_comment_mail
from backend.utils import validations
from backend import authz, util

from __init__ import FI_MAIL_REVIEWERS


async def does_group_has_drills(group: str) -> bool:
    """Return True if the provided group has drills."""
    attrs = get_attributes(group, ['has_drills'])

    return bool(attrs.get('has_drills', False))


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
        has_forces: bool):
    if is_continuous_type:
        if has_forces and not has_drills:
            raise InvalidProjectServicesConfig(
                'Forces is only available when Drills is too')
    else:
        if has_drills:
            raise InvalidProjectServicesConfig(
                'Drills is only available in projects of type Continuous')
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
            has_forces)

        if internal_project_domain.does_project_name_exist(project_name) \
                and not project_dal.exists(project_name):
            project: ProjectType = {
                'project_name': project_name,
                'description': description,
                'has_drills': has_drills,
                'has_forces': has_forces,
                'companies': companies,
                'type': subscription,
                'project_status': 'ACTIVE'
            }

            success = project_dal.create(project)
            if success:
                internal_project_domain.remove_project_name(project_name)
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

    if success:
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
    group_name: str,
    has_drills: bool,
    has_forces: bool,
    requester_email: str,
    subscription: str,
) -> bool:
    is_continuous_type: bool = subscription == 'continuous'

    validate_project_services_config(
        is_continuous_type,
        has_drills,
        has_forces)

    success: bool = project_dal.update(
        data={
            'has_drills': has_drills,
            'has_forces': has_forces,
            'type': subscription,
        },
        project_name=group_name,
    )

    if success:
        notifications_domain.edit_group(
            group_name=group_name,
            has_drills=has_drills,
            has_forces=has_forces,
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


def total_vulnerabilities(finding_id: str) -> Dict[str, int]:
    """Get total vulnerabilities in new format."""
    finding = {'openVulnerabilities': 0, 'closedVulnerabilities': 0}
    if finding_domain.validate_finding(finding_id):
        vulnerabilities = vuln_dal.get_vulnerabilities(finding_id)
        for vuln in vulnerabilities:
            current_state = vuln_domain.get_last_approved_status(vuln)
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
        [total_vulnerabilities(str(fin.get('finding_id', ''))).get(vuln_type)
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


def get_last_closing_vuln(findings: List[Dict[str, FindingType]]) -> Decimal:
    """Get day since last vulnerability closing."""
    closing_dates = []
    for fin in findings:
        if finding_domain.validate_finding(str(fin['finding_id'])):
            vulnerabilities = vuln_dal.get_vulnerabilities(
                str(fin.get('finding_id', '')))
            closing_vuln_date = [get_last_closing_date(vuln)
                                 for vuln in vulnerabilities
                                 if is_vulnerability_closed(vuln)]
            if closing_vuln_date:
                closing_dates.append(max(closing_vuln_date))
            else:
                # Vulnerability does not have closing date
                pass
    if closing_dates:
        current_date = max(closing_dates)
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


def get_max_open_severity(findings: List[Dict[str, FindingType]]) -> Decimal:
    """Get maximum severity of project with open vulnerabilities."""
    total_severity: List[float] = \
        cast(List[float],
             [fin.get('cvss_temporal', '') for fin in findings
              if int(total_vulnerabilities(str(fin.get('finding_id', '')))
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


def get_mean_remediate(findings: List[Dict[str, FindingType]]) -> Decimal:
    """Get mean time to remediate a vulnerability."""
    total_vuln = 0
    total_days = 0
    tzn = pytz.timezone('America/Bogota')
    for finding in findings:
        if finding_domain.validate_finding(str(finding['finding_id'])):
            vulnerabilities = vuln_dal.get_vulnerabilities(str(finding.get('finding_id', '')))
            for vuln in vulnerabilities:
                open_vuln_date = get_open_vulnerability_date(vuln)
                closed_vuln_date = get_last_closing_date(vuln)
                if open_vuln_date:
                    if closed_vuln_date:
                        total_days += int(
                            (closed_vuln_date - open_vuln_date).days)
                    else:
                        current_day = datetime.now(tz=tzn).date()
                        total_days += int((current_day - open_vuln_date).days)
                    total_vuln += 1
    if total_vuln:
        mean_vulnerabilities = Decimal(
            round(total_days / float(total_vuln))).quantize(Decimal('0.1'))
    else:
        mean_vulnerabilities = Decimal(0).quantize(Decimal('0.1'))
    return mean_vulnerabilities


def get_mean_remediate_severity(project_name: str, min_severity: float,
                                max_severity: float) -> Decimal:
    """Get mean time to remediate."""
    total_vuln = 0
    total_days = 0
    tzn = pytz.timezone('America/Bogota')
    project_name = project_name.lower()
    finding_ids = list_findings(project_name)
    findings = finding_domain.get_findings(finding_ids)
    for finding in findings:
        if min_severity <= cast(float, finding.get('severityCvss', 0)) <= max_severity:
            vulnerabilities = vuln_dal.get_vulnerabilities(str(finding.get('findingId', '')))
            for vuln in vulnerabilities:
                open_vuln_date = get_open_vulnerability_date(vuln)
                closed_vuln_date = get_last_closing_date(vuln)
                if open_vuln_date:
                    if closed_vuln_date:
                        total_days += int(
                            (closed_vuln_date - open_vuln_date).days)
                    else:
                        current_day = datetime.now(tz=tzn).date()
                        total_days += int((current_day - open_vuln_date).days)
                    total_vuln += 1
    if total_vuln:
        mean_vulnerabilities = Decimal(
            round(total_days / float(total_vuln))).quantize(Decimal('0.1'))
    else:
        mean_vulnerabilities = Decimal(0).quantize(Decimal('0.1'))
    return mean_vulnerabilities


def get_total_treatment(findings: List[Dict[str, FindingType]]) -> Dict[str, int]:
    """Get the total treatment of all the vulnerabilities"""
    accepted_vuln: int = 0
    indefinitely_accepted_vuln: int = 0
    in_progress_vuln: int = 0
    undefined_treatment: int = 0
    for finding in findings:
        fin_treatment = cast(List[Dict[str, str]],
                             finding.get('historic_treatment', [{}]))[-1].get('treatment')
        if finding_domain.validate_finding(str(finding['finding_id'])):
            open_vulns = int(total_vulnerabilities(
                str(finding['finding_id'])).get('openVulnerabilities', ''))
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


def get_open_findings(finding_vulns: List[List[Dict[str, FindingType]]]) -> int:
    open_findings = [
        vulns for vulns in finding_vulns
        if [vuln for vuln in vulns
            if vuln_domain.get_last_approved_status(vuln) == 'open']
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


def list_comments(project_name: str, user_email: str) -> List[CommentType]:
    comments = [
        comment_domain.fill_comment_data(project_name, user_email, comment)
        for comment in project_dal.get_comments(project_name)
    ]

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
