""" Asynchronous task execution scheduler for FLUIDIntegrates """
# pylint: disable=too-many-lines

# Standard libraries
import logging
import logging.config
from itertools import chain
from collections import (
    OrderedDict,
    defaultdict,
)
from datetime import datetime
from decimal import Decimal
from typing import (
    Any,
    Callable,
    cast,
    Counter,
    Dict,
    List,
    Tuple,
    Union,
)

# Third party libraries
import bugsnag
from botocore.exceptions import ClientError
from aioextensions import (
    collect,
    schedule,
)

# Local libraries
from back.settings import (
    LOGGING,
    NOEXTRA
)
from backend import mailer
from backend.api import get_new_context
from backend.dal import (
    project as project_dal,
    tag as tag_dal,
)
from backend.domain import (
    finding as finding_domain,
    organization as org_domain,
    project as project_domain,
    tag as tag_domain,
    vulnerability as vuln_domain,
)
from backend.filters import (
    finding as finding_filters,
)
from backend.typing import (
    Event as EventType,
    Finding as FindingType,
    Historic as HistoricType,
    MailContent as MailContentType,
    Project as ProjectType,
)
from events import domain as events_domain
from newutils import datetime as datetime_utils
from newutils.findings import (
    filter_by_date,
    get_state_actions,
    sort_historic_by_date,
)
from __init__ import (
    BASE_URL,
    FI_TEST_PROJECTS,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_PROJECTS,
    FI_MAIL_REVIEWERS,
    FI_ENVIRONMENT,
    FI_BUGSNAG_API_KEY_SCHEDULER
)

logging.config.dictConfig(LOGGING)

bugsnag.configure(
    api_key=FI_BUGSNAG_API_KEY_SCHEDULER,
    project_root=BASE_URL,
    release_stage=FI_ENVIRONMENT,
)
bugsnag.start_session()

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
    events = await project_domain.list_events(project)
    event_list = await collect(
        events_domain.get_event(event)
        for event in events
    )
    unsolved_events = list(filter(is_a_unsolved_event, event_list))
    return unsolved_events


def extract_info_from_event_dict(event_dict: EventType) -> EventType:
    event_dict = {
        'type': event_dict.get('event_type', ''),
        'details': event_dict.get('detail', '')
    }
    return event_dict


async def send_unsolved_events_email(context: Any, group_name: str) -> None:
    group_loader = context.group_all
    organization_loader = context.organization
    mail_to = []
    events_info_for_email = []
    project_info = await project_domain.get_attributes(
        group_name, ['historic_configuration']
    )
    historic_configuration = cast(
        HistoricType,
        project_info.get('historic_configuration', [{}])
    )
    if (project_info and
            historic_configuration[-1].get('type', '') == 'continuous'):
        mail_to = await get_external_recipients(group_name)
        mail_to.append(FI_MAIL_CONTINUOUS)
        mail_to.append(FI_MAIL_PROJECTS)
        unsolved_events = await get_unsolved_events(group_name)
        events_info_for_email = [
            extract_info_from_event_dict(x)
            for x in unsolved_events
        ]
    group = await group_loader.load(group_name)
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']
    context_event: MailContentType = {
        'project': group_name.capitalize(),
        'organization': org_name,
        'events_len': int(len(events_info_for_email)),
        'event_url': f'{BASE_URL}/orgs/{org_name}/groups/{group_name}/events'
    }
    if context_event['events_len'] and mail_to:
        scheduler_send_mail(
            mailer.send_mail_unsolved_events,
            mail_to,
            context_event
        )


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
        last_day: str) -> Dict[str, int]:
    """Get total closed and found vulnerabilities by time range"""
    resp: Dict[str, int] = defaultdict(int)
    for vuln in vulns:
        historic_states = cast(List[Dict[str, str]], vuln['historic_state'])
        last_state = vuln_domain.get_last_approved_state(vuln)

        if (last_state and first_day <= last_state['date'] <= last_day and
                last_state['state'] == 'DELETED'):
            resp['found'] -= 1
        if first_day <= historic_states[0]['date'] <= last_day:
            resp['found'] += 1
    resp['closed'] = sum([
        get_closed_vulns(vuln, last_day) for vuln in vulns
    ])
    resp['accepted'] = sum([
        get_accepted_vulns(vuln, last_day) for vuln in vulns
    ])
    return resp


