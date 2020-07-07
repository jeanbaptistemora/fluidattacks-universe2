""" Asynchronous task execution scheduler for FLUIDIntegrates """


import asyncio
import logging
import logging.config
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Union, cast

from more_itertools import chunked
import rollbar
from botocore.exceptions import ClientError
from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings

from backend import mailer, util
from backend.dal import (
    finding as finding_dal,
    project as project_dal,
    vulnerability as vuln_dal
)
from backend.domain import (
    finding as finding_domain,
    project as project_domain,
    user as user_domain,
    vulnerability as vuln_domain,
    event as event_domain,
    tag as tag_domain
)
from backend.typing import (
    Event as EventType,
    Finding as FindingType
)
from __init__ import (
    BASE_URL,
    FI_TEST_PROJECTS,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_PROJECTS,
    FI_MAIL_REVIEWERS
)

logging.config.dictConfig(settings.LOGGING)  # type: ignore
LOGGER = logging.getLogger(__name__)


def is_not_a_fluidattacks_email(email: str) -> bool:
    return 'fluidattacks.com' not in email


def remove_fluid_from_recipients(emails: List[str]) -> List[str]:
    new_email_list = list(filter(is_not_a_fluidattacks_email, emails))
    return new_email_list


def is_a_unsolved_event(event: EventType) -> bool:
    return cast(
        List[Dict[str, str]],
        event.get('historic_state', [{}])
    )[-1].get('state', '') == 'CREATED'


async def get_unsolved_events(project: str) -> List[EventType]:
    events = await sync_to_async(project_domain.list_events)(project)
    event_list = await asyncio.gather(*[
        asyncio.create_task(
            event_domain.get_event(
                event
            )
        )
        for event in events
    ])
    unsolved_events = list(filter(is_a_unsolved_event, event_list))
    return unsolved_events


def extract_info_from_event_dict(event_dict: EventType) -> EventType:
    event_dict = {
        'type': event_dict['event_type'],
        'details': event_dict['detail']
    }
    return event_dict


async def send_unsolved_events_email(project: str):
    mail_to = []
    events_info_for_email = []
    project_info = await sync_to_async(project_domain.get_project_info)(
        project
    )
    historic_configuration = project_info.get(
        'historic_configuration', [{}]
    )
    if (project_info and
            historic_configuration[-1].get('type', '') == 'continuous'):
        mail_to = await sync_to_async(get_external_recipients)(project)
        mail_to.append(FI_MAIL_CONTINUOUS)
        mail_to.append(FI_MAIL_PROJECTS)
        unsolved_events = await get_unsolved_events(project)
        events_info_for_email = [
            extract_info_from_event_dict(x)
            for x in unsolved_events
        ]
    context_event: Dict[str, Union[str, int]] = {
        'project': project.capitalize(),
        'events_len': int(len(events_info_for_email)),
        'event_url': f'{BASE_URL}/groups/{project}/events'
    }
    if context_event['events_len'] and mail_to:
        mailer.send_mail_unsolved_events(mail_to, context_event)


def get_external_recipients(project: str) -> List[str]:
    recipients = cast(List[str], project_domain.get_managers(project))
    return remove_fluid_from_recipients(recipients)


def get_finding_url(finding: Dict[str, str]) -> str:
    url = (
        f'{BASE_URL}/groups/{finding["project_name"]}/'
        f'{finding["finding_id"]}/description'
    )
    return url


def get_status_vulns_by_time_range(
        vulns: List[Dict[str, FindingType]],
        first_day: str,
        last_day: str,
        findings_released: List[Dict[str, FindingType]]) -> Dict[str, int]:
    """Get total closed and found vulnerabilities by time range"""
    resp: Dict[str, int] = defaultdict(int)
    for vuln in vulns:
        historic_states = cast(List[Dict[str, str]], vuln['historic_state'])
        last_state = vuln_domain.get_last_approved_state(vuln)

        if last_state and first_day <= last_state['date'] <= last_day:
            if last_state['state'] == 'closed':
                resp['closed'] += 1
            elif last_state['state'] == 'DELETED':
                resp['found'] -= 1
        if first_day <= historic_states[0]['date'] <= last_day:
            resp['found'] += 1
    resp['accepted'] = get_accepted_vulns(
        findings_released, vulns, first_day, last_day)
    return resp


