""" Asynchronous task execution scheduler for FLUIDIntegrates """

# pylint: disable=E0402

from __future__ import absolute_import
from datetime import datetime, timedelta
from collections import OrderedDict
import logging
import logging.config
import rollbar
from botocore.exceptions import ClientError
from __init__ import (
    FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS,
    FI_MAIL_REVIEWERS
)
from django.conf import settings
from . import views
from .dal import integrates_dal, project as project_dal
from .domain.finding import (get_age_finding, get_tracking_vulnerabilities)
from .domain.project import (
    get_last_closing_vuln, get_mean_remediate, get_max_open_severity,
    get_total_treatment
)
from .dal.helpers.formstack import FormstackAPI
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


def get_event(event_id, context):
    event = eventuality.event_data(event_id, context)
    return event


def is_a_unsolved_event(event):
    return event['eventStatus'] == 'UNSOLVED'


def get_events_submissions(project):
    formstack_api = FormstackAPI()
    return formstack_api.get_eventualities(project)['submissions']


def get_unsolved_events(project, context):
    events_submissions = get_events_submissions(project)

    events = [get_event(x['id'], context) for x in events_submissions]
    unsolved_events = list(filter(is_a_unsolved_event, events))
    return unsolved_events


def extract_info_from_event_dict(event_dict):
    return {'type': event_dict['eventType'], 'details': event_dict['detail']}


def send_unsolved_events_email(project, context):
    unsolved_events = get_unsolved_events(project, context)
    mail_to = get_external_recipients(project)
    project_info = integrates_dal.get_project_dynamo(project)
    if project_info and \
            project_info[0].get('type') == 'continuous':
        mail_to.append(FI_MAIL_CONTINUOUS)
        mail_to.append(FI_MAIL_PROJECTS)
    events_info_for_email = [extract_info_from_event_dict(x)
                             for x in unsolved_events]
    context_event = {'project': project.capitalize(),
                     'events': events_info_for_email}
    if context_event['events'] and mail_to:
        send_mail_unsolved_events(mail_to, context_event)


def get_external_recipients(project):
    recipients = integrates_dal.get_project_users(project)
    recipients_list = [x[0] for x in recipients if x[1] == 1]
    return remove_fluid_from_recipients(recipients_list)


def get_finding_url(finding):
    url = '{url!s}/dashboard#!/project/{project!s}/' '{finding!s}/description' \
        .format(url=BASE_URL,
                project=finding['project_name'],
                finding=finding['finding_id'])
    return url


def get_status_vulns_by_time_range(vulns, first_day, last_day,
                                   findings_released):
    """Get total closed and found vulnerabilities by time range"""
    resp = {'found': 0, 'closed': 0, 'accepted': 0}
    count = 0
    for vuln in vulns:
        historic_states = vuln['historic_state']
        last_state = historic_states[-1]
        if first_day <= last_state['date'] <= last_day and last_state['state'] == 'closed':
            resp['closed'] += 1
        if first_day <= historic_states[0]['date'] <= last_day:
            count += 1
    resp['found'] = count
    resp['accepted'] = get_accepted_vulns(findings_released, vulns, first_day, last_day)
    return resp


def create_weekly_date(first_date):
    """Create format weekly date"""
    first_date = datetime.strptime(first_date, "%Y-%m-%d")
    begin = first_date - timedelta(days=(first_date.isoweekday() - 1) % 7)
    end = begin + timedelta(days=6)
    if begin.year != end.year:
        date = '{0:%b} {0.day}, {0.year} - {1:%b} {1.day}, {1.year}'
    elif begin.month != end.month:
        date = "{0:%b} {0.day} - {1:%b} {1.day}, {1.year}"
    else:
        date = "{0:%b} {0.day} - {1.day}, {1.year}"
    return date.format(begin, end)


def get_accepted_vulns(findings_released, vulns, first_day, last_day):
    """Get all vulnerabilities accepted by time range"""
    accepted = 0
    for finding in findings_released:
        if finding['treatment'] == 'ACCEPTED':
            for vuln in vulns:
                accepted += get_by_time_range(finding, vuln, first_day, last_day)
    return accepted


