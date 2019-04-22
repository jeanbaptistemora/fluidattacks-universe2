""" Asynchronous task execution scheduler for FLUIDIntegrates """

# pylint: disable=E0402

from __future__ import absolute_import
from datetime import datetime, timedelta
import logging
import logging.config
import rollbar
from botocore.exceptions import ClientError
from __init__ import (
    FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS, FI_MAIL_ENGINEERING,
    FI_MAIL_REVIEWERS
)
from django.conf import settings
from . import views
from .dao import integrates_dao
from .domain.project import get_last_closing_vuln, get_mean_remediate
from .api.formstack import FormstackAPI
from .dto import remission
from .dto import eventuality
from .dto.finding import finding_vulnerabilities
from .mailer import send_mail_new_vulnerabilities, send_mail_new_remediated, \
    send_mail_new_releases, send_mail_unsolved_events, \
    send_mail_project_deletion
from . import util


logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger(__name__)

BASE_URL = 'https://fluidattacks.com/integrates'
BASE_WEB_URL = 'https://fluidattacks.com/web'


def is_not_a_fluidattacks_email(email):
    return 'fluidattacks.com' not in email


def remove_fluid_from_recipients(emails):
    new_email_list = list(filter(is_not_a_fluidattacks_email, emails))
    return new_email_list


def get_event(event_id):
    event = eventuality.event_data(event_id)
    return event


def is_a_unsolved_event(event):
    return event['eventStatus'] == 'UNSOLVED'


def get_events_submissions(project):
    formstack_api = FormstackAPI()
    return formstack_api.get_eventualities(project)['submissions']


def get_unsolved_events(project):
    events_submissions = get_events_submissions(project)

    events = [get_event(x['id']) for x in events_submissions]
    unsolved_events = list(filter(is_a_unsolved_event, events))
    return unsolved_events


def extract_info_from_event_dict(event_dict):
    return {'type': event_dict['eventType'], 'details': event_dict['detail']}


def send_unsolved_events_email(project):
    unsolved_events = get_unsolved_events(project)
    mail_to = get_external_recipients(project)
    project_info = integrates_dao.get_project_dynamo(project)
    if project_info and \
            project_info[0].get('type') == 'continuous':
        mail_to.append(FI_MAIL_CONTINUOUS)
        mail_to.append(FI_MAIL_PROJECTS)
    events_info_for_email = [extract_info_from_event_dict(x)
                             for x in unsolved_events]
    context = {'project': project.capitalize(),
               'events': events_info_for_email}
    if not context['events'] or not mail_to:
        context = []
    else:
        send_mail_unsolved_events(mail_to, context)


def get_external_recipients(project):
    recipients = integrates_dao.get_project_users(project)
    recipients_list = [x[0] for x in recipients if x[1] == 1]
    return remove_fluid_from_recipients(recipients_list)


def get_new_vulnerabilities():
    """Summary mail send with the findings of a project."""
    # pylint: disable-msg=R0914
    projects = integrates_dao.get_registered_projects()
    for project in projects:
        project = str.lower(str(project[0]))
        context = {'findings': list(), 'findings_working_on': list()}
        delta_total = 0
        try:
            finding_requests = integrates_dao.get_findings_dynamo(project,
                                                                  'finding_id')
            for finding in finding_requests:
                message = ''
                finding['id'] = finding['finding_id']
                act_finding = finding_vulnerabilities(str(finding['id']))
                row = integrates_dao.get_vulns_by_id_dynamo(
                    project,
                    int(finding['id'])
                )
                if str.lower(str(act_finding['projectName'])) == project and \
                        'releaseDate' in act_finding and row:
                    finding_url = '{url!s}/dashboard#!/project/{project!s}/' \
                        '{finding!s}/description' \
                        .format(url=BASE_URL,
                                project=project,
                                finding=finding['id'])
                    has_treatment = finding_has_treatment(
                        act_finding,
                        finding_url)
                    if has_treatment:
                        context['findings_working_on'].append(has_treatment)
                    else:
                        message = 'Finding {finding!s} of project {project!s} ' \
                            'has defined treatment' \
                            .format(finding=finding['id'], project=project)
                        LOGGER.info(message)
                    delta = int(act_finding['openVulnerabilities']) - \
                        int(row[0]['vuln_hoy'])
                    finding_text = format_vulnerabilities(delta, act_finding)
                    if finding_text != '':
                        context['findings'].append({
                            'nombre_hallazgo': finding_text,
                            'url_vuln': finding_url
                        })
                        delta_total = delta_total + abs(delta)
                        integrates_dao.add_or_update_vulns_dynamo(
                            project,
                            int(finding['id']),
                            int(act_finding['openVulnerabilities'])
                        )
                    else:
                        message = 'Finding {finding!s} of project ' \
                            '{project!s} no change during the week' \
                            .format(finding=finding['id'], project=project)
                        LOGGER.info(message)
                else:
                    message = 'Finding {finding!s} of project {project!s} is ' \
                        'not valid' \
                        .format(finding=finding['id'], project=project)
                    LOGGER.info(message)
        except (TypeError, KeyError):
            rollbar.report_message(
                'Error: An error ocurred getting new vulnerabilities '
                'notification email',
                'error')
        if delta_total > 0:
            context['project'] = str.upper(str(project))
            context['project_url'] = '{url!s}/dashboard#!/project/' \
                '{project!s}/indicators' \
                .format(url=BASE_URL, project=project)
            recipients = integrates_dao.get_project_users(project)
            mail_to = [x[0] for x in recipients if x[1] == 1]
            mail_to.append(FI_MAIL_CONTINUOUS)
            mail_to.append(FI_MAIL_PROJECTS)
            send_mail_new_vulnerabilities(mail_to, context)