def create_weekly_date(first_date: str) -> str:
    """Create format weekly date"""
    first_date_ = datetime.strptime(first_date, '%Y-%m-%d %H:%M:%S')
    begin = first_date_ - timedelta(days=(first_date_.isoweekday() - 1) % 7)
    end = begin + timedelta(days=6)
    if begin.year != end.year:
        date = '{0:%b} {0.day}, {0.year} - {1:%b} {1.day}, {1.year}'
    elif begin.month != end.month:
        date = '{0:%b} {0.day} - {1:%b} {1.day}, {1.year}'
    else:
        date = '{0:%b} {0.day} - {1.day}, {1.year}'
    return date.format(begin, end)


def get_accepted_vulns(
        findings_released: List[Dict[str, FindingType]],
        vulns: List[Dict[str, FindingType]],
        first_day: str, last_day: str) -> int:
    """Get all vulnerabilities accepted by time range"""
    accepted = 0
    for finding in findings_released:
        historic_treatment = cast(
            List[Dict[str, str]],
            finding.get('historic_treatment', [{}])
        )
        if historic_treatment[-1].get('treatment') == 'ACCEPTED':
            for vuln in vulns:
                accepted += get_by_time_range(
                    finding, vuln, first_day, last_day
                )
    return accepted


def get_by_time_range(
        finding: Dict[str, FindingType],
        vuln: Dict[str, FindingType],
        first_day: str,
        last_day: str) -> int:
    """Accepted vulnerability of finding."""
    count = 0
    if finding['finding_id'] == vuln['finding_id']:

        history = vuln_domain.get_last_approved_state(
            cast(Dict[str, finding_dal.FindingType], vuln))
        if (history and
                first_day <= history['date'] <= last_day and
                history['state'] == 'open'):
            count += 1
        else:
            # date of vulnerabilities outside of time_range or state not open
            pass
    else:
        # vulnerabilities is from finding
        pass
    return count


def create_register_by_week(project: str) -> \
        List[List[Dict[str, Union[str, int]]]]:
    """Create weekly vulnerabilities registry by project"""
    accepted = 0
    closed = 0
    found = 0
    all_registers = OrderedDict()
    findings_released = project_domain.get_released_findings(project)
    vulns = get_all_vulns_by_project(findings_released)
    if vulns:
        first_day, last_day = get_first_week_dates(vulns)
        first_day_last_week = get_date_last_vulns(vulns)
        while first_day <= first_day_last_week:
            result_vulns_by_week = get_status_vulns_by_time_range(
                vulns, first_day,
                last_day,
                findings_released)
            accepted += result_vulns_by_week.get('accepted', 0)
            closed += result_vulns_by_week.get('closed', 0)
            found += result_vulns_by_week.get('found', 0)
            if any(status_vuln
                   for status_vuln in list(result_vulns_by_week.values())):
                week_dates = create_weekly_date(first_day)
                all_registers[week_dates] = {
                    'found': found,
                    'closed': closed,
                    'accepted': accepted,
                    'assumed_closed': accepted + closed,
                    'opened': found - closed - accepted,
                }
            first_day = str(
                datetime.strptime(first_day, '%Y-%m-%d %H:%M:%S') +
                timedelta(days=7)
            )
            last_day = str(
                datetime.strptime(last_day, '%Y-%m-%d %H:%M:%S') +
                timedelta(days=7)
            )
    return create_data_format_chart(all_registers)


def create_data_format_chart(
        all_registers: Dict[str, Dict[str, int]]) -> \
        List[List[Dict[str, Union[str, int]]]]:
    result_data = []
    plot_points: Dict[str, List[Dict[str, Union[str, int]]]] = {
        'found': [],
        'closed': [],
        'accepted': [],
        'assumed_closed': [],
        'opened': []
    }
    for week, dict_status in list(all_registers.items()):
        for status in plot_points:
            plot_points[status].append({'x': week, 'y': dict_status[status]})
    for status in plot_points:
        result_data.append(plot_points[status])
    return result_data


def get_all_vulns_by_project(
        findings_released: List[Dict[str, FindingType]]) -> \
        List[Dict[str, FindingType]]:
    """Get all vulnerabilities by project"""
    vulns: List[Dict[str, FindingType]] = []
    for finding in findings_released:
        vulns += vuln_dal.get_vulnerabilities(str(
            finding.get('finding_id', '')
        ))
    return vulns