def get_by_time_range(finding, vuln, first_day, last_day):
    """Accepted vulnerability of finding."""
    count = 0
    if finding['finding_id'] == vuln['finding_id']:
        history = vuln['historic_state'][-1]
        if first_day <= history['date'] <= last_day and history['state'] == 'open':
            count += 1
        else:
            # date of vulnerabilities outside of time_range or state not open
            pass
    else:
        # vulnerabilities is from finding
        pass
    return count


def create_register_by_week(project):
    """Create weekly vulnerabilities registry by project"""
    accepted = 0
    closed = 0
    found = 0
    all_registers = OrderedDict()
    findings_released = integrates_dal.get_findings_released_dynamo(project)
    vulns = get_all_vulns_by_project(findings_released)
    if vulns:
        first_day, last_day = get_first_week_dates(vulns)
        first_day_last_week = get_date_last_vulns(vulns)
        while first_day <= first_day_last_week:
            result_vulns_by_week = get_status_vulns_by_time_range(vulns, first_day,
                                                                  last_day,
                                                                  findings_released)
            accepted += result_vulns_by_week['accepted']
            closed += result_vulns_by_week['closed']
            found += result_vulns_by_week['found']
            if any(status_vuln for status_vuln in result_vulns_by_week.values()):
                week_dates = create_weekly_date(first_day)
                all_registers[week_dates] = {
                    'found': found,
                    'closed': closed,
                    'accepted': accepted,
                    'assumed_closed': accepted + closed
                }
            first_day = str(datetime.strptime(first_day, "%Y-%m-%d") +
                            timedelta(days=7)).split(' ')[0]
            last_day = str(datetime.strptime(last_day, "%Y-%m-%d") +
                           timedelta(days=7)).split(' ')[0]
    return create_data_format_chart(all_registers)


def create_data_format_chart(all_registers):
    result_data = []
    plot_points = {
        'found': [],
        'closed': [],
        'accepted': [],
        'assumed_closed': []}
    for week, dict_status in all_registers.items():
        for status in plot_points:
            plot_points[status].append({'x': week, 'y': dict_status[status]})
    for status in plot_points:
        result_data.append(plot_points[status])
    return result_data


def get_all_vulns_by_project(findings_released):
    """Get all vulnerabilities by project"""
    vulns = []
    for finding in findings_released:
        vulns += integrates_dal.get_vulnerabilities_dynamo(finding['finding_id'])
    return vulns


def get_first_week_dates(vulns):
    """Get first week vulnerabilities"""
    first_date = min([datetime.strptime(vuln['historic_state'][0]['date'],
                                        "%Y-%m-%d %H:%M:%S") for vuln in vulns])
    day_week = first_date.weekday()
    first_day = first_date - timedelta(days=day_week)
    last_day = first_day + timedelta(days=6)
    return str(first_day).split(' ')[0], str(last_day).split(' ')[0]


def get_date_last_vulns(vulns):
    """Get date of the last vulnerabilities"""
    last_date = max([datetime.strptime(vuln['historic_state'][-1]['date'],
                                       "%Y-%m-%d %H:%M:%S") for vuln in vulns])
    day_week = last_date.weekday()
    first_day = str(last_date - timedelta(days=day_week)).split(' ')[0]
    return first_day


def get_new_vulnerabilities():
    """Summary mail send with the findings of a project."""
    projects = project_dal.get_active_projects()
    for project in projects:
        project = project.lower()
        context = {'updated_findings': list(), 'no_treatment_findings': list()}
        try:
            finding_requests = integrates_dal.get_findings_released_dynamo(project)
            for act_finding in finding_requests:
                finding_url = get_finding_url(act_finding)
                msj_finding_pending = \
                    create_msj_finding_pending(act_finding, context)
                delta = calculate_vulnerabilities(act_finding)
                finding_text = format_vulnerabilities(delta, act_finding)
                if msj_finding_pending:
                    context['no_treatment_findings'].append({'finding_name': msj_finding_pending,
                                                             'finding_url': finding_url})
                if finding_text:
                    context['updated_findings'].append({'finding_name': finding_text,
                                                        'finding_url': finding_url})
                context['project'] = str.upper(str(act_finding['project_name']))
                context['project_url'] = '{url!s}/dashboard#!/project/' \
                    '{project!s}/indicators' \
                    .format(url=BASE_URL, project=act_finding['project_name'])
        except (TypeError, KeyError):
            rollbar.report_message(
                'Error: An error ocurred getting new vulnerabilities '
                'notification email',
                'error')
        if context['updated_findings']:
            mail_to = prepare_mail_recipients(project)
            send_mail_new_vulnerabilities(mail_to, context)


