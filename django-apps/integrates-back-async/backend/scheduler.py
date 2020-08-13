""" Asynchronous task execution scheduler for FLUIDIntegrates """


import asyncio
import logging
import logging.config
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Tuple, Union, cast

from more_itertools import chunked
from botocore.exceptions import ClientError
from asgiref.sync import async_to_sync, sync_to_async

from backend import mailer, util
from backend.dal import (
    project as project_dal,
    tag as tag_dal
)
from backend.domain import (
    finding as finding_domain,
    organization as org_domain,
    project as project_domain,
    tag as tag_domain,
    vulnerability as vuln_domain,
    event as event_domain
)
from backend.typing import (
    Event as EventType,
    Finding as FindingType,
    Historic as HistoricType,
    Project as ProjectType
)
from backend.utils import aio
from fluidintegrates.settings import (
    LOGGING,
    NOEXTRA
)
from __init__ import (
    BASE_URL,
    FI_TEST_PROJECTS,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_PROJECTS,
    FI_MAIL_REVIEWERS
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger('console')


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
    events = await project_domain.list_events(project)
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
        'type': event_dict.get('event_type', ''),
        'details': event_dict.get('detail', '')
    }
    return event_dict


async def send_unsolved_events_email(project: str) -> None:
    mail_to = []
    events_info_for_email = []
    project_info = await project_domain.get_attributes(
        project, ['historic_configuration']
    )
    historic_configuration = cast(
        HistoricType,
        project_info.get('historic_configuration', [{}])
    )
    if (project_info and
            historic_configuration[-1].get('type', '') == 'continuous'):
        mail_to = await get_external_recipients(project)
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


async def get_external_recipients(project: str) -> List[str]:
    recipients = await project_domain.get_managers(project)
    return remove_fluid_from_recipients(recipients)


def get_finding_url(finding: Dict[str, FindingType]) -> str:
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
            elif last_state['state'] == 'open' and len(historic_states) > 1:
                if historic_states[-2]['state'] == 'closed':
                    resp['found'] += 1
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

        history = vuln_domain.get_last_approved_state(vuln)
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


async def create_register_by_week(
        project: str) -> List[List[Dict[str, Union[str, int]]]]:
    """Create weekly vulnerabilities registry by project"""
    accepted = 0
    closed = 0
    found = 0
    all_registers = OrderedDict()
    findings_released = await project_domain.get_released_findings(project)
    vulns = await vuln_domain.list_vulnerabilities_async(
        [str(finding['finding_id']) for finding in findings_released]
    )
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
    all_registers: Dict[str, Dict[str, int]]
) -> List[List[Dict[str, Union[str, int]]]]:
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


def get_first_week_dates(
        vulns: List[Dict[str, FindingType]]) -> Tuple[str, str]:
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