def get_first_week_dates(vulns: List[Dict[str, FindingType]]) -> \
        Tuple[str, str]:
    """Get first week vulnerabilities"""
    first_date = min([
        datetime.strptime(
            cast(
                List[Dict[str, str]],
                vuln['historic_state']
            )[0]['date'],
            '%Y-%m-%d %H:%M:%S'
        )
        for vuln in vulns
    ])
    day_week = first_date.weekday()
    first_day_delta = first_date - timedelta(days=day_week)
    first_day = datetime.combine(first_day_delta, datetime.min.time())
    last_day_delta = first_day + timedelta(days=6)
    last_day = datetime.combine(
        last_day_delta,
        datetime.max.time().replace(microsecond=0)
    )
    return str(first_day), str(last_day)


def get_date_last_vulns(vulns: List[Dict[str, FindingType]]) -> str:
    """Get date of the last vulnerabilities"""
    last_date = max([
        datetime.strptime(
            cast(
                List[Dict[str, str]],
                vuln['historic_state']
            )[-1]['date'],
            '%Y-%m-%d %H:%M:%S'
        )
        for vuln in vulns
    ])
    day_week = last_date.weekday()
    first_day = str(last_date - timedelta(days=day_week))
    return first_day


@async_to_sync
async def get_new_vulnerabilities():
    """Summary mail send with the findings of a project."""
    rollbar.report_message(
        'Warning: Function to get new vulnerabilities is running',
        'warning'
    )
    projects = await sync_to_async(project_domain.get_active_projects)()
    fin_attrs = 'finding_id, historic_treatment, project_name, finding'
    released_findings = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(project_domain.get_released_findings)(
                project, fin_attrs
            )
        )
        for project in projects
    ])
    finding_urls = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(get_finding_url)(
                act_finding
            )
        )
        for finding_requests in released_findings
        for act_finding in finding_requests
    ])
    msj_finding_pendings = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(create_msj_finding_pending)(
                act_finding
            )
        )
        for finding_requests in released_findings
        for act_finding in finding_requests
    ])
    deltas = await asyncio.gather(*[
        asyncio.create_task(
            calculate_vulnerabilities(
                act_finding
            )
        )
        for finding_requests in released_findings
        for act_finding in finding_requests
    ])
    for project in projects:
        context = {'updated_findings': list(), 'no_treatment_findings': list()}
        try:
            finding_requests = released_findings.pop(0)
            for act_finding in finding_requests:
                finding_url = finding_urls.pop(0)
                msj_finding_pending = msj_finding_pendings.pop(0)
                delta = deltas.pop(0)
                finding_text = format_vulnerabilities(delta, act_finding)
                if msj_finding_pending:
                    context['no_treatment_findings'].append({
                        'finding_name': msj_finding_pending,
                        'finding_url': finding_url
                    })
                if finding_text:
                    context['updated_findings'].append({
                        'finding_name': finding_text,
                        'finding_url': finding_url
                    })
                context['project'] = str.upper(str(
                    act_finding['project_name']
                ))
                context['project_url'] = (
                    f'{BASE_URL}/groups/'
                    f'{act_finding["project_name"]}/indicators'
                )
        except (TypeError, KeyError):
            rollbar.report_message(
                ('Error: An error ocurred getting new vulnerabilities '
                 'notification email'),
                'error', payload_data=locals())
            raise
        if context['updated_findings']:
            mail_to = await project_domain.get_users_to_notify(project)
            await sync_to_async(mailer.send_mail_new_vulnerabilities)(
                mail_to, context
            )


async def calculate_vulnerabilities(act_finding: Dict[str, str]) -> int:
    vulns = await sync_to_async(vuln_dal.get_vulnerabilities)(
        act_finding['finding_id']
    )
    all_tracking = await finding_domain.get_tracking_vulnerabilities(vulns)
    delta_total = 0
    if len(all_tracking) > 1:
        if ((datetime.strptime(str(all_tracking[-1]['date']), "%Y-%m-%d")) >
                (datetime.now() - timedelta(days=8))):
            delta_open = abs(
                all_tracking[-1]['open'] - all_tracking[-2]['open']
            )
            delta_closed = abs(
                all_tracking[-1]['closed'] - all_tracking[-2]['closed']
            )
            delta_total = delta_open - delta_closed
    elif (len(all_tracking) == 1 and
            (datetime.strptime(str(all_tracking[-1]['date']), "%Y-%m-%d")) >
            (datetime.now() - timedelta(days=8))):
        delta_open = all_tracking[-1]['open']
        delta_closed = all_tracking[-1]['closed']
        delta_total = delta_open - delta_closed
    return delta_total