def create_weekly_date(first_date: str) -> str:
    """Create format weekly date"""
    first_date_ = datetime_utils.get_from_str(first_date)
    begin = datetime_utils.get_minus_delta(
        first_date_,
        days=(first_date_.isoweekday() - 1) % 7
    )
    end = datetime_utils.get_plus_delta(begin, days=6)
    if begin.year != end.year:
        date = '{0:%b} {0.day}, {0.year} - {1:%b} {1.day}, {1.year}'
    elif begin.month != end.month:
        date = '{0:%b} {0.day} - {1:%b} {1.day}, {1.year}'
    else:
        date = '{0:%b} {0.day} - {1.day}, {1.year}'
    return date.format(begin, end)


def get_closed_vulns(
    vuln: Dict[str, FindingType],
    last_day: str,
) -> int:
    historic_state = sort_historic_by_date(vuln['historic_state'])
    states = filter_by_date(
        historic_state, datetime_utils.get_from_str(last_day)
    )
    if (states and states[-1]['date'] <= last_day and
            states[-1]['state'] == 'closed'):
        return 1

    return 0


def get_accepted_vulns(
    vuln: Dict[str, FindingType],
    last_day: str,
) -> int:
    accepted_treatments = {'ACCEPTED', 'ACCEPTED_UNDEFINED'}
    sorted_treatment = sort_historic_by_date(
        vuln.get('historic_treatment', [])
    )
    treatments = filter_by_date(
        sorted_treatment, datetime_utils.get_from_str(last_day)
    )
    if (treatments and
            treatments[-1].get('treatment') in accepted_treatments):
        return get_by_time_range(vuln, last_day)

    return 0


def get_by_time_range(
        vuln: Dict[str, FindingType],
        last_day: str) -> int:
    """Accepted vulnerability"""
    historic_state = sort_historic_by_date(vuln['historic_state'])
    states = filter_by_date(
        historic_state, datetime_utils.get_from_str(last_day)
    )
    if (states and
            states[-1]['date'] <= last_day and states[-1]['state'] == 'open'):
        return 1

    return 0


async def create_register_by_week(
    context: Any,
    project: str
) -> List[List[Dict[str, Union[str, int]]]]:
    """Create weekly vulnerabilities registry by project"""
    finding_vulns_loader = context.finding_vulns_nzr
    group_findings_loader = context.group_findings
    accepted = 0
    closed = 0
    found = 0
    all_registers = OrderedDict()

    findings_released = await group_findings_loader.load(project)
    vulns = await finding_vulns_loader.load_many_chained([
        finding['finding_id'] for finding in findings_released
    ])

    if vulns:
        first_day, last_day = get_first_week_dates(vulns)
        first_day_last_week = get_date_last_vulns(vulns)
        while first_day <= first_day_last_week:
            result_vulns_by_week = get_status_vulns_by_time_range(
                vulns,
                first_day,
                last_day,
            )
            accepted = result_vulns_by_week.get('accepted', 0)
            closed = result_vulns_by_week.get('closed', 0)
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
            first_day = datetime_utils.get_as_str(
                datetime_utils.get_plus_delta(
                    datetime_utils.get_from_str(first_day),
                    days=7
                )
            )
            last_day = datetime_utils.get_as_str(
                datetime_utils.get_plus_delta(
                    datetime_utils.get_from_str(last_day),
                    days=7
                )
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
        datetime_utils.get_from_str(
            cast(
                List[Dict[str, str]],
                vuln['historic_state']
            )[0]['date']
        )
        for vuln in vulns
    ])
    day_week = first_date.weekday()
    first_day_delta = datetime_utils.get_minus_delta(first_date, days=day_week)
    first_day = datetime.combine(first_day_delta, datetime.min.time())
    last_day_delta = datetime_utils.get_plus_delta(first_day, days=6)
    last_day = datetime.combine(
        last_day_delta,
        datetime.max.time().replace(microsecond=0)
    )
    return (
        datetime_utils.get_as_str(first_day),
        datetime_utils.get_as_str(last_day)
    )


