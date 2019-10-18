"""Domain functions for projects."""

from __future__ import absolute_import
import threading
import re
from datetime import datetime
from decimal import Decimal
import pytz

from django.conf import settings

from __init__ import FI_MAIL_REPLYERS
from app.dal import integrates_dal, project as project_dal
from app.domain import vulnerability as vuln_domain
from app.dto.finding import (
    total_vulnerabilities
)
from app.mailer import send_mail_comment
from app.util import format_comment_date


def get_email_recipients(project_name):
    """Get the recipients of the comment email."""
    recipients = [str(user) for user in get_users(project_name)]
    replyers = FI_MAIL_REPLYERS.split(',')
    recipients += replyers

    return recipients


def send_comment_mail(project_name, email, comment_data):
    """Send a mail in a project."""
    parent = comment_data['parent']
    recipients = get_email_recipients(project_name)
    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    mail_context = {
        'project': project_name,
        'user_email': email,
        'comment_type': 'project',
        'parent': parent,
        'comment': comment_data['content'].replace('\n', ' '),
        'comment_url':
            base_url + '/project/{project!s}/comments'
        .format(project=project_name)
    }
    email_send_thread = threading.Thread(
        name='New project email thread',
        target=send_mail_comment,
        args=(recipients,
              mail_context))
    email_send_thread.start()


def add_comment(project_name, email, comment_data):
    """Add comment in a project."""
    send_comment_mail(project_name, email, comment_data)
    return integrates_dal.add_project_comment_dynamo(project_name,
                                                     email,
                                                     comment_data)


def validate_tags(tags):
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


def validate_project(project):
    """Validate if a project exist and is not deleted."""
    project_info = integrates_dal.get_project_attributes_dynamo(
        project, ['project_name', 'deletion_date'])
    is_valid_project = False
    if project_info:
        if project_info.get('deletion_date'):
            is_valid_project = False
        else:
            is_valid_project = True
    else:
        is_valid_project = False
    return is_valid_project


def get_vulnerabilities(findings, vuln_type):
    """Get total vulnerabilities by type."""
    vulnerabilities = \
        [total_vulnerabilities(fin['finding_id']).get(vuln_type)
         for fin in findings]
    vulnerabilities = sum(vulnerabilities)
    return vulnerabilities


def get_pending_closing_check(project):
    """Check for pending closing checks."""
    pending_closing = len(
        integrates_dal.get_remediated_project_dynamo(project))
    return pending_closing


def get_last_closing_vuln(findings):
    """Get day since last vulnerability closing."""
    closing_dates = []
    for fin in findings:
        vulnerabilities = integrates_dal.get_vulnerabilities_dynamo(
            fin['finding_id'])
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
        tzn = pytz.timezone(settings.TIME_ZONE)
        last_closing = \
            Decimal((datetime.now(tz=tzn).date() -
                     current_date).days).quantize(Decimal('0.1'))
    else:
        last_closing = Decimal(0)
    return last_closing


def get_last_closing_date(vulnerability):
    """Get last closing date of a vulnerability."""
    current_state = vuln_domain.get_last_approved_state(vulnerability)
    last_closing_date = None

    if current_state and current_state.get('state') == 'closed':
        last_closing_date = datetime.strptime(
            current_state.get('date').split(' ')[0],
            '%Y-%m-%d'
        )
        tzn = pytz.timezone(settings.TIME_ZONE)
        last_closing_date = last_closing_date.replace(tzinfo=tzn).date()
    else:
        # Vulnerability does not have closing date
        pass
    return last_closing_date


def is_vulnerability_closed(vuln):
    """Return if a vulnerability is closed."""
    is_vuln_closed = vuln_domain.get_last_approved_status(vuln) == 'closed'
    return is_vuln_closed


def get_max_severity(findings):
    """Get maximum severity of a project."""
    total_severity = [fin.get('cvss_temporal') for fin in findings]
    if total_severity:
        max_severity = max(total_severity)
    else:
        max_severity = 0
    return max_severity