def format_vulnerabilities(delta: int, act_finding: Dict[str, str]) -> str:
    """Format vulnerabities changes in findings."""
    if delta > 0:
        finding_text = f'{act_finding["finding"]} (+{delta})'
    elif delta < 0:
        finding_text = f'{act_finding["finding"]} ({delta})'
    else:
        finding_text = ''
        message = (
            f'Finding {act_finding["finding_id"]} of project '
            f'{act_finding["project_name"]} has no changes during the week'
        )
        LOGGER.info(message)
    return finding_text


def create_msj_finding_pending(act_finding: Dict[str, FindingType]) -> str:
    """Validate if a finding has treatment."""
    historic_treatment = cast(
        List[Dict[str, str]],
        act_finding.get('historic_treatment', [{}])
    )
    open_vulns = [
        vuln
        for vuln in vuln_domain.get_vulnerabilities(
            str(act_finding['finding_id'])
        )
        if vuln['current_state'] == 'open'
    ]
    if historic_treatment[-1].get('treatment', 'NEW') == 'NEW' and open_vulns:
        days = finding_domain.get_age_finding(act_finding)
        finding_name = f'{act_finding["finding"]} -{days} day(s)-'
        result = finding_name
    else:
        result = ''
    return result


@async_to_sync
async def get_remediated_findings():
    """Summary mail send with findings that have not been verified yet."""
    rollbar.report_message(
        'Warning: Function to get remediated findings is running',
        'warning'
    )
    active_projects = await sync_to_async(project_domain.get_active_projects)()
    findings = []
    pending_verification_findings = await asyncio.gather(*[
        asyncio.create_task(
            project_dal.get_pending_verification_findings(
                project
            )
        )
        for project in active_projects
    ])
    for project_findings in pending_verification_findings:
        findings += project_findings

    if findings:
        try:
            mail_to = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
            context = {'findings': list()}
            for finding in findings:
                context['findings'].append({
                    'finding_name': finding['finding'],
                    'finding_url': (
                        f'{BASE_URL}/groups/'
                        f'{str.lower(str(finding["project_name"]))}/'
                        f'{finding["finding_id"]}/description'
                    ),
                    'project': str.upper(str(finding['project_name']))})
            context['total'] = len(findings)
            await sync_to_async(mailer.send_mail_new_remediated)(
                mail_to, context
            )
        except (TypeError, KeyError) as ex:
            rollbar.report_message(
                'Warning: An error ocurred getting data for remediated email',
                'warning',
                extra_data=ex,
                payload_data=locals()
            )
    else:
        LOGGER.info('There are no findings to verificate')


@async_to_sync
async def weekly_report():
    """Save weekly report in dynamo."""
    rollbar.report_message(
        'Warning: Function to do weekly report in DynamoDB is running',
        'warning'
    )
    init_date = (datetime.today() - timedelta(days=7)).date().strftime(
        '%Y-%m-%d'
    )
    final_date = (datetime.today() - timedelta(days=1)).date().strftime(
        '%Y-%m-%d'
    )
    all_companies = await sync_to_async(user_domain.get_all_companies)()
    all_users = await asyncio.gather(*[
        asyncio.create_task(
            all_users_formatted(x)
        )
        for x in all_companies
    ])
    registered_users = await sync_to_async(user_domain.get_all_users_report)(
        'FLUID', final_date
    )
    logged_users = await sync_to_async(user_domain.logging_users_report)(
        'FLUID', init_date, final_date
    )
    await sync_to_async(project_dal.get_weekly_report)(
        init_date,
        final_date,
        registered_users,
        logged_users,
        all_users
    )


async def all_users_formatted(company: str) -> Dict[str, int]:
    """Format total users by company."""
    total_users = await sync_to_async(user_domain.get_all_users)(company)
    all_users_by_company = {company: total_users}
    return all_users_by_company