def format_vulnerabilities(delta, act_finding):
    """Format vulnerabities changes in findings."""
    if delta > 0:
        finding_text = u'{finding!s} (+{delta!s})'.format(
            finding=act_finding['finding'],
            delta=delta)
    elif delta < 0:
        finding_text = u'{finding!s} ({delta!s})'.format(
            finding=act_finding['finding'],
            delta=delta)
    else:
        finding_text = ''
    return finding_text


def finding_has_treatment(act_finding, finding_url):
    """Validate if a finding has treatment."""
    if ('releaseDate' in act_finding) and \
            (act_finding['estado'] != 'Cerrado'):
        if 'treatment' in act_finding and \
                act_finding['treatment'] == 'NEW':
            finding_name = act_finding['finding'] + ' -' + \
                act_finding['edad'] + ' day(s)-'
            resp = {
                'hallazgo_pendiente': finding_name,
                'url_hallazgo': finding_url
            }
        else:
            resp = False
    else:
        resp = False
    return resp


def update_new_vulnerabilities():
    """Summary mail send to update the vulnerabilities of a project."""
    projects = integrates_dao.get_registered_projects()
    for project in projects:
        try:
            project = str.lower(str(project[0]))
            old_findings = integrates_dao.get_vulns_by_project_dynamo(project)
            finding_requests = integrates_dao.get_findings_dynamo(project, 'finding_id')
            if len(old_findings) != len(finding_requests):
                delta = abs(len(old_findings) - len(finding_requests))
                for finding in finding_requests[-delta:]:
                    act_finding = finding_vulnerabilities(str(finding['finding_id']))
                    if 'releaseDate' in act_finding:
                        integrates_dao.add_or_update_vulns_dynamo(
                            project,
                            int(finding['finding_id']), 0)
            else:
                message = 'Project {project!s} does not have new vulnerabilities' \
                    .format(project=project)
                LOGGER.info(message)
        except (TypeError, KeyError):
            rollbar.report_message('Error: \
An error ocurred updating new vulnerabilities', 'error')


def get_remediated_findings():
    """Summary mail send with findings that have not been verified yet."""
    findings = integrates_dao.get_remediated_allfin_dynamo(True)
    if findings != []:
        try:
            mail_to = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
            context = {'findings': list()}
            cont = 0
            for finding in findings:
                context['findings'].append({
                    'finding_name': finding['finding_name'],
                    'finding_url':
                    '{url!s}/dashboard#!/project/{project!s}/{finding!s}/description'
                        .format(url=BASE_URL,
                                project=str.lower(str(finding['project'])),
                                finding=finding['finding_id']),
                    'project': str.upper(str(finding['project']))})
                cont += 1
            context['total'] = cont
            send_mail_new_remediated(mail_to, context)
        except (TypeError, KeyError):
            rollbar.report_message(
                'Warning: An error ocurred getting data for remediated email',
                'warning')
    else:
        LOGGER.info('There are no findings to verificate')


def weekly_report():
    """Save weekly report in dynamo."""
    init_date = (datetime.today() - timedelta(days=7)).date()
    final_date = (datetime.today() - timedelta(days=1)).date()
    all_companies = integrates_dao.get_all_companies()
    all_users = [all_users_formatted(x) for x in all_companies]
    registered_users = integrates_dao.all_users_report('FLUID',
                                                       final_date)
    logged_users = integrates_dao.logging_users_report('FLUID',
                                                       init_date,
                                                       final_date)
    integrates_dao.weekly_report_dynamo(
        str(init_date),
        str(final_date),
        registered_users[0][0],
        logged_users[0][0],
        all_users
    )


def all_users_formatted(company):
    """Format total users by company."""
    total_users = integrates_dao.get_all_users(company)
    all_users_by_company = {company[0]: int(total_users[0][0])}
    return all_users_by_company


def inactive_users():
    final_date = (datetime.today() - timedelta(days=7))
    inac_users = integrates_dao.all_inactive_users()
    for user in inac_users:
        if user[1] <= final_date:
            integrates_dao.delete_user(user[0])