def get_date_last_vulns(vulns: List[Dict[str, FindingType]]) -> str:
    """Get date of the last vulnerabilities"""
    last_date = max([
        datetime_utils.get_from_str(
            cast(
                List[Dict[str, str]],
                vuln['historic_state']
            )[-1]['date']
        )
        for vuln in vulns
    ])
    day_week = last_date.weekday()
    first_day = datetime_utils.get_as_str(
        datetime_utils.get_minus_delta(last_date, days=day_week)
    )
    return first_day


async def send_group_treatment_change(
    context: Any,
    group_name: str,
    min_date: datetime
) -> None:
    payload_data = {'group_name': group_name}
    msg = 'Info: Getting treatment change'
    LOGGER.info(msg, extra={'extra': payload_data})
    findings = await finding_domain.list_findings(context, [group_name])
    await collect(
        vuln_domain.send_treatment_change_mail(context, finding_id, min_date)
        for finding_id in findings[0]
    )


async def get_group_new_vulnerabilities(context: Any, group_name: str) -> None:
    group_findings_loader = context.group_findings
    msg = 'Info: Getting new vulnerabilities'
    LOGGER.info(msg, extra={'extra': locals()})
    fin_attrs = {'finding_id', 'project_name', 'finding'}
    mail_context: MailContentType = {
        'updated_findings': list(),
        'no_treatment_findings': list()
    }
    try:
        finding_requests = await group_findings_loader.load(group_name)
        for act_finding in finding_requests:
            finding_url = get_finding_url(act_finding)
            msj_finding_pending = await create_msj_finding_pending(
                get_new_context(),
                act_finding
            )
            delta = await calculate_vulnerabilities(
                get_new_context(),
                str(act_finding['finding_id'])
            )
            finding_text = format_vulnerabilities(delta, act_finding)
            if msj_finding_pending:
                cast(
                    List[Dict[str, str]],
                    mail_context['no_treatment_findings']
                ).append({
                    'finding_name': msj_finding_pending,
                    'finding_url': finding_url
                })
            if finding_text:
                cast(
                    List[Dict[str, str]],
                    mail_context['updated_findings']
                ).append({
                    'finding_name': finding_text,
                    'finding_url': finding_url
                })
            mail_context['project'] = str.upper(str(
                act_finding['project_name']
            ))
            mail_context['project_url'] = (
                f'{BASE_URL}/groups/'
                f'{act_finding["project_name"]}/indicators'
            )
    except (TypeError, KeyError) as ex:
        LOGGER.exception(ex, extra={'extra': {'group_name': group_name}})
        raise
    if mail_context['updated_findings']:
        mail_to = await project_domain.get_users_to_notify(group_name)
        scheduler_send_mail(
            mailer.send_mail_new_vulnerabilities,
            mail_to,
            mail_context
        )


async def get_new_vulnerabilities() -> None:
    """Summary mail send with the findings of a project."""
    context = get_new_context()
    msg = '[scheduler]: get_new_vulnerabilities is running'
    LOGGER.warning(msg, **NOEXTRA)
    groups = await project_domain.get_active_projects()
    await collect([
        get_group_new_vulnerabilities(context, group)
        for group in groups
    ])


async def send_treatment_change() -> None:
    context = get_new_context()
    groups = await project_domain.get_active_projects()
    min_date = datetime_utils.get_now_minus_delta(days=1)
    await collect(
        [send_group_treatment_change(context, group_name, min_date)
         for group_name in groups],
        workers=20
    )


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


