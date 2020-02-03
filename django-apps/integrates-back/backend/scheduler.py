""" Asynchronous task execution scheduler for FLUIDIntegrates """


import logging
import logging.config
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta

import rollbar
from botocore.exceptions import ClientError
from django.conf import settings

from backend.domain import (
    finding as finding_domain, project as project_domain,
    user as user_domain, vulnerability as vuln_domain,
    event as event_domain
)
from backend.mailer import (
    send_mail_new_vulnerabilities, send_mail_new_remediated,
    send_mail_new_releases, send_mail_unsolved_events
)

from backend import util
from backend.dal import integrates_dal, project as project_dal

from __init__ import (
    FI_TEST_PROJECTS, FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS, FI_MAIL_REVIEWERS
)

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger(__name__)

BASE_URL = 'https://fluidattacks.com/integrates'
BASE_WEB_URL = 'https://fluidattacks.com/web'


def is_not_a_fluidattacks_email(email):
    return 'fluidattacks.com' not in email


def remove_fluid_from_recipients(emails):
    new_email_list = list(filter(is_not_a_fluidattacks_email, emails))
    return new_email_list


def is_a_unsolved_event(event):
    return event.get('historic_state', [{}])[-1].get('state', '') == 'CREATED'


def get_unsolved_events(project):
    events = project_domain.list_events(project)
    event_list = []
    for event in events:
        event_attr = event_domain.get_event(event)
        event_list.append(event_attr)
    unsolved_events = list(filter(is_a_unsolved_event, event_list))
    return unsolved_events


def extract_info_from_event_dict(event_dict):
    event_dict = {'type': event_dict['event_type'], 'details': event_dict['detail']}
    return event_dict


def send_unsolved_events_email(project):
    unsolved_events = get_unsolved_events(project)
    mail_to = get_external_recipients(project)
    project_info = project_domain.get_project_info(project)
    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    if project_info and \
            project_info[0].get('type') == 'continuous':
        mail_to.append(FI_MAIL_CONTINUOUS)
        mail_to.append(FI_MAIL_PROJECTS)
    else:
        mail_to = []
    events_info_for_email = [extract_info_from_event_dict(x)
                             for x in unsolved_events]
    context_event = {'project': project.capitalize(),
                     'events_len': len(events_info_for_email),
                     'event_url': '{}/project/{}/events'.format(
                         base_url, project)}
    if context_event['events_len'] and mail_to:
        send_mail_unsolved_events(mail_to, context_event)


def get_external_recipients(project):
    recipients = project_domain.get_managers(project)
    return remove_fluid_from_recipients(recipients)


def get_finding_url(finding):
    url = '{url!s}/dashboard#!/project/{project!s}/' '{finding!s}/description' \
        .format(url=BASE_URL,
                project=finding['project_name'],
                finding=finding['finding_id'])
    return url


def get_status_vulns_by_time_range(vulns, first_day, last_day,
                                   findings_released):
    """Get total closed and found vulnerabilities by time range"""
    resp = defaultdict(int)
    for vuln in vulns:
        historic_states = vuln['historic_state']
        last_state = vuln_domain.get_last_approved_state(vuln)

        if last_state and first_day <= last_state['date'] <= last_day and \
           last_state['state'] == 'closed':
            resp['closed'] += 1
        if first_day <= historic_states[0]['date'] <= last_day:
            resp['found'] += 1
    resp['accepted'] = get_accepted_vulns(
        findings_released, vulns, first_day, last_day)
    return resp


def create_weekly_date(first_date):
    """Create format weekly date"""
    first_date = datetime.strptime(first_date, '%Y-%m-%d %H:%M:%S')
    begin = first_date - timedelta(days=(first_date.isoweekday() - 1) % 7)
    end = begin + timedelta(days=6)
    if begin.year != end.year:
        date = '{0:%b} {0.day}, {0.year} - {1:%b} {1.day}, {1.year}'
    elif begin.month != end.month:
        date = '{0:%b} {0.day} - {1:%b} {1.day}, {1.year}'
    else:
        date = '{0:%b} {0.day} - {1.day}, {1.year}'
    return date.format(begin, end)


def get_accepted_vulns(findings_released, vulns, first_day, last_day):
    """Get all vulnerabilities accepted by time range"""
    accepted = 0
    for finding in findings_released:
        historic_treatment = finding.get('historic_treatment', [{}])
        if historic_treatment[-1].get('treatment') == 'ACCEPTED':
            for vuln in vulns:
                accepted += get_by_time_range(finding, vuln, first_day, last_day)
    return accepted