def prepare_mail_recipients(project):
    recipients = integrates_dal.get_project_users(project)
    mail_to = [x[0] for x in recipients if x[1] == 1]
    mail_to.append(FI_MAIL_CONTINUOUS)
    return mail_to


def calculate_vulnerabilities(act_finding):
    vulns = integrates_dal.get_vulnerabilities_dynamo(act_finding['finding_id'])
    all_tracking = get_tracking_vulnerabilities(act_finding, vulns)
    delta_total = 0
    if len(all_tracking) > 1:
        if (datetime.strptime(all_tracking[-1]['date'], "%Y-%m-%d")) > (datetime.now() -
                                                                        timedelta(days=8)):
            delta_open = abs(all_tracking[-1]['open'] - all_tracking[-2]['open'])
            delta_closed = abs(all_tracking[-1]['closed'] - all_tracking[-2]['closed'])
            delta_total = delta_open - delta_closed
    elif len(all_tracking) == 1 and \
        (datetime.strptime(all_tracking[-1]['date'], "%Y-%m-%d")) > \
            (datetime.now() - timedelta(days=8)):
        delta_open = all_tracking[-1]['open']
        delta_closed = all_tracking[-1]['closed']
        delta_total = delta_open - delta_closed
    return delta_total


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
        message = 'Finding {finding!s} of project ' \
            '{project!s} no change during the week' \
            .format(finding=act_finding['finding_id'],
                    project=act_finding['project_name'])
        LOGGER.info(message)
    return finding_text


def create_msj_finding_pending(act_finding, context):
    """Validate if a finding has treatment."""
    finding_vulns = finding_vulnerabilities(act_finding['finding_id'])
    state = finding_vulns['estado'].lower()
    if act_finding['treatment'] == 'NEW' and state == 'abierto':
        days = get_age_finding(act_finding)
        finding_name = act_finding['finding'] + ' -' + \
            str(days) + ' day(s)-'
        result = finding_name
    else:
        message = 'Finding {finding!s} of project {project!s} ' \
            'has defined treatment' \
            .format(finding=act_finding['finding_id'],
                    project=act_finding['project_name'])
        util.cloudwatch_log(context, message)
        result = ''
    return result


def get_remediated_findings():
    """Summary mail send with findings that have not been verified yet."""
    projects = project_dal.get_active_projects()
    for project in projects:
        findings = integrates_dal.get_remediated_project_dynamo(project)
        if findings:
            try:
                mail_to = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
                context = {'findings': list()}
                for finding in findings:
                    context['findings'].append({
                        'finding_name': finding['finding'],
                        'finding_url':
                        '{url!s}/dashboard#!/project/{project!s}/{finding!s}/description'
                            .format(url=BASE_URL,
                                    project=str.lower(str(finding['project_name'])),
                                    finding=finding['finding_id']),
                        'project': str.upper(str(finding['project_name']))})
                context['total'] = len(findings)
                send_mail_new_remediated(mail_to, context)
            except (TypeError, KeyError) as ex:
                rollbar.report_message(
                    'Warning: An error ocurred getting data for remediated email',
                    'warning', extra_data=ex, payload_data=locals())
        else:
            LOGGER.info('There are no findings to verificate')


def weekly_report():
    """Save weekly report in dynamo."""
    init_date = (datetime.today() - timedelta(days=7)).date()
    final_date = (datetime.today() - timedelta(days=1)).date()
    all_companies = integrates_dal.get_all_companies()
    all_users = [all_users_formatted(x) for x in all_companies]
    registered_users = integrates_dal.all_users_report('FLUID',
                                                       final_date)
    logged_users = integrates_dal.logging_users_report('FLUID',
                                                       init_date,
                                                       final_date)
    integrates_dal.weekly_report_dynamo(
        str(init_date),
        str(final_date),
        registered_users[0][0],
        logged_users[0][0],
        all_users
    )


def all_users_formatted(company):
    """Format total users by company."""
    total_users = integrates_dal.get_all_users(company)
    all_users_by_company = {company[0]: int(total_users[0][0])}
    return all_users_by_company


