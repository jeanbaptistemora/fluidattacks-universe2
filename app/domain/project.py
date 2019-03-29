"""Domain functions for projects."""
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

import threading
import re
from decimal import Decimal
import datetime
import pytz

from app.dao import integrates_dao
from app.mailer import send_mail_comment
from app.dto.finding import (
    total_vulnerabilities
)


def comment_has_parent(comment_data):
    """Check if a comment has a parent."""
    return comment_data['parent'] != 0


def get_email_recipients(project_name):
    """Get the recipients of the comment email."""
    project_users = integrates_dao.get_project_users(project_name)
    recipients = [user[0] for user in project_users if user[1] == 1]
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
    return integrates_dao.add_project_comment_dynamo(project_name,
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
    project_info = integrates_dao.get_project_attributes_dynamo(
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
        [total_vulnerabilities(i['finding_id']).get(vuln_type) for i in findings]
    vulnerabilities = sum(vulnerabilities)
    return vulnerabilities


def get_closed_percentage(findings):
    """Calculate closed percentage."""
    total_vuln = 0
    closed_percentage = 0
    for fin in findings:
        vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(
            fin['finding_id'])
        total_vuln += len(vulnerabilities)
    if total_vuln:
        closed_vulnerabilities = get_vulnerabilities(
            findings, 'closedVulnerabilities')
        closed_percentage = Decimal(
            (closed_vulnerabilities * 100.0) / total_vuln).quantize(Decimal("0.1"))
    else:
        closed_percentage = 0
    return closed_percentage


def get_pending_closing_check(project):
    """Check for pending closing checks."""
    pending_closing = len(integrates_dao.get_remediated_project_dynamo(project))
    return pending_closing


def get_last_closing_vuln(findings):
    """Get day since last vulnerability closing."""
    last_closing = 0
    closing_dates = []
    for fin in findings:
        vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(
            fin['finding_id'])
        for vuln in vulnerabilities:
            last_closing_date = get_last_closing_date(vuln)
            if last_closing_date:
                closing_dates.append(last_closing_date)
            else:
                # Vulnerability does not have closing date
                pass
    if closing_dates:
        current_date = max(closing_dates)
        tzn = pytz.timezone('America/Bogota')
        last_closing = \
            int((datetime.datetime.now(tz=tzn).date() - current_date).days)
    else:
        last_closing = 0
    return last_closing


def get_last_closing_date(vulnerability):
    """Get last closing date of a vulnerability."""
    all_states = vulnerability.get('historic_state')
    current_state = all_states[len(all_states) - 1]
    last_closing_date = None
    if current_state.get('state') == 'closed':
        last_closing_date = datetime.datetime.strptime(
            current_state.get('date').split(' ')[0],
            '%Y-%m-%d'
        )
        tzn = pytz.timezone('America/Bogota')
        last_closing_date = last_closing_date.replace(tzinfo=tzn).date()
    else:
        # Vulnerability does not have closing date
        pass
    return last_closing_date


def get_undefined_treatment(findings):
    """Get the total vulnerabilities that does not have treatment."""
    total_open_vuln = 0
    for finding in findings:
        if finding.get('treatment') == 'NEW':
            open_vuln = total_vulnerabilities(
                finding['finding_id']).get('openVulnerabilities')
            total_open_vuln += open_vuln
        else:
            # Finding has treatment defined
            pass
    return total_open_vuln


def get_max_severity(findings):
    """Get maximum severity of a project."""
    total_severity = [fin.get('cvss_temporal') for fin in findings]
    max_severity = max(total_severity)
    return max_severity


def get_max_open_severity(findings):
    """Get maximum severity of project with open vulnerabilities."""
    total_severity = \
        [fin.get('cvss_temporal') for fin in findings
         if total_vulnerabilities(
            fin['finding_id']).get('openVulnerabilities') > 0]
    max_severity = max(total_severity)
    return max_severity