def get_by_time_range(finding, vuln, first_day, last_day):
    """Accepted vulnerability of finding."""
    count = 0
    if finding['finding_id'] == vuln['finding_id']:

        history = vuln_domain.get_last_approved_state(vuln)
        if history and first_day <= history['date'] <= last_day and \
           history['state'] == 'open':
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
            accepted += result_vulns_by_week.get('accepted', 0)
            closed += result_vulns_by_week.get('closed', 0)
            found += result_vulns_by_week.get('found', 0)
            if any(status_vuln for status_vuln in list(result_vulns_by_week.values())):
                week_dates = create_weekly_date(first_day)
                all_registers[week_dates] = {
                    'found': found,
                    'closed': closed,
                    'accepted': accepted,
                    'assumed_closed': accepted + closed
                }
            first_day = str(datetime.strptime(first_day, '%Y-%m-%d %H:%M:%S') +
                            timedelta(days=7))
            last_day = str(datetime.strptime(last_day, '%Y-%m-%d %H:%M:%S') +
                           timedelta(days=7))
    return create_data_format_chart(all_registers)


def create_data_format_chart(all_registers):
    result_data = []
    plot_points = {
        'found': [],
        'closed': [],
        'accepted': [],
        'assumed_closed': []}
    for week, dict_status in list(all_registers.items()):
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
                                        '%Y-%m-%d %H:%M:%S') for vuln in vulns])
    day_week = first_date.weekday()
    first_day_delta = first_date - timedelta(days=day_week)
    first_day = datetime.combine(first_day_delta, datetime.min.time())
    last_day_delta = first_day + timedelta(days=6)
    last_day = datetime.combine(last_day_delta,
                                datetime.max.time().replace(microsecond=0))
    return str(first_day), str(last_day)


def get_date_last_vulns(vulns):
    """Get date of the last vulnerabilities"""
    last_date = max([datetime.strptime(vuln['historic_state'][-1]['date'],
                                       '%Y-%m-%d %H:%M:%S') for vuln in vulns])
    day_week = last_date.weekday()
    first_day = str(last_date - timedelta(days=day_week))
    return first_day


def get_new_vulnerabilities():
    """Summary mail send with the findings of a project."""
    rollbar.report_message(
        'Warning: Function to get new vulnerabilities is running', 'warning')
    projects = project_domain.get_active_projects()
    fin_attrs = 'finding_id, historic_treatment, project_name, finding'
    for project in projects:
        context = {'updated_findings': list(), 'no_treatment_findings': list()}
        try:
            finding_requests = integrates_dal.get_findings_released_dynamo(project, fin_attrs)
            for act_finding in finding_requests:
                finding_url = get_finding_url(act_finding)
                msj_finding_pending = \
                    create_msj_finding_pending(act_finding)
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
                'error', payload_data=locals())
            raise
        if context['updated_findings']:
            mail_to = prepare_mail_recipients(project)
            send_mail_new_vulnerabilities(mail_to, context)


def prepare_mail_recipients(project):
    mail_to = project_domain.get_users(project)
    mail_to.append(FI_MAIL_CONTINUOUS)
    return mail_to


def calculate_vulnerabilities(act_finding):
    vulns = integrates_dal.get_vulnerabilities_dynamo(act_finding['finding_id'])
    all_tracking = finding_domain.get_tracking_vulnerabilities(vulns)
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
        finding_text = '{finding!s} (+{delta!s})'.format(
            finding=act_finding['finding'],
            delta=delta)
    elif delta < 0:
        finding_text = '{finding!s} ({delta!s})'.format(
            finding=act_finding['finding'],
            delta=delta)
    else:
        finding_text = ''
        message = 'Finding {finding!s} of project ' \
            '{project!s} has no changes during the week' \
            .format(finding=act_finding['finding_id'],
                    project=act_finding['project_name'])
        LOGGER.info(message)
    return finding_text


def create_msj_finding_pending(act_finding):
    """Validate if a finding has treatment."""
    historic_treatment = act_finding.get('historic_treatment', [{}])
    open_vulns = [
        vuln for vuln in vuln_domain.get_vulnerabilities(
            act_finding['finding_id'])
        if vuln['current_state'] == 'open']
    if historic_treatment[-1].get('treatment', 'NEW') == 'NEW' and open_vulns:
        days = finding_domain.get_age_finding(act_finding)
        finding_name = act_finding['finding'] + ' -' + \
            str(days) + ' day(s)-'
        result = finding_name
    else:
        result = ''
    return result


def get_remediated_findings():
    """Summary mail send with findings that have not been verified yet."""
    rollbar.report_message(
        'Warning: Function to get remediated findings is running', 'warning')
    active_projects = project_domain.get_active_projects()
    findings = []
    for project in active_projects:
        findings += project_dal.get_pending_verification_findings(project)

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
    rollbar.report_message(
        'Warning: Function to do weekly report in DynamoDB is running', 'warning')
    init_date = \
        (datetime.today() - timedelta(days=7)).date().strftime('%Y-%m-%d')
    final_date = \
        (datetime.today() - timedelta(days=1)).date().strftime('%Y-%m-%d')
    all_companies = user_domain.get_all_companies()
    all_users = [all_users_formatted(x) for x in all_companies]
    registered_users = user_domain.get_all_users_report('FLUID', final_date)
    logged_users = user_domain.logging_users_report(
        'FLUID', init_date, final_date)
    integrates_dal.weekly_report_dynamo(
        init_date,
        final_date,
        registered_users,
        logged_users,
        all_users
    )