def inactive_users():
    final_date = (datetime.today() - timedelta(days=7))
    inac_users = integrates_dal.all_inactive_users()
    for user in inac_users:
        if user[1] <= final_date:
            integrates_dal.delete_user(user[0])


def get_new_releases():
    """Summary mail send with findings that have not been released yet."""
    projects = integrates_dal.get_registered_projects()
    api = FormstackAPI()
    context_finding = {'findings': list()}
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
                    context_finding['findings'].append({
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
        context_finding['total'] = cont
        approvers = FI_MAIL_REVIEWERS.split(',')
        mail_to = [FI_MAIL_PROJECTS]
        mail_to.extend(approvers)
        send_mail_new_releases(mail_to, context_finding)
    else:
        rollbar.report_message('Warning: There are no new drafts',
                               'warning')


def send_unsolved_to_all(context):
    """Send email with unsolved events to all projects """
    projects = project_dal.get_active_projects()
    return [send_unsolved_events_email(x[0], context) for x in projects]


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
        project_info = integrates_dal.get_project_dynamo(project)
        if filtered_remissions and project_info:
            lastest_remission = remission.get_lastest(filtered_remissions)
            if lastest_remission['LAST_REMISSION'] == 'Si' and \
               lastest_remission['APPROVAL_STATUS'] == 'Approved' and \
               project_info[0].get('type') == 'oneshot':
                days_until_now = \
                    remission.days_until_now(lastest_remission['TIMESTAMP'])
                is_sended = is_deleted(
                    project,
                    days_until_now, days_to_send, days_to_delete)
                was_deleted = is_sended[0]
                was_email_sended = is_sended[1]
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


def is_deleted(project,
               days_until_now, days_to_send, days_to_delete):
    """Project was deleted """
    if days_until_now in days_to_send:
        context_project = {'project': project.capitalize()}
        mail_to = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
        send_mail_project_deletion(mail_to, context_project)
        was_deleted = False
        was_email_sended = True
    elif days_until_now >= days_to_delete:
        views.delete_project(project)
        integrates_dal.add_attribute_dynamo(
            'FI_projects',
            ['project_name', project.lower()],
            'deletion_date',
            datetime.today().isoformat(' '))
        was_deleted = True
        was_email_sended = False
    else:
        was_email_sended = False
        was_deleted = False
    return [was_deleted, was_email_sended]


def deletion_of_finished_project():
    rollbar.report_message(
        'Warning: Function to delete finished project is running '
        'deletion finished project',
        'warning')
    today_weekday = datetime.today().weekday()
    if today_weekday == 0:
        days_to_send = [6, 7]
        days_to_delete = -1
    elif today_weekday == 1:
        days_to_send = [6]
        days_to_delete = 7
    elif today_weekday == 4:
        days_to_send = [5, 6]
        days_to_delete = 7
    elif today_weekday == 5:
        days_to_send = [-1]
        days_to_delete = 6
    elif today_weekday == 6:
        days_to_send = [-1]
        days_to_delete = -1
    else:
        days_to_send = [6]
        days_to_delete = 7
    projects = integrates_dal.get_registered_projects()
    return [deletion(x[0], days_to_send, days_to_delete)
            for x in projects]


def update_indicators():
    """Update in dynamo indicators."""
    projects = integrates_dal.get_registered_projects()
    table_name = 'FI_projects'
    indicators = {
        'last_closing_date': 0,
        'mean_remediate': 0,
        'max_open_severity': 0,
        'total_treatment': {},
        'remediated_over_time': []
    }
    for project in projects:
        try:
            project = str.lower(str(project[0]))
            findings = integrates_dal.get_findings_released_dynamo(
                project, 'finding_id, treatment, cvss_temporal')
            indicators['last_closing_date'] = get_last_closing_vuln(findings)
            indicators['mean_remediate'] = get_mean_remediate(findings)
            indicators['max_open_severity'] = get_max_open_severity(findings)
            indicators['total_treatment'] = get_total_treatment(findings)
            indicators['remediated_over_time'] = create_register_by_week(project)
            primary_keys = ['project_name', project]
            response = integrates_dal.add_multiple_attributes_dynamo(
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