def get_max_open_severity(findings):
    """Get maximum severity of project with open vulnerabilities."""
    total_severity = \
        [fin.get('cvss_temporal') for fin in findings
         if total_vulnerabilities(fin['finding_id']).get('openVulnerabilities') > 0]
    if total_severity:
        max_severity = Decimal(max(total_severity)).quantize(Decimal('0.1'))
    else:
        max_severity = Decimal(0).quantize(Decimal('0.1'))
    return max_severity


def get_open_vulnerability_date(vulnerability):
    """Get open vulnerability date of a vulnerability."""
    all_states = vulnerability.get('historic_state')
    current_state = all_states[0]
    open_date = None
    if current_state.get('state') == 'open' and \
       not current_state.get('approval_status'):
        open_date = datetime.strptime(
            current_state.get('date').split(' ')[0],
            '%Y-%m-%d'
        )
        tzn = pytz.timezone('America/Bogota')
        open_date = open_date.replace(tzinfo=tzn).date()
    else:
        # Vulnerability does not have closing date
        pass
    return open_date


def get_mean_remediate(findings):
    """Get mean time to remediate a vulnerability."""
    total_vuln = 0
    total_days = 0
    tzn = pytz.timezone('America/Bogota')
    for finding in findings:
        vulnerabilities = integrates_dal.get_vulnerabilities_dynamo(
            finding['finding_id'])
        for vuln in vulnerabilities:
            open_vuln_date = get_open_vulnerability_date(vuln)
            closed_vuln_date = get_last_closing_date(vuln)
            if open_vuln_date:
                if closed_vuln_date:
                    total_days += int((closed_vuln_date - open_vuln_date).days)
                else:
                    current_day = datetime.now(tz=tzn).date()
                    total_days += int((current_day - open_vuln_date).days)
                total_vuln += 1
            else:
                # Vulnerability does not have an open date
                pass
    if total_vuln:
        mean_vulnerabilities = Decimal(
            round(total_days / float(total_vuln))).quantize(Decimal('0.1'))
    else:
        mean_vulnerabilities = Decimal(0).quantize(Decimal('0.1'))
    return mean_vulnerabilities


def get_total_treatment(findings):
    """Get the total treatment of all the vulnerabilities"""
    accepted_vuln = 0
    in_progress_vuln = 0
    undefined_treatment = 0
    for finding in findings:
        open_vulns = total_vulnerabilities(
            finding['finding_id']).get('openVulnerabilities')
        if finding.get('treatment') == 'ACCEPTED':
            accepted_vuln += open_vulns
        elif finding.get('treatment') == 'IN PROGRESS':
            in_progress_vuln += open_vulns
        else:
            undefined_treatment += open_vulns
    treatment = {
        'accepted': accepted_vuln,
        'inProgress': in_progress_vuln,
        'undefined': undefined_treatment
    }
    return treatment


def is_finding_in_drafts(finding_id):
    release_date = integrates_dal.get_finding_attributes_dynamo(finding_id,
                                                                ['releaseDate']
                                                                )
    retval = False
    if release_date:
        tzn = pytz.timezone('America/Bogota')
        release_datetime = datetime.strptime(
            release_date.get('releaseDate').split(' ')[0],
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


def list_drafts(project_name):
    return project_dal.list_drafts(project_name)


def list_comments(user_email, project_name):
    comments = [{
        'content': comment['content'],
        'created': format_comment_date(comment['created']),
        'created_by_current_user': comment['email'] == user_email,
        'email': comment['email'],
        'fullname': comment['fullname'],
        'id': int(comment['user_id']),
        'modified': format_comment_date(comment['modified']),
        'parent': int(comment['parent'])
    } for comment in integrates_dal.get_project_comments_dynamo(project_name)]

    return comments


def get_active_projects():
    projects = project_dal.get_active_projects()

    return projects


def list_findings(project_name):
    """ Returns the list of finding ids associated with the project"""
    return project_dal.list_findings(project_name)


def get_finding_project_name(finding_id):
    return integrates_dal.get_finding_project(finding_id)


def list_managers(project_name):
    return [manager[0] for manager in project_dal.list_managers(project_name)]


def get_description(project_name):
    return project_dal.get_description(project_name)


def get_users(project_name, active=True):
    return project_dal.get_users(project_name, active)


def remove_all_project_access(project):
    return project_dal.remove_all_project_access(project)