def get_new_releases():
    """Summary mail send with findings that have not been released yet."""
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    context = {'findings': list()}
    cont = 0
    for project in projects:
        try:
            finding_requests = api.get_findings(project)['submissions']
            project = str.lower(str(project[0]))
            for finding in finding_requests:
                finding_parsed = finding_vulnerabilities(finding['id'])
                project_fin = str.lower(str(finding_parsed['projectName']))
                if ('releaseDate' not in finding_parsed and
                        project_fin == project):
                    context['findings'].append({
                        'finding_name': finding_parsed['finding'],
                        'finding_url':
                        '{url!s}/dashboard#!/project/{project!s}/{finding!s}'
                        '/description'
                            .format(url=BASE_URL,
                                    project=project,
                                    finding=finding['id']),
                        'project': str.upper(str(project))
                    })
                    cont += 1
        except (TypeError, KeyError):
            rollbar.report_message(
                'Warning: An error ocurred getting data for new drafts email',
                'warning')
    if cont > 0:
        context['total'] = cont
        approvers = FI_MAIL_REVIEWERS.split(',')
        mail_to = [FI_MAIL_ENGINEERING]
        mail_to.extend(approvers)
        send_mail_new_releases(mail_to, context)
    else:
        LOGGER.info('There are no new drafts')


def send_unsolved_to_all():
    """Send email with unsolved events to all projects """
    projects = integrates_dao.get_registered_projects()
    list(map(lambda x: send_unsolved_events_email(x[0]), projects))


def deletion(project, days_to_send, days_to_delete):
    formstack_api = FormstackAPI()
    remission_submissions = formstack_api.get_remmisions(project)['submissions']
    if remission_submissions:
        remissions_list = [
            remission.create_dict(
                formstack_api.get_submission(x['id'])
            ) for x in remission_submissions]
        filtered_remissions = list(filter(lambda x: x['FLUID_PROJECT'].lower()
                                          == project.lower(), remissions_list))
        project_info = integrates_dao.get_project_dynamo(project)
        if filtered_remissions and project_info:
            lastest_remission = remission.get_lastest(filtered_remissions)
            if lastest_remission['LAST_REMISSION'] == 'Si' and \
               lastest_remission['APPROVAL_STATUS'] == 'Approved' and \
               project_info[0]['type'] == 'oneshot':
                days_until_now = \
                    remission.days_until_now(lastest_remission['TIMESTAMP'])
                if days_until_now in days_to_send:
                    context = {'project': project.capitalize()}
                    mail_to = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
                    send_mail_project_deletion(mail_to, context)
                    was_deleted = False
                    was_email_sended = True
                elif days_until_now in days_to_delete:
                    views.delete_project(project)
                    integrates_dao.add_attribute_dynamo(
                        'FI_projects',
                        ['project_name', project.lower()],
                        'deletion_date',
                        datetime.today().isoformat(' '))
                    was_deleted = True
                    was_email_sended = False
                else:
                    was_email_sended = False
                    was_deleted = False
            else:
                was_email_sended = False
                was_deleted = False
        else:
            was_email_sended = False
            was_deleted = False
    else:
        was_email_sended = False
        was_deleted = False
    return [was_email_sended, was_deleted]


def deletion_of_finished_project():
    rollbar.report_message(
        'Warning: Function to delete finished project is running '
        'deletion finished project',
        'warning')
    today_weekday = datetime.today().weekday()
    if today_weekday == 0:
        days_to_send = [6, 7]
        days_to_delete = [-1]
    elif today_weekday == 1:
        days_to_send = [6]
        days_to_delete = [7, 8]
    elif today_weekday == 4:
        days_to_send = [5, 6]
        days_to_delete = [7]
    elif today_weekday == 5:
        days_to_send = [-1]
        days_to_delete = [6, 7]
    elif today_weekday == 6:
        days_to_send = [-1]
        days_to_delete = [-1]
    else:
        days_to_send = [6]
        days_to_delete = [7]
    projects = integrates_dao.get_registered_projects()
    list(map(lambda x: deletion(x[0], days_to_send, days_to_delete), projects))


def update_indicators():
    """Update in dynamo indicators."""
    projects = integrates_dao.get_registered_projects()
    table_name = 'FI_projects'
    for project in projects:
        try:
            project = str.lower(str(project[0]))
            findings = integrates_dao.get_findings_released_dynamo(
                project, 'finding_id, treatment, cvss_temporal')
            last_closing_date = get_last_closing_vuln(findings)
            mean_remediate = get_mean_remediate(findings)
            primary_keys = ['project_name', project]
            indicators = {
                'last_closing_date': last_closing_date,
                'mean_remediate': mean_remediate
            }
            response = integrates_dao.add_multiple_attributes_dynamo(
                table_name, primary_keys, indicators)
            if response:
                util.invalidate_cache(project)
            else:
                rollbar.report_message(
                    'Error: An error ocurred updating indicators of '
                    'the project {project} in dynamo'.format(project=project),
                    'error')
        except (KeyError, ClientError):
            rollbar.report_message(
                'Error: An error ocurred updating '
                'indicators of the project {project}'.format(project=project),
                'error')