@async_to_sync
async def get_new_releases():
    """Summary mail send with findings that have not been released yet."""
    rollbar.report_message(
        'Warning: Function to get new releases is running',
        'warning'
    )
    test_projects = FI_TEST_PROJECTS.split(',')
    projects = await sync_to_async(project_domain.get_active_projects)()
    email_context = defaultdict(list)
    cont = 0
    list_drafts = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(project_domain.list_drafts)(
                project
            )
        )
        for project in projects
        if project not in test_projects
    ])
    project_drafts = await asyncio.gather(*[
        asyncio.create_task(
            finding_domain.get_findings_async(
                drafts
            )
        )
        for drafts in list_drafts
    ])
    for project in projects:
        if project not in test_projects:
            try:
                finding_requests = project_drafts.pop(0)
                for finding in finding_requests:
                    if 'releaseDate' not in finding:
                        submission = finding.get('historicState')
                        status = submission[-1].get('state')
                        category = (
                            'unsubmitted'
                            if status in ('CREATED', 'REJECTED')
                            else 'unreleased'
                        )
                        email_context[category].append({
                            'finding_name': finding.get('finding'),
                            'finding_url': (
                                f'{BASE_URL}/groups/{project}/drafts/'
                                f'{finding.get("findingId")}/description'
                            ),
                            'project': project.upper()
                        })
                        cont += 1
            except (TypeError, KeyError):
                rollbar.report_message(
                    ('Warning: An error ocurred getting '
                     'data for new drafts email'),
                    'warning'
                )
        else:
            # ignore test projects
            pass
    if cont > 0:
        email_context['total_unreleased'] = len(email_context['unreleased'])
        email_context['total_unsubmitted'] = len(email_context['unsubmitted'])
        approvers = FI_MAIL_REVIEWERS.split(',')
        mail_to = [FI_MAIL_PROJECTS]
        mail_to.extend(approvers)
        await sync_to_async(mailer.send_mail_new_releases)(
            mail_to, email_context
        )
    else:
        rollbar.report_message(
            'Warning: There are no new drafts',
            'warning'
        )


@async_to_sync
async def send_unsolved_to_all() -> List[bool]:
    """Send email with unsolved events to all projects """
    rollbar.report_message(
        'Warning: Function to send email with unsolved events is running',
        'warning'
    )
    projects = await sync_to_async(project_domain.get_active_projects)()
    return await asyncio.gather(*[
        send_unsolved_events_email(project)
        for project in projects
    ])


async def get_project_indicators(project: str) -> Dict[str, object]:
    findings = await sync_to_async(project_domain.get_released_findings)(
        project, 'finding_id, historic_treatment, cvss_temporal'
    )
    last_closing_vuln_days, last_closing_vuln = (
        await project_domain.get_last_closing_vuln_info(findings)
    )
    max_open_severity, max_open_severity_finding = (
        await project_domain.get_max_open_severity(findings)
    )
    indicators = {
        'closed_vulnerabilities': (
            await project_domain.get_closed_vulnerabilities(project)
        ),
        'last_closing_date': last_closing_vuln_days,
        'last_closing_vuln_finding': last_closing_vuln.get('finding_id', ''),
        'mean_remediate': await project_domain.get_mean_remediate(findings),
        'mean_remediate_critical_severity': (
            await project_domain.get_mean_remediate_severity(project, 9, 10)
        ),
        'mean_remediate_high_severity': (
            await project_domain.get_mean_remediate_severity(project, 7, 8.9)
        ),
        'mean_remediate_low_severity': (
            await project_domain.get_mean_remediate_severity(project, 0.1, 3.9)
        ),
        'mean_remediate_medium_severity': (
            await project_domain.get_mean_remediate_severity(project, 4, 6.9)
        ),
        'max_open_severity': max_open_severity,
        'max_open_severity_finding': max_open_severity_finding.get(
            'finding_id', ''
        ),
        'open_findings': await project_domain.get_open_finding(project),
        'open_vulnerabilities': (
            await project_domain.get_open_vulnerabilities(project)
        ),
        'total_treatment': await project_domain.get_total_treatment(findings),
        'remediated_over_time': (
            await sync_to_async(create_register_by_week)(project)
        )
    }
    return indicators


async def update_group_indicators(group_name: str) -> None:
    rollbar.report_message(
        f'Info: Updating indicators in {group_name}',
        'info'
    )
    indicators = await get_project_indicators(group_name)
    try:
        response = await sync_to_async(project_dal.update)(
            group_name, indicators
        )
        if response:
            util.invalidate_cache(group_name)
            rollbar.report_message(
                f'Info: Updated indicators in {group_name}',
                'info'
            )
        else:
            rollbar.report_message(
                ('Error: An error ocurred updating indicators of '
                 f'the group {group_name} in the database'),
                'error'
            )
    except ClientError:
        rollbar.report_message(
            ('Error: An error ocurred updating '
             f'indicators of the group {group_name}'),
            'error'
        )


