""" Asynchronous task execution scheduler for FLUIDIntegrates """
# pylint: disable=too-many-lines

# Standard libraries
import logging
import logging.config
from collections import (
    defaultdict,
    OrderedDict,
)
from datetime import datetime
from decimal import Decimal
from itertools import chain
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

# Third party libraries
import bugsnag
from aioextensions import (
    collect,
    schedule,
)
from botocore.exceptions import ClientError

# Local libraries
from back.settings import LOGGING
from backend import mailer
from backend.api import get_new_context
from backend.typing import (
    Event as EventType,
    Finding as FindingType,
    Historic as HistoricType,
    MailContent as MailContentType,
    Project as ProjectType,
)
from events import domain as events_domain
from findings import domain as findings_domain
from groups import domain as groups_domain
from group_access import domain as group_access_domain
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
    vulnerabilities as vulns_utils,
)
from newutils.findings import (
    filter_by_date,
    sort_historic_by_date,
)
from organizations import domain as orgs_domain
from tags import domain as tags_domain
from vulnerabilities import domain as vulns_domain
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
    events = await events_domain.list_group_events(project)
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
    project_info = await groups_domain.get_attributes(
        group_name, ['historic_configuration']
    )
    historic_configuration = cast(
        HistoricType,
        project_info.get('historic_configuration', [{}])
    )
    if (project_info and
            historic_configuration[-1].get('type', '') == 'continuous'):
        mail_to = await get_external_recipients(group_name)
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
    recipients = await group_access_domain.get_managers(project)
    return remove_fluid_from_recipients(recipients)