async def calculate_vulnerabilities(context: Any, finding_id: str) -> int:
    finding_vulns_loader = context.finding_vulns_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    states_actions = get_state_actions(vulns)
    today = datetime_utils.get_now()
    last_week = datetime_utils.get_now_minus_delta(days=8)
    actions = list(filter(
        lambda action: (
            datetime_utils.get_from_str(action.date, '%Y-%m-%d') >= last_week
            and datetime_utils.get_from_str(action.date, '%Y-%m-%d') <= today
        ),
        states_actions
    ))
    state_counter: Counter[str] = sum(
        [Counter({action.action: action.times}) for action in actions],
        Counter()
    )
    return state_counter['open'] - state_counter['closed']


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
    context: Any,
    act_finding: Dict[str, FindingType]
) -> str:
    """Validate if a finding has treatment."""
    finding_vulns_loader = context.finding_vulns_nzr
    finding_id = cast(str, act_finding['finding_id'])
    open_vulns = [
        vuln
        for vuln in await finding_vulns_loader.load(finding_id)
        if vuln['current_state'] == 'open'
        and cast(
            List[Dict[str, str]],
            vuln.get('historic_treatment', [{}])
        )[-1].get('treatment', 'NEW') == 'NEW'
    ]
    if open_vulns:
        context = get_new_context()
        days = finding_domain.get_finding_age(context, finding_id)
        finding_name = f'{act_finding["finding"]} -{days} day(s)-'
        result = finding_name
    else:
        result = ''
    return result


async def get_remediated_findings() -> None:
    """Summary mail send with findings that have not been verified yet."""
    msg = '[scheduler]: get_remediated_findings is running'
    LOGGER.warning(msg, extra=dict(extra=None))
    active_projects = await project_domain.get_active_projects()
    findings = []
    pending_verification_findings = await collect(
        project_domain.get_pending_verification_findings(
            get_new_context(),
            project
        )
        for project in active_projects
    )
    for project_findings in pending_verification_findings:
        findings += project_findings

    if findings:
        try:
            mail_to = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
            context: MailContentType = {'findings': list(), 'total': 0}
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
            scheduler_send_mail(
                mailer.send_mail_new_remediated,
                mail_to,
                context
            )
        except (TypeError, KeyError) as ex:
            LOGGER.exception(ex, extra={'extra': locals()})
    else:
        msg = '[scheduler]: There are no findings to verify'
        LOGGER.warning(msg, extra=dict(extra=None))


async def get_new_releases() -> None:  # pylint: disable=too-many-locals
    """Summary mail send with findings that have not been released yet."""
    context = get_new_context()
    group_loader = context.group_all
    organization_loader = context.organization
    msg = '[scheduler]: get_new_releases is running'
    LOGGER.warning(msg, extra=dict(extra=None))
    test_groups = FI_TEST_PROJECTS.split(',')
    groups = await project_domain.get_active_projects()
    email_context: MailContentType = (
        defaultdict(list)
    )
    cont = 0
    groups = [
        group
        for group in groups
        if group not in test_groups
    ]
    list_drafts = await finding_domain.list_drafts(groups)
    group_drafts = await collect(
        finding_domain.get_findings_async(drafts)
        for drafts in list_drafts
    )
    for group_name, finding_requests in zip(groups, group_drafts):
        if group_name not in test_groups:
            try:
                for finding in finding_requests:
                    is_finding_released = finding_filters.is_released(finding)
                    if not is_finding_released:
                        group = await group_loader.load(group_name)
                        org_id = group['organization']
                        organization = await organization_loader.load(org_id)
                        org_name = organization['name']
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
                                f'{BASE_URL}/orgs/{org_name}/groups/'
                                f'{group_name}/drafts/'
                                f'{finding.get("findingId")}/description'
                            ),
                            'project': group_name.upper(),
                            'organization': org_name
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
        scheduler_send_mail(
            mailer.send_mail_new_releases,
            mail_to,
            email_context
        )
    else:
        msg = '[scheduler]: There are no new drafts'
        LOGGER.warning(msg, extra=dict(extra=None))


async def send_unsolved_to_all() -> None:
    """Send email with unsolved events to all projects """
    context = get_new_context()
    msg = '[scheduler]: send_unsolved_to_all is running'
    LOGGER.warning(msg, extra=dict(extra=None))
    projects = await project_domain.get_active_projects()
    await collect(
        send_unsolved_events_email(context, project)
        for project in projects
    )


