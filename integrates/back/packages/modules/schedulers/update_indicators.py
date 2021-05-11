
import logging
import logging.config
from collections import (
    OrderedDict,
    defaultdict,
)
from datetime import datetime
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
    cast,
)

from aioextensions import collect
from botocore.exceptions import ClientError

from back.settings import LOGGING
from custom_types import Finding as FindingType
from dataloaders import get_new_context
from findings import domain as findings_domain
from groups import domain as groups_domain
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
    vulnerabilities as vulns_utils,
)


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


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


async def create_register_by_week(
    context: Any,
    group: str,
    min_date: Optional[datetime] = None
) -> List[List[Dict[str, Union[str, int]]]]:
    """Create weekly vulnerabilities registry by group"""
    finding_vulns_loader = context.finding_vulns_nzr
    accepted = 0
    closed = 0
    found = 0
    all_registers = OrderedDict()

    findings_released = await context.group_findings.load(group)
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
            if any(
                status_vuln
                for status_vuln in list(result_vulns_by_week.values())
            ):
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


def get_accepted_vulns(
    vuln: Dict[str, FindingType],
    last_day: str,
    min_date: Optional[str] = None,
) -> int:
    accepted_vulns: int = 0
    accepted_treatments = {'ACCEPTED', 'ACCEPTED_UNDEFINED'}
    sorted_treatment = findings_utils.sort_historic_by_date(
        vuln.get('historic_treatment', [])
    )
    treatments = findings_utils.filter_by_date(
        sorted_treatment,
        datetime_utils.get_from_str(last_day)
    )
    if (
        treatments and
        treatments[-1].get('treatment') in accepted_treatments
    ):
        accepted_vulns = get_by_time_range(vuln, last_day, min_date)
    return accepted_vulns


def get_by_time_range(
    vuln: Dict[str, FindingType],
    last_day: str,
    min_date: Optional[str] = None,
) -> int:
    """Accepted vulnerability"""
    accepted_vulns: int = 0
    historic_state = findings_utils.sort_historic_by_date(
        vuln['historic_state']
    )
    states = findings_utils.filter_by_date(
        historic_state,
        datetime_utils.get_from_str(last_day)
    )
    if (
        states and
        states[-1]['date'] <= last_day and
        states[-1]['state'] == 'open'
    ):
        accepted_vulns = 1
        if (
            min_date and
            datetime_utils.get_from_str(
                historic_state[0]['date']
            ) < datetime_utils.get_from_str(min_date)
        ):
            accepted_vulns = 0
    return accepted_vulns


def get_closed_vulns(
    vuln: Dict[str, FindingType],
    last_day: str,
    min_date: Optional[str] = None,
) -> int:
    closed_vulns: int = 0
    historic_state = findings_utils.sort_historic_by_date(
        vuln['historic_state']
    )
    states = findings_utils.filter_by_date(
        historic_state,
        datetime_utils.get_from_str(last_day)
    )
    if (
        states and
        states[-1]['date'] <= last_day and
        states[-1]['state'] == 'closed'
    ):
        closed_vulns = 1
        if (
            min_date and
            datetime_utils.get_from_str(
                historic_state[0]['date']
            ) < datetime_utils.get_from_str(min_date)
        ):
            closed_vulns = 0
    return closed_vulns


def get_date_last_vulns(vulns: List[Dict[str, FindingType]]) -> str:
    """Get date of the last vulnerabilities"""
    last_date = max([
        datetime_utils.get_from_str(
            cast(List[Dict[str, str]], vuln['historic_state'])[-1]['date']
        )
        for vuln in vulns
    ])
    day_week = last_date.weekday()
    first_day = datetime_utils.get_as_str(
        datetime_utils.get_minus_delta(last_date, days=day_week)
    )
    return first_day


def get_first_week_dates(
    vulns: List[Dict[str, FindingType]],
    min_date: Optional[datetime] = None
) -> Tuple[str, str]:
    """Get first week vulnerabilities"""
    first_date = min([
        datetime_utils.get_from_str(
            cast(List[Dict[str, str]], vuln['historic_state'])[0]['date']
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


async def get_group_indicators(group: str) -> Dict[str, object]:
    context = get_new_context()
    group_findings_loader = context.group_findings
    findings = await group_findings_loader.load(group)

    last_closing_vuln_days, last_closing_vuln = (
        await findings_domain.get_last_closing_vuln_info(context, findings)
    )
    max_open_severity, max_open_severity_finding = (
        await findings_domain.get_max_open_severity(context, findings)
    )
    remediated_over_time = await create_register_by_week(
        context,
        group
    )
    remediated_over_thirty_days = await create_register_by_week(
        context,
        group,
        datetime.combine(
            datetime_utils.get_now_minus_delta(days=30),
            datetime.min.time()
        )
    )
    remediated_over_ninety_days = await create_register_by_week(
        context,
        group,
        datetime.combine(
            datetime_utils.get_now_minus_delta(days=90),
            datetime.min.time()
        )
    )
    indicators = {
        'closed_vulnerabilities': (
            await groups_domain.get_closed_vulnerabilities(context, group)
        ),
        'last_closing_date': last_closing_vuln_days,
        'last_closing_vuln_finding': last_closing_vuln.get('finding_id', ''),
        'mean_remediate': await groups_domain.get_mean_remediate(
            context,
            group
        ),
        'mean_remediate_non_treated': (
            await groups_domain.get_mean_remediate_non_treated(group)
        ),
        'mean_remediate_critical_severity': (
            await groups_domain.get_mean_remediate_severity(
                context,
                group,
                9,
                10
            )
        ),
        'mean_remediate_high_severity': (
            await groups_domain.get_mean_remediate_severity(
                context,
                group,
                7,
                8.9
            )
        ),
        'mean_remediate_low_severity': (
            await groups_domain.get_mean_remediate_severity(
                context,
                group,
                0.1,
                3.9
            )
        ),
        'mean_remediate_medium_severity': (
            await groups_domain.get_mean_remediate_severity(
                context,
                group,
                4,
                6.9
            )
        ),
        'max_open_severity': max_open_severity,
        'max_open_severity_finding': max_open_severity_finding.get(
            'finding_id',
            ''
        ),
        'open_findings': await groups_domain.get_open_finding(
            context,
            group
        ),
        'open_vulnerabilities': (
            await groups_domain.get_open_vulnerabilities(context, group)
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

        if (
            last_state and
            first_day <= last_state['date'] <= last_day and
            last_state['state'] == 'DELETED'
        ):
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


async def update_group_indicators(group_name: str) -> None:
    payload_data = {'group_name': group_name}
    indicators = await get_group_indicators(group_name)
    try:
        response = await groups_domain.update(group_name, indicators)
        if not response:
            msg = 'Error: An error ocurred updating indicators in the database'
            LOGGER.error(msg, extra={'extra': payload_data})
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': payload_data})


async def update_indicators() -> None:
    """Update in dynamo indicators."""
    groups = await groups_domain.get_active_groups()
    await collect(map(update_group_indicators, groups), workers=20)


async def main() -> None:
    await update_indicators()
