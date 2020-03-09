"""Domain functions for projects."""

from typing import Dict, List, Union, cast
from collections import namedtuple
import re
from datetime import datetime, timedelta
from decimal import Decimal
import pytz

from django.conf import settings

from backend.dal import finding as finding_dal, project as project_dal
from backend.dal.comment import CommentType
from backend.dal.finding import FindingType
from backend.dal.project import ProjectType
from backend.domain import comment as comment_domain, resources as resources_domain
from backend.domain import finding as finding_domain, user as user_domain
from backend.domain import vulnerability as vuln_domain
from backend.exceptions import (
    AlreadyPendingDeletion, InvalidParameter, InvalidProjectName, NotPendingDeletion,
    PermissionDenied
)
from backend.mailer import send_comment_mail
from backend import util

from __init__ import FI_MAIL_REPLYERS


def get_email_recipients(project_name: str) -> List[str]:
    """Get the recipients of the comment email."""
    recipients = [str(user) for user in get_users(project_name)]
    replyers = FI_MAIL_REPLYERS.split(',')
    recipients += replyers

    return recipients


def add_comment(project_name: str, email: str, comment_data: CommentType) -> bool:
    """Add comment in a project."""
    send_comment_mail(comment_data, 'project', email, 'project', project_name)
    return project_dal.add_comment(project_name, email, comment_data)


def create_project(user_email: str, user_role: str, **kwargs: str) -> bool:
    is_user_admin = user_role == 'admin'
    if is_user_admin:
        companies = [company.lower() for company in kwargs.get('companies', [])]
    else:
        companies = [str(user_domain.get_data(user_email, 'company'))]
    description = kwargs.get('description', '')
    project_name = kwargs.get('project_name', '').lower()
    if kwargs.get('subscription'):
        subscription = kwargs.get('subscription')
    else:
        subscription = 'continuous'
    resp = False
    if not (not description.strip() or not project_name.strip() or
       not all([company.strip() for company in companies]) or
       not companies):
        if not project_dal.exists(project_name):
            project: ProjectType = {
                'project_name': project_name,
                'description': description,
                'companies': companies,
                'type': subscription,
                'project_status': 'ACTIVE'
            }
            resp = project_dal.create(project)
            if resp:
                if not is_user_admin:
                    add_user_access = user_domain.update_project_access(
                        user_email, project_name, True)
                    add_user_manager = add_user(
                        project_name.lower(), user_email.lower(), 'customeradmin')
                    resp = all([add_user_access, add_user_manager])
        else:
            raise InvalidProjectName()
    else:
        raise InvalidParameter()
    return resp


def add_user(project_name: str, user_email: str, role: str) -> bool:
    return project_dal.add_user(project_name, user_email, role)


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
    if user_domain.get_project_access(user_email, project) and project_name == project:
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
    if is_request_deletion_user(project, user_email) and project_name == project:
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


def remove_project(project_name: str, user_email: str) -> object:
    """Delete project information."""
    project = project_name.lower()
    Status = namedtuple(
        'Status',
        'are_findings_masked are_users_removed is_project_finished are_resources_removed'
    )
    response = Status(False, False, False, False)
    data = project_dal.get_attributes(project, ['project_status'])
    validation = False
    if user_email:
        validation = is_alive(project) and user_domain.get_project_access(user_email, project)
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
    return response


def remove_all_users_access(project: str) -> bool:
    """Remove user access to project."""
    user_active = get_users(project)
    user_suspended = get_users(project, active=False)
    all_users = user_active + user_suspended
    are_users_removed = True
    for user in all_users:
        is_user_removed = remove_user_access(project, user, 'customeradmin')
        if is_user_removed:
            are_users_removed = True
        else:
            are_users_removed = False
            break
    return are_users_removed


def remove_user_access(project: str, user_email: str, role: str) -> bool:
    """Remove user access to project."""
    project_dal.remove_user_role(project, user_email, role)
    return project_dal.remove_access(user_email, project)