async def get_project_indicators(project: str) -> Dict[str, object]:
    context = get_new_context()
    group_findings_loader = context.group_findings

    findings = await group_findings_loader.load(project)
    last_closing_vuln_days, last_closing_vuln = (
        await project_domain.get_last_closing_vuln_info(context, findings)
    )
    max_open_severity, max_open_severity_finding = (
        await project_domain.get_max_open_severity(context, findings)
    )
    remediated_over_time = await create_register_by_week(
        context,
        project
    )
    indicators = {
        'closed_vulnerabilities': (
            await project_domain.get_closed_vulnerabilities(context, project)
        ),
        'last_closing_date': last_closing_vuln_days,
        'last_closing_vuln_finding': last_closing_vuln.get('finding_id', ''),
        'mean_remediate': await project_domain.get_mean_remediate(
            context,
            project
        ),
        'mean_remediate_non_treated': (
            await project_domain.get_mean_remediate_non_treated(project)
        ),
        'mean_remediate_critical_severity': (
            await project_domain.get_mean_remediate_severity(
                context,
                project,
                9,
                10
            )
        ),
        'mean_remediate_high_severity': (
            await project_domain.get_mean_remediate_severity(
                context,
                project,
                7,
                8.9
            )
        ),
        'mean_remediate_low_severity': (
            await project_domain.get_mean_remediate_severity(
                context,
                project,
                0.1,
                3.9
            )
        ),
        'mean_remediate_medium_severity': (
            await project_domain.get_mean_remediate_severity(
                context,
                project,
                4,
                6.9
            )
        ),
        'max_open_severity': max_open_severity,
        'max_open_severity_finding': max_open_severity_finding.get(
            'finding_id', ''
        ),
        'open_findings': await project_domain.get_open_finding(
            context,
            project
        ),
        'open_vulnerabilities': (
            await project_domain.get_open_vulnerabilities(context, project)
        ),
        'total_treatment': await project_domain.get_total_treatment(
            context,
            findings
        ),
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
            msg = 'Info: Updated indicators'
            LOGGER.info(msg, extra={'extra': payload_data})
        else:
            msg = 'Error: An error ocurred updating indicators in the database'
            LOGGER.info(msg, extra={'extra': payload_data})
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': payload_data})


async def update_indicators() -> None:
    """Update in dynamo indicators."""
    msg = '[scheduler]: update_indicators is running'
    LOGGER.warning(msg, **NOEXTRA)
    groups = await project_domain.get_active_projects()
    await collect(map(update_group_indicators, groups), workers=20)


async def update_organization_indicators(
    context: Any,
    organization_name: str,
    groups: List[str]
) -> Tuple[bool, List[str]]:
    group_findings_loader = context.group_findings

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
    groups_attrs = await collect(
        project_domain.get_attributes(
            group,
            indicator_list + ['tag']
        )
        for group in groups
    )
    group_findings = await group_findings_loader.load_many(groups)
    for index, group in enumerate(groups):
        groups_attrs[index]['max_severity'] = Decimal(max(
            [
                float(finding.get('cvss_temporal', 0.0))
                for finding in group_findings[index]
            ]
            if group_findings[index]
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
    return all(success), updated_tags


async def update_portfolios() -> None:
    """
    Update portfolios metrics
    """
    LOGGER.info('[scheduler]: updating portfolios indicators', **NOEXTRA)
    context = get_new_context()
    group_loader = context.group_all
    async for _, org_name, org_groups in \
            org_domain.iterate_organizations_and_groups():
        org_tags = await context.organization_tags.load(org_name)
        org_groups_attrs = await group_loader.load_many(
            list(org_groups)
        )
        tag_groups: List[str] = [
            str(group['name'])
            for group in org_groups_attrs
            if group['project_status'] == 'ACTIVE' and group['tags']
        ]
        success, updated_tags = await update_organization_indicators(
            context,
            org_name,
            tag_groups
        )
        if success:
            deleted_tags = [
                tag['tag']
                for tag in org_tags
                if tag['tag'] not in updated_tags
            ]
            await collect(
                tag_domain.delete(org_name, str(tag)) for tag in deleted_tags
            )
        else:
            LOGGER.error(
                '[scheduler]: error updating portfolio indicators',
                extra={'extra': {'organization': org_name}}
            )


async def reset_group_expired_accepted_findings(
    context: Any,
    group_name: str,
    today: str
) -> None:
    LOGGER.info(
        'Resetting expired accepted findings',
        extra={'extra': locals()}
    )
    finding_vulns_loader = context.finding_vulns
    group_findings_loader = context.group_findings

    group_findings = await group_findings_loader.load(group_name)
    vulns = list(
        chain.from_iterable(
            await finding_vulns_loader.load_many([
                finding['finding_id'] for finding in group_findings
            ])
        )
    )

    for vuln in vulns:
        finding_id = cast(str, vuln.get('finding_id'))
        historic_treatment = cast(
            List[Dict[str, str]],
            vuln.get('historic_treatment', [{}])
        )
        is_accepted_expired = (
            historic_treatment[-1].get('acceptance_date', today) < today
        )
        is_undefined_accepted_expired = (
            (historic_treatment[-1].get('treatment') ==
                'ACCEPTED_UNDEFINED') and
            (historic_treatment[-1].get('acceptance_status') ==
                'SUBMITTED') and
            datetime_utils.get_plus_delta(
                datetime_utils.get_from_str(
                    historic_treatment[-1].get(
                        'date', datetime_utils.DEFAULT_STR
                    )
                ),
                days=5
            ) <= datetime_utils.get_from_str(today)
        )
        if is_accepted_expired or is_undefined_accepted_expired:
            updated_values = {'treatment': 'NEW'}
            await vuln_domain.add_vuln_treatment(
                finding_id=finding_id,
                updated_values=updated_values,
                vuln=vuln,
                user_email=historic_treatment[-1].get('user', ''),
                date=datetime_utils.get_as_str(datetime_utils.get_now())
            )


async def reset_expired_accepted_findings() -> None:
    """ Update treatment if acceptance date expires """
    msg = '[scheduler]: reset_expired_accepted_findings is running'
    LOGGER.warning(msg, **NOEXTRA)
    today = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )
    context = get_new_context()
    groups = await project_domain.get_active_projects()
    await collect(
        [reset_group_expired_accepted_findings(context, group_name, today)
         for group_name in groups],
        workers=40
    )


def scheduler_send_mail(
    send_mail_function: Callable,
    mail_to: List[str],
    mail_context: MailContentType
) -> None:
    schedule(
        send_mail_function(mail_to, mail_context)
    )


async def delete_obsolete_orgs() -> None:
    """ Delete obsolete organizations """
    msg = '[scheduler]: delete_obsolete_orgs is running'
    LOGGER.info(msg, **NOEXTRA)
    today = datetime_utils.get_now().date()
    email = 'integrates@fluidattacks.com'
    async for org_id, org_name in org_domain.iterate_organizations():
        org_pending_deletion_date_str = (
            await org_domain.get_pending_deletion_date_str(org_id)
        )
        org_users = await org_domain.get_users(org_id)
        org_groups = await org_domain.get_groups(org_id)
        if len(org_users) <= 1 or len(org_groups) == 0:
            if org_pending_deletion_date_str:
                org_pending_deletion_date = datetime_utils.get_from_str(
                    org_pending_deletion_date_str
                )
                if org_pending_deletion_date.date() <= today:
                    msg = f'- organization: {org_name} will be deleted'
                    LOGGER.info(msg, **NOEXTRA)
                    await org_domain.delete_organization(
                        get_new_context(),
                        org_id,
                        email
                    )
            else:
                new_org_pending_deletion_date_str = datetime_utils.get_as_str(
                    datetime_utils.get_now_plus_delta(days=60)
                )
                await org_domain.update_pending_deletion_date(
                    org_id,
                    org_name,
                    new_org_pending_deletion_date_str
                )
                if org_users:
                    scheduler_send_mail(
                        mailer.send_mail_org_deletion,
                        org_users,
                        {
                            'deletion_date': new_org_pending_deletion_date_str,
                            'org_name': org_name,
                        }
                    )
        else:
            await org_domain.update_pending_deletion_date(
                org_id,
                org_name,
                None
            )