def all_users_formatted(company):
    """Format total users by company."""
    total_users = user_domain.get_all_users(company)
    all_users_by_company = {company: total_users}
    return all_users_by_company


def inactive_users():
    rollbar.report_message(
        'Warning: Function to delete inactive users is running', 'warning')
    final_date = (datetime.today() - timedelta(days=7))
    inac_users = user_domain.get_all_inactive_users(
        final_date.strftime('%Y-%m-%d %H:%M:%S'))
    for user in inac_users:
        user_domain.remove_user(user)


def get_new_releases():
    """Summary mail send with findings that have not been released yet."""
    rollbar.report_message('Warning: Function to get new releases is running',
                           'warning')
    test_projects = FI_TEST_PROJECTS.split(',')
    projects = project_domain.get_active_projects()
    email_context = defaultdict(list)
    cont = 0
    for project in projects:
        if project not in test_projects:
            try:
                finding_requests = finding_domain.get_findings(
                    finding_domain.filter_deleted_findings(project_domain.list_drafts(project)))
                for finding in finding_requests:
                    if 'releaseDate' not in finding:
                        submission = finding.get('historicState')
                        status = submission[-1].get('state')
                        category = ('unsubmitted' if status in ('CREATED', 'REJECTED')
                                    else 'unreleased')
                        email_context[category].append({
                            'finding_name': finding.get('finding'),
                            'finding_url':
                            '{url!s}/dashboard#!/project/{project!s}/drafts/'
                            '{finding!s}/description'
                                .format(url=BASE_URL,
                                        project=project,
                                        finding=finding.get('findingId')),
                            'project': project.upper()
                        })
                        cont += 1
            except (TypeError, KeyError):
                rollbar.report_message(
                    'Warning: An error ocurred getting data for new drafts email',
                    'warning')
        else:
            # ignore test projects
            pass
    if cont > 0:
        email_context['total_unreleased'] = len(email_context['unreleased'])
        email_context['total_unsubmitted'] = len(email_context['unsubmitted'])
        approvers = FI_MAIL_REVIEWERS.split(',')
        mail_to = [FI_MAIL_PROJECTS]
        mail_to.extend(approvers)
        send_mail_new_releases(mail_to, email_context)
    else:
        rollbar.report_message('Warning: There are no new drafts',
                               'warning')


def send_unsolved_to_all():
    """Send email with unsolved events to all projects """
    rollbar.report_message('Warning: Function to send email with unsolved events is running',
                           'warning')
    projects = project_domain.get_active_projects()
    return [send_unsolved_events_email(x) for x in projects]


def get_project_indicators(project):
    findings = integrates_dal.get_findings_released_dynamo(
        project, 'finding_id, historic_treatment, cvss_temporal')
    indicators = {
        'last_closing_date': project_domain.get_last_closing_vuln(findings),
        'mean_remediate': project_domain.get_mean_remediate(findings),
        'max_open_severity': project_domain.get_max_open_severity(findings),
        'total_treatment': project_domain.get_total_treatment(findings),
        'remediated_over_time': create_register_by_week(project)
    }
    return indicators


def update_indicators():
    """Update in dynamo indicators."""
    rollbar.report_message(
        'Warning: Function to update indicators in DynamoDB is running', 'warning')
    projects = project_domain.get_active_projects()
    table_name = 'FI_projects'
    for project in projects:
        indicators = get_project_indicators(project)
        primary_keys = ['project_name', project]
        try:
            response = integrates_dal.add_multiple_attributes_dynamo(
                table_name, primary_keys, indicators)
            if response:
                util.invalidate_cache(project)
            else:
                rollbar.report_message(
                    'Error: An error ocurred updating indicators of '
                    'the project {project} in dynamo'.format(project=project),
                    'error')
        except ClientError:
            rollbar.report_message(
                'Error: An error ocurred updating '
                'indicators of the project {project}'.format(project=project),
                'error')


def reset_expired_accepted_findings():
    """ Update treatment if acceptance date expires """
    rollbar.report_message('Warning: Function to update treatment if'
                           'acceptance date expires is running', 'warning')
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    projects = project_domain.get_active_projects()
    for project in projects:
        findings = finding_domain.get_findings(
            finding_domain.filter_deleted_findings(
                project_domain.list_findings(project)))
        for finding in findings:
            finding_id = finding.get('findingId')
            historic_treatment = finding.get('historicTreatment', [{}])
            is_accepted_expired = historic_treatment[-1].get('acceptance_date', today) < today
            is_undefined_accepted_expired = (
                historic_treatment[-1].get('treatment') == 'ACCEPTED_UNDEFINED' and
                historic_treatment[-1].get('acceptance_status') == 'SUBMITTED' and
                datetime.strptime(historic_treatment[-1].get('date'), "%Y-%m-%d %H:%M:%S")
                + timedelta(days=5) <= datetime.strptime(today, "%Y-%m-%d %H:%M:%S"))
            if is_accepted_expired or is_undefined_accepted_expired:
                updated_values = {'treatment': 'NEW'}
                finding_domain.update_treatment(finding_id, updated_values, '')
                util.invalidate_cache(finding_id)