def validate_tags(tags: List[str]) -> List[str]:
    """Validate tags array."""
    tags_validated = []
    pattern = re.compile('^[a-z0-9]+(?:-[a-z0-9]+)*$')
    for tag in tags:
        if pattern.match(tag):
            tags_validated.append(tag)
        else:
            # Invalid tag
            pass
    return tags_validated


def is_alive(project: str) -> bool:
    return project_dal.is_alive(project)


def is_request_deletion_user(project: str, user_email: str) -> bool:
    return project_dal.is_request_deletion_user(project, user_email)


def total_vulnerabilities(finding_id: str) -> Dict[str, int]:
    """Get total vulnerabilities in new format."""
    finding = {'openVulnerabilities': 0, 'closedVulnerabilities': 0}
    if finding_domain.validate_finding(finding_id):
        vulnerabilities = finding_dal.get_vulnerabilities(finding_id)
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
        if finding_domain.validate_finding(fin['finding_id']):
            vulnerabilities = finding_dal.get_vulnerabilities(
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


def get_max_severity(findings: List[Dict[str, FindingType]]) -> float:
    """Get maximum severity of a project."""
    total_severity = cast(List[float], [fin.get('cvss_temporal') for fin in findings])
    if total_severity:
        max_severity: float = max(total_severity)
    else:
        max_severity = 0
    return max_severity if max_severity else 0.0


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
        if finding_domain.validate_finding(finding['finding_id']):
            vulnerabilities = finding_dal.get_vulnerabilities(str(finding.get('finding_id', '')))
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
    accepted_vuln = 0
    in_progress_vuln: int = 0
    undefined_treatment: int = 0
    for finding in findings:
        fin_treatment = cast(List[Dict[str, str]],
                             finding.get('historic_treatment', [{}]))[-1].get('treatment')
        if finding_domain.validate_finding(finding['finding_id']):
            open_vulns = int(total_vulnerabilities(
                str(finding['finding_id'])).get('openVulnerabilities', ''))
            if fin_treatment == 'ACCEPTED':
                accepted_vuln += open_vulns
            elif fin_treatment == 'IN PROGRESS':
                in_progress_vuln += open_vulns
            else:
                undefined_treatment += open_vulns
    treatment = {
        'accepted': accepted_vuln,
        'inProgress': in_progress_vuln,
        'undefined': undefined_treatment
    }
    return treatment


def is_finding_in_drafts(finding_id: str) -> bool:
    release_date: Dict[str, str] = cast(Dict[str, str],
                                        finding_dal.get_attributes(finding_id, ['releaseDate']))
    retval = False
    if release_date:
        tzn = pytz.timezone('America/Bogota')
        release_datetime = datetime.strptime(
            str(release_date.get('releaseDate', '')).split(' ')[0],
            '%Y-%m-%d'
        ).date()
        now_time = datetime.now(tz=tzn).date()
        if release_datetime > now_time:
            retval = True
        else:
            # Finding is currently released
            pass
    else:
        retval = True
    return retval


def get_current_month_authors(project_name: str) -> str:
    return project_dal.get_current_month_authors(project_name)


def get_current_month_commits(project_name: str) -> str:
    return project_dal.get_current_month_commits(project_name)


def update(project_name: str, data: ProjectType) -> bool:
    return project_dal.update(project_name, data)


def list_drafts(project_name: str) -> List[str]:
    return project_dal.list_drafts(project_name)


def list_comments(project_name: str, user_role: str) -> List[CommentType]:
    comments = [comment_domain.fill_comment_data(user_role, comment)
                for comment in project_dal.get_comments(project_name)]
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


def get_managers(project_name: str) -> Union[str, List[str]]:
    project = project_dal.get(project_name)
    is_admin = cast(List[str], project[0].get('customeradmin', ''))
    if is_admin is None:
        is_admin = ''
    return is_admin