@async_to_sync
async def update_indicators():
    """Update in dynamo indicators."""
    rollbar.report_message(
        'Warning: Function to update indicators in DynamoDB is running',
        'warning'
    )
    groups = await sync_to_async(project_domain.get_active_projects)()
    # number of groups that can be updated at a time
    groups_chunks = chunked(groups, 40)
    for grps_chunk in groups_chunks:
        await asyncio.gather(*[
            asyncio.create_task(
                update_group_indicators(group_name)
            )
            for group_name in grps_chunk
        ])


async def reset_group_expired_accepted_findings(
        group_name: str, today: str) -> None:
    rollbar.report_message(
        f'Info: Resetting expired accepted findings in {group_name}',
        'info'
    )
    list_findings = await sync_to_async(project_domain.list_findings)(
        group_name
    )
    findings = await finding_domain.get_findings_async(
        list_findings
    )
    for finding in findings:
        finding_id = cast(str, finding.get('findingId'))
        historic_treatment = cast(
            List[Dict[str, str]],
            finding.get('historicTreatment', [{}])
        )
        is_accepted_expired = (
            historic_treatment[-1].get('acceptance_date', today) < today
        )
        is_undefined_accepted_expired = (
            (historic_treatment[-1].get('treatment') ==
                'ACCEPTED_UNDEFINED') and
            (historic_treatment[-1].get('acceptance_status') ==
                'SUBMITTED') and
            (
                datetime.strptime(
                    historic_treatment[-1].get('date', '0001-01-01 00:00:00'),
                    "%Y-%m-%d %H:%M:%S"
                ) + timedelta(days=5)
            ) <= datetime.strptime(today, "%Y-%m-%d %H:%M:%S")
        )
        if is_accepted_expired or is_undefined_accepted_expired:
            updated_values = {'treatment': 'NEW'}
            await finding_domain.update_treatment(
                finding_id, updated_values, ''
            )
            util.invalidate_cache(finding_id)


@async_to_sync
async def reset_expired_accepted_findings():
    """ Update treatment if acceptance date expires """
    rollbar.report_message(
        ('Warning: Function to update treatment if'
         'acceptance date expires is running'),
        'warning'
    )
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    groups = await sync_to_async(project_domain.get_active_projects)()
    # number of groups that can be updated at a time
    groups_chunks = chunked(groups, 40)
    for grps_chunk in groups_chunks:
        await asyncio.gather(*[
            asyncio.create_task(
                reset_group_expired_accepted_findings(group_name, today)
            )
            for group_name in grps_chunk
        ])


@async_to_sync
async def delete_pending_projects():
    """ Delete pending to delete projects """
    rollbar.report_message(
        ('Warning: Function to delete projects if '
         'deletion_date expires is running'),
        'warning'
    )
    today = datetime.now()
    projects = await sync_to_async(project_domain.get_pending_to_delete)()
    remove_project_tasks = []
    for project in projects:
        historic_deletion = project.get('historic_deletion', [{}])
        last_state = historic_deletion[-1]
        deletion_date = last_state.get(
            'deletion_date', today.strftime('%Y-%m-%d %H:%M:%S')
        )
        deletion_date = datetime.strptime(deletion_date, '%Y-%m-%d %H:%M:%S')
        if deletion_date < today:
            task = asyncio.create_task(
                sync_to_async(project_domain.remove_project)(
                    project.get('project_name')
                )
            )
            remove_project_tasks.append(task)
            util.invalidate_cache(project.get('project_name'))
    await asyncio.gather(*remove_project_tasks)


@async_to_sync
async def update_tags_indicators():
    """Update tag indicators in dynamo."""
    rollbar.report_message(
        ('Warning: Function to update tag'
         'indicators in DynamoDB is running'),
        'warning'
    )
    projects = await sync_to_async(project_domain.get_active_projects)()
    projects = await asyncio.gather(*[
        asyncio.create_task(
            sync_to_async(project_domain.get_attributes)(
                project, ['companies', 'project_name', 'tag']
            )
        )
        for project in projects
    ])
    all_organization = {
        organization.lower()
        for project in projects
        for organization in project.get('companies', [])
    }
    for organization in all_organization:
        try:
            await tag_domain.update_organization_indicators(
                organization, projects
            )
        except ClientError:
            rollbar.report_message(
                ('Error: An error ocurred updating tag '
                 f'indicators of organizaion {organization}'),
                'error'
            )