async def get_group_new_vulnerabilities(group_name: str) -> None:
    msg = 'Info: Getting new vulnerabilities'
    LOGGER.info(msg, extra={'extra': locals()})
    fin_attrs = 'finding_id, historic_treatment, project_name, finding'
    context: Dict[str, Union[str, List[Dict[str, str]]]] = {
        'updated_findings': list(),
        'no_treatment_findings': list()
    }
    try:
        finding_requests = await project_domain.get_released_findings(
            group_name,
            fin_attrs
        )
        for act_finding in finding_requests:
            finding_url = get_finding_url(act_finding)
            msj_finding_pending = await create_msj_finding_pending(
                act_finding
            )
            delta = await calculate_vulnerabilities(
                act_finding
            )
            finding_text = format_vulnerabilities(delta, act_finding)
            if msj_finding_pending:
                cast(
                    List[Dict[str, str]],
                    context['no_treatment_findings']
                ).append({
                    'finding_name': msj_finding_pending,
                    'finding_url': finding_url
                })
            if finding_text:
                cast(
                    List[Dict[str, str]],
                    context['updated_findings']
                ).append({
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
    except (TypeError, KeyError) as ex:
        LOGGER.exception(ex, extra={'extra': {'group_name': group_name}})
        raise
    if context['updated_findings']:
        mail_to = await project_domain.get_users_to_notify(group_name)
        await aio.ensure_io_bound(
            mailer.send_mail_new_vulnerabilities,
            mail_to,
            context
        )


@async_to_sync  # type: ignore
async def get_new_vulnerabilities() -> None:
    """Summary mail send with the findings of a project."""
    msg = '[scheduler]: get_new_vulnerabilities is running'
    LOGGER.warning(msg, **NOEXTRA)
    groups = await project_domain.get_active_projects()
    await aio.materialize(map(get_group_new_vulnerabilities, groups))


def calculate_tag_indicators(
        tag: str,
        tags_dict: Dict[str, List[ProjectType]],
        indicator_list: List[str]) -> Dict[str, Union[Decimal, List[str]]]:
    tag_info: Dict[str, Union[Decimal, List[str]]] = {}
    for indicator in indicator_list:
        if 'max' in indicator:
            tag_info[indicator] = Decimal(
                max([
                    cast(Decimal, group.get(indicator, Decimal('0.0')))
                    for group in tags_dict[tag]
                ])
            ).quantize(Decimal('0.1'))
        elif 'mean' in indicator:
            tag_info[indicator] = Decimal(
                sum([
                    cast(Decimal, group.get(indicator, Decimal('0.0')))
                    for group in tags_dict[tag]
                ]) / Decimal(len(tags_dict[tag]))
            ).quantize(Decimal('0.1'))
        else:
            tag_info[indicator] = Decimal(
                min([
                    cast(Decimal, group.get(indicator, Decimal('inf')))
                    for group in tags_dict[tag]
                ])
            ).quantize(Decimal('0.1'))
        tag_info['projects'] = [
            str(group['name']) for group in tags_dict[tag]
        ]
    return tag_info


async def calculate_vulnerabilities(
        act_finding: Dict[str, FindingType]) -> int:
    vulns = await vuln_domain.list_vulnerabilities_async(
        [str(act_finding['finding_id'])]
    )
    all_tracking = await finding_domain.get_tracking_vulnerabilities(vulns)
    delta_total = 0
    # Remove last duplicate cycles who are added by approving an open vuln
    if len(all_tracking) > 1:
        last_cycle_open = all_tracking[-1]['open']
        last_cycle_close = all_tracking[-1]['closed']
        for cycle in all_tracking[::-1][1:]:
            if (last_cycle_open == cycle['open']
                    and last_cycle_close == cycle['closed']):
                all_tracking.pop()
                continue
            break
    if len(all_tracking) > 1:
        if ((datetime.strptime(str(all_tracking[-1]['date']), "%Y-%m-%d")) >
                (datetime.now() - timedelta(days=8))):
            open_2 = cast(int, all_tracking[-1]['open'])
            open_1 = cast(int, all_tracking[-2]['open'])
            closed_2 = cast(int, all_tracking[-1]['closed'])
            closed_1 = cast(int, all_tracking[-2]['closed'])
            delta_open = abs(open_2 - open_1)
            delta_closed = abs(closed_2 - closed_1)
            delta_total = delta_open - delta_closed
    elif (len(all_tracking) == 1 and
            (datetime.strptime(str(all_tracking[-1]['date']), "%Y-%m-%d")) >
            (datetime.now() - timedelta(days=8))):
        delta_open = cast(int, all_tracking[-1]['open'])
        delta_closed = cast(int, all_tracking[-1]['closed'])
        delta_total = delta_open - delta_closed
    return delta_total


def format_vulnerabilities(
        delta: int,
        act_finding: Dict[str, FindingType]) -> str:
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
        LOGGER.info(message, **NOEXTRA)
    return finding_text


async def create_msj_finding_pending(
        act_finding: Dict[str, FindingType]) -> str:
    """Validate if a finding has treatment."""
    historic_treatment = cast(
        List[Dict[str, str]],
        act_finding.get('historic_treatment', [{}])
    )
    open_vulns = [
        vuln
        for vuln in await vuln_domain.list_vulnerabilities_async(
            [str(act_finding['finding_id'])]
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


@async_to_sync  # type: ignore
async def get_remediated_findings() -> None:
    """Summary mail send with findings that have not been verified yet."""
    msg = '[scheduler]: get_remediated_findings is running'
    LOGGER.warning(msg, extra=dict(extra=None))
    active_projects = await project_domain.get_active_projects()
    findings = []
    pending_verification_findings = await asyncio.gather(*[
        asyncio.create_task(
            project_domain.get_pending_verification_findings(
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
            context = {'findings': list(), 'total': 0}
            for finding in findings:
                cast(
                    List[Dict[str, str]],
                    context['findings']
                ).append({
                    'finding_name': finding['finding'],
                    'finding_url': (
                        f'{BASE_URL}/groups/'
                        f'{str.lower(str(finding["project_name"]))}/'
                        f'{finding["finding_id"]}/description'
                    ),
                    'project': str.upper(str(finding['project_name']))
                })
            context['total'] = len(findings)
            await sync_to_async(mailer.send_mail_new_remediated)(
                mail_to, context
            )
        except (TypeError, KeyError) as ex:
            LOGGER.exception(ex, extra={'extra': locals()})
    else:
        msg = '[scheduler]: There are no findings to verify'
        LOGGER.warning(msg, extra=dict(extra=None))


@async_to_sync  # type: ignore
async def get_new_releases() -> None:  # pylint: disable=too-many-locals
    """Summary mail send with findings that have not been released yet."""
    msg = '[scheduler]: get_new_releases is running'
    LOGGER.warning(msg, extra=dict(extra=None))
    test_projects = FI_TEST_PROJECTS.split(',')
    projects = await project_domain.get_active_projects()
    email_context: Dict[str, Union[List[Dict[str, str]], int]] = (
        defaultdict(list)
    )
    cont = 0
    projects = [
        project
        for project in projects
        if project not in test_projects
    ]
    list_drafts = await project_domain.list_drafts(projects)
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
                        cast(
                            List[Dict[str, str]],
                            email_context[category]
                        ).append({
                            'finding_name': finding.get('finding'),
                            'finding_url': (
                                f'{BASE_URL}/groups/{project}/drafts/'
                                f'{finding.get("findingId")}/description'
                            ),
                            'project': project.upper()
                        })
                        cont += 1
            except (TypeError, KeyError) as ex:
                LOGGER.exception(ex, extra={'extra': locals()})
        else:
            # ignore test projects
            pass
    if cont > 0:
        email_context['total_unreleased'] = len(
            cast(List[Dict[str, str]], email_context['unreleased'])
        )
        email_context['total_unsubmitted'] = len(
            cast(List[Dict[str, str]], email_context['unsubmitted'])
        )
        approvers = FI_MAIL_REVIEWERS.split(',')
        mail_to = [FI_MAIL_PROJECTS]
        mail_to.extend(approvers)
        await sync_to_async(mailer.send_mail_new_releases)(
            mail_to, email_context
        )
    else:
        msg = '[scheduler]: There are no new drafts'
        LOGGER.warning(msg, extra=dict(extra=None))


@async_to_sync  # type: ignore
async def send_unsolved_to_all() -> None:
    """Send email with unsolved events to all projects """
    msg = '[scheduler]: send_unsolved_to_all is running'
    LOGGER.warning(msg, extra=dict(extra=None))
    projects = await project_domain.get_active_projects()
    await asyncio.gather(*[
        asyncio.create_task(
            send_unsolved_events_email(project)
        )
        for project in projects
    ])


async def get_project_indicators(project: str) -> Dict[str, object]:
    findings = await project_domain.get_released_findings(
        project,
        'finding_id, historic_treatment, cvss_temporal'
    )
    last_closing_vuln_days, last_closing_vuln = (
        await project_domain.get_last_closing_vuln_info(findings)
    )
    max_open_severity, max_open_severity_finding = (
        await project_domain.get_max_open_severity(findings)
    )
    remediated_over_time = await create_register_by_week(
        project
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
        'remediated_over_time': remediated_over_time
    }
    return indicators


async def update_group_indicators(group_name: str) -> None:
    payload_data = {
        'group_name': group_name
    }
    msg = 'Info: Updating indicators'
    LOGGER.info(msg, extra={'extra': payload_data})
    indicators = await get_project_indicators(group_name)
    try:
        response = await project_dal.update(
            group_name,
            indicators
        )
        if response:
            await util.invalidate_cache(group_name)
            msg = 'Info: Updated indicators'
            LOGGER.info(msg, extra={'extra': payload_data})
        else:
            msg = 'Error: An error ocurred updating indicators in the database'
            LOGGER.info(msg, extra={'extra': payload_data})
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': payload_data})


@async_to_sync  # type: ignore
async def update_indicators() -> None:
    """Update in dynamo indicators."""
    msg = '[scheduler]: update_indicators is running'
    LOGGER.warning(msg, **NOEXTRA)
    groups = await project_domain.get_active_projects()
    aio.materialize(map(update_group_indicators, groups), 10)


async def update_organization_indicators(
        organization_name: str,
        groups: List[str]) -> Tuple[bool, List[str]]:
    success: List[bool] = []
    updated_tags: List[str] = []
    indicator_list: List[str] = [
        'max_open_severity',
        'mean_remediate',
        'mean_remediate_critical_severity',
        'mean_remediate_high_severity',
        'mean_remediate_low_severity',
        'mean_remediate_medium_severity',
        'last_closing_date'
    ]
    tags_dict: Dict[str, List[ProjectType]] = defaultdict(list)
    groups_attrs = await aio.materialize(
        project_domain.get_attributes(
            group,
            indicator_list + ['tag']
        )
        for group in groups
    )
    groups_findings = await project_domain.list_findings(groups)
    groups_findings_attrs = await aio.materialize(
        finding_domain.get_findings_async(group_findings)
        for group_findings in groups_findings
    )
    for index, group in enumerate(groups):
        groups_attrs[index]['max_severity'] = Decimal(max(
            [
                float(finding.get('severityCvss', 0.0))
                for finding in groups_findings_attrs[index]
            ]
            if groups_findings_attrs[index]
            else [0.0]
        )).quantize(Decimal('0.1'))
        groups_attrs[index]['name'] = group
        for tag in groups_attrs[index]['tag']:
            tags_dict[tag].append(groups_attrs[index])
    for tag in tags_dict:
        updated_tags.append(tag)
        tag_info = calculate_tag_indicators(
            tag, tags_dict, indicator_list + ['max_severity']
        )
        success.append(
            await tag_dal.update(organization_name, tag, tag_info)
        )
        if success[-1]:
            await util.invalidate_cache(tag)
    return all(success), updated_tags


@async_to_sync
async def update_portfolios() -> None:
    """
    Update portfolios metrics
    """
    LOGGER.info('[scheduler]: updating portfolios indicators', **NOEXTRA)
    async for _, org_name, org_groups in \
            org_domain.iterate_organizations_and_groups():
        org_tags = await tag_domain.get_tags(org_name, ['tag'])
        org_groups_attrs = await aio.materialize(
            project_domain.get_attributes(
                group, ['project_name', 'project_status', 'tag']
            )
            for group in org_groups
        )
        tag_groups: List[str] = [
            group['project_name']
            for group in org_groups_attrs
            if group.get('project_status') == 'ACTIVE' and group.get('tag', [])
        ]
        success, updated_tags = await update_organization_indicators(
            org_name, tag_groups
        )
        if success:
            deleted_tags = [
                tag['tag']
                for tag in org_tags
                if tag['tag'] not in updated_tags
            ]
            await aio.materialize(
                tag_domain.delete(org_name, str(tag)) for tag in deleted_tags
            )
        else:
            LOGGER.error(
                '[scheduler]: error updating portfolio indicators',
                extra={'extra': {'organization': org_name}}
            )


async def reset_group_expired_accepted_findings(
        group_name: str,
        today: str) -> None:
    LOGGER.info(
        'Resetting expired accepted findings',
        extra={'extra': locals()}
    )
    list_findings = await project_domain.list_findings(
        [group_name]
    )
    findings = await finding_domain.get_findings_async(
        list_findings[0]
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
            await util.invalidate_cache(finding_id)


@async_to_sync  # type: ignore
async def reset_expired_accepted_findings() -> None:
    """ Update treatment if acceptance date expires """
    msg = '[scheduler]: reset_expired_accepted_findings is running'
    LOGGER.warning(msg, **NOEXTRA)
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    groups = await project_domain.get_active_projects()
    # number of groups that can be updated at a time
    groups_chunks = chunked(groups, 40)
    for grps_chunk in groups_chunks:
        await asyncio.gather(*[
            asyncio.create_task(
                reset_group_expired_accepted_findings(group_name, today)
            )
            for group_name in grps_chunk
        ])


@async_to_sync  # type: ignore
async def delete_pending_projects() -> None:
    """ Delete pending to delete projects """
    msg = '[scheduler]: delete_pending_projects is running'
    LOGGER.warning(msg, **NOEXTRA)
    today = datetime.now()
    projects = await project_domain.get_pending_to_delete()
    remove_project_tasks = []
    project_names = [
        project.get('project_name', '')
        for project in projects
    ]
    msg = f'- pending projects: {project_names}'
    LOGGER.info(msg, extra=dict(extra=projects))
    for project in projects:
        historic_deletion: HistoricType = cast(
            HistoricType,
            project.get('historic_deletion', [{}])
        )
        last_state = historic_deletion[-1]
        last_state_date: str = last_state.get(
            'deletion_date', today.strftime('%Y-%m-%d %H:%M:%S')
        )
        deletion_date: datetime = datetime.strptime(
            last_state_date, '%Y-%m-%d %H:%M:%S'
        )
        if deletion_date < today:
            msg = f'- project: {project.get("project_name")} will be deleted'
            LOGGER.info(msg, extra=dict(extra=project))
            task = asyncio.create_task(
                sync_to_async(project_domain.remove_project)(
                    project.get('project_name')
                )
            )
            remove_project_tasks.append(task)
            await util.invalidate_cache(str(project.get('project_name')))
    await asyncio.gather(*remove_project_tasks)