def get_status_vulns_by_time_range(
        vulns: List[Dict[str, FindingType]],
        first_day: str,
        last_day: str,
        min_date: Optional[str] = None
) -> Dict[str, int]:
    """Get total closed and found vulnerabilities by time range"""
    resp: Dict[str, int] = defaultdict(int)
    for vuln in vulns:
        historic_states = cast(List[Dict[str, str]], vuln['historic_state'])
        last_state = vulns_utils.get_last_approved_state(vuln)

        if (last_state and first_day <= last_state['date'] <= last_day and
                last_state['state'] == 'DELETED'):
            resp['found'] -= 1
        if first_day <= historic_states[0]['date'] <= last_day:
            resp['found'] += 1
    resp['closed'] = sum([
        get_closed_vulns(vuln, last_day, min_date) for vuln in vulns
    ])
    resp['accepted'] = sum([
        get_accepted_vulns(vuln, last_day, min_date) for vuln in vulns
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
    min_date: Optional[str] = None,
) -> int:
    historic_state = sort_historic_by_date(vuln['historic_state'])
    states = filter_by_date(
        historic_state, datetime_utils.get_from_str(last_day)
    )
    if (states and states[-1]['date'] <= last_day and
            states[-1]['state'] == 'closed'):
        if (
            min_date and
            datetime_utils.get_from_str(
                historic_state[0]['date']
            ) < datetime_utils.get_from_str(min_date)
        ):
            return 0
        return 1

    return 0


def get_accepted_vulns(
    vuln: Dict[str, FindingType],
    last_day: str,
    min_date: Optional[str] = None,
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
        return get_by_time_range(vuln, last_day, min_date)

    return 0


def get_by_time_range(
    vuln: Dict[str, FindingType],
    last_day: str,
    min_date: Optional[str] = None,
) -> int:
    """Accepted vulnerability"""
    historic_state = sort_historic_by_date(vuln['historic_state'])
    states = filter_by_date(
        historic_state, datetime_utils.get_from_str(last_day)
    )
    if (states and
            states[-1]['date'] <= last_day and states[-1]['state'] == 'open'):
        if (
            min_date and
            datetime_utils.get_from_str(
                historic_state[0]['date']
            ) < datetime_utils.get_from_str(min_date)
        ):
            return 0

        return 1

    return 0


async def create_register_by_week(
    context: Any,
    project: str,
    min_date: Optional[datetime] = None
) -> List[List[Dict[str, Union[str, int]]]]:
    """Create weekly vulnerabilities registry by project"""
    finding_vulns_loader = context.finding_vulns_nzr
    accepted = 0
    closed = 0
    found = 0
    all_registers = OrderedDict()

    findings_released = await context.group_findings.load(project)
    vulns = await finding_vulns_loader.load_many_chained([
        finding['finding_id'] for finding in findings_released
    ])

    if vulns:
        first_day, last_day = get_first_week_dates(vulns, min_date)
        first_day_last_week = get_date_last_vulns(vulns)
        while first_day <= first_day_last_week:
            result_vulns_by_week = get_status_vulns_by_time_range(
                vulns,
                first_day,
                last_day,
                datetime_utils.get_as_str(min_date) if min_date else None
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
    vulns: List[Dict[str, FindingType]],
    min_date: Optional[datetime] = None
) -> Tuple[str, str]:
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
    if min_date:
        first_date = min_date
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


async def get_remediated_findings() -> None:
    """Summary mail send with findings that have not been verified yet."""
    active_projects = await groups_domain.get_active_groups()
    findings = []
    pending_verification_findings = await collect(
        findings_domain.get_pending_verification_findings(
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


async def get_new_releases() -> None:  # pylint: disable=too-many-locals
    """Summary mail send with findings that have not been released yet."""
    context = get_new_context()
    group_loader = context.group_all
    organization_loader = context.organization
    test_groups = FI_TEST_PROJECTS.split(',')
    groups = await groups_domain.get_active_groups()
    email_context: MailContentType = (
        defaultdict(list)
    )
    cont = 0
    groups = [
        group
        for group in groups
        if group not in test_groups
    ]
    list_drafts = await findings_domain.list_drafts(groups)
    group_drafts = await collect(
        findings_domain.get_findings_async(drafts)
        for drafts in list_drafts
    )
    for group_name, finding_requests in zip(groups, group_drafts):
        if group_name not in test_groups:
            try:
                for finding in finding_requests:
                    is_finding_released = findings_utils.is_released(finding)
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


async def send_unsolved_to_all() -> None:
    """Send email with unsolved events to all projects """
    context = get_new_context()
    projects = await groups_domain.get_active_groups()
    await collect(
        send_unsolved_events_email(context, project)
        for project in projects
    )


async def get_project_indicators(project: str) -> Dict[str, object]:
    context = get_new_context()
    group_findings_loader = context.group_findings

    findings = await group_findings_loader.load(project)
    last_closing_vuln_days, last_closing_vuln = (
        await findings_domain.get_last_closing_vuln_info(context, findings)
    )
    max_open_severity, max_open_severity_finding = (
        await findings_domain.get_max_open_severity(context, findings)
    )
    remediated_over_time = await create_register_by_week(
        context,
        project
    )
    remediated_over_thirty_days = await create_register_by_week(
        context,
        project,
        datetime.combine(
            datetime_utils.get_now_minus_delta(days=30), datetime.min.time()
        )
    )
    remediated_over_ninety_days = await create_register_by_week(
        context,
        project,
        datetime.combine(
            datetime_utils.get_now_minus_delta(days=90), datetime.min.time()
        )
    )
    indicators = {
        'closed_vulnerabilities': (
            await groups_domain.get_closed_vulnerabilities(context, project)
        ),
        'last_closing_date': last_closing_vuln_days,
        'last_closing_vuln_finding': last_closing_vuln.get('finding_id', ''),
        'mean_remediate': await groups_domain.get_mean_remediate(
            context,
            project
        ),
        'mean_remediate_non_treated': (
            await groups_domain.get_mean_remediate_non_treated(project)
        ),
        'mean_remediate_critical_severity': (
            await groups_domain.get_mean_remediate_severity(
                context,
                project,
                9,
                10
            )
        ),
        'mean_remediate_high_severity': (
            await groups_domain.get_mean_remediate_severity(
                context,
                project,
                7,
                8.9
            )
        ),
        'mean_remediate_low_severity': (
            await groups_domain.get_mean_remediate_severity(
                context,
                project,
                0.1,
                3.9
            )
        ),
        'mean_remediate_medium_severity': (
            await groups_domain.get_mean_remediate_severity(
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
        'open_findings': await groups_domain.get_open_finding(
            context,
            project
        ),
        'open_vulnerabilities': (
            await groups_domain.get_open_vulnerabilities(context, project)
        ),
        'total_treatment': await findings_domain.get_total_treatment(
            context,
            findings
        ),
        'remediated_over_time': remediated_over_time,
        'remediated_over_time_30': remediated_over_thirty_days,
        'remediated_over_time_90': remediated_over_ninety_days
    }
    return indicators


async def update_group_indicators(group_name: str) -> None:
    payload_data = {
        'group_name': group_name
    }
    indicators = await get_project_indicators(group_name)
    try:
        response = await groups_domain.update(
            group_name,
            indicators
        )
        if not response:
            msg = 'Error: An error ocurred updating indicators in the database'
            LOGGER.error(msg, extra={'extra': payload_data})
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': payload_data})


async def update_indicators() -> None:
    """Update in dynamo indicators."""
    groups = await groups_domain.get_active_groups()
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
        groups_domain.get_attributes(
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
            await tags_domain.update(organization_name, tag, tag_info)
        )
    return all(success), updated_tags


async def update_portfolios() -> None:
    """
    Update portfolios metrics
    """
    context = get_new_context()
    group_loader = context.group_all
    async for _, org_name, org_groups in \
            orgs_domain.iterate_organizations_and_groups():
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
                tags_domain.delete(org_name, str(tag)) for tag in deleted_tags
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
            await vulns_domain.add_vuln_treatment(
                finding_id=finding_id,
                updated_values=updated_values,
                vuln=vuln,
                user_email=historic_treatment[-1].get('user', ''),
                date=datetime_utils.get_as_str(datetime_utils.get_now())
            )


async def reset_expired_accepted_findings() -> None:
    """ Update treatment if acceptance date expires """
    today = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )
    context = get_new_context()
    groups = await groups_domain.get_active_groups()
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
