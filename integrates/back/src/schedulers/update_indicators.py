from aioextensions import (
    collect,
)
from botocore.exceptions import (
    ClientError,
)
from collections import (
    OrderedDict,
)
from custom_types import (
    Finding as FindingType,
    Historic,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from findings import (
    domain as findings_domain,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
    vulnerabilities as vulns_utils,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


class VulnerabilityStatusByTimeRange(NamedTuple):
    vulnerabilities: int
    cvssf: Decimal


class VulnerabilitiesStatusByTimeRange(NamedTuple):
    accepted_vulnerabilities: int
    closed_vulnerabilities: int
    found_vulnerabilities: int
    accepted_cvssf: Decimal
    closed_cvssf: Decimal
    found_cvssf: Decimal


class RegisterByWeek(NamedTuple):
    vulnerabilities: List[List[Dict[str, Union[str, int]]]]
    vulnerabilities_cvssf: List[List[Dict[str, Union[str, int]]]]


def create_data_format_chart(
    all_registers: Dict[str, Dict[str, int]]
) -> List[List[Dict[str, Union[str, int]]]]:
    result_data = []
    plot_points: Dict[str, List[Dict[str, Union[str, int]]]] = {
        "found": [],
        "closed": [],
        "accepted": [],
        "assumed_closed": [],
        "opened": [],
    }
    for week, dict_status in list(all_registers.items()):
        for status in plot_points:
            plot_points[status].append({"x": week, "y": dict_status[status]})
    for status in plot_points:
        result_data.append(plot_points[status])
    return result_data


def get_severity(
    *,
    findings_dict: Dict[str, Dict[str, FindingType]],
    vulnerability: Dict[str, FindingType],
) -> Decimal:
    return Decimal(
        findings_dict[str(vulnerability["finding_id"])].get(
            "cvss_temporal", 0.0
        )
    )


async def create_register_by_week(  # pylint: disable=too-many-locals
    context: Any, group: str, min_date: Optional[datetime] = None
) -> RegisterByWeek:
    """Create weekly vulnerabilities registry by group"""
    found = 0
    found_cvssf = Decimal(0.0)
    all_registers = OrderedDict()
    all_registers_cvsff = OrderedDict()

    findings: List[Dict[str, FindingType]] = await context.group_findings.load(
        group
    )
    vulns = await context.finding_vulns_nzr.load_many_chained(
        [finding["finding_id"] for finding in findings]
    )
    findings_dict: Dict[str, Dict[str, FindingType]] = {
        str(finding["finding_id"]): finding for finding in findings
    }
    vulnerabilities_severity = [
        get_severity(findings_dict=findings_dict, vulnerability=vulnerability)
        for vulnerability in vulns
    ]
    historic_states = [
        findings_utils.sort_historic_by_date(vulnerability["historic_state"])
        for vulnerability in vulns
    ]

    if vulns:
        first_day, last_day = get_first_week_dates(vulns, min_date)
        first_day_last_week = get_date_last_vulns(vulns)
        while first_day <= first_day_last_week:
            result_vulns_by_week: VulnerabilitiesStatusByTimeRange = (
                get_status_vulns_by_time_range(
                    vulnerabilities=vulns,
                    vulnerabilities_severity=vulnerabilities_severity,
                    vulnerabilities_historic_states=historic_states,
                    first_day=first_day,
                    last_day=last_day,
                    min_date=datetime_utils.get_as_str(min_date)
                    if min_date
                    else None,
                )
            )
            found += result_vulns_by_week.found_vulnerabilities
            found_cvssf += result_vulns_by_week.found_cvssf
            if any(
                [
                    result_vulns_by_week.accepted_vulnerabilities,
                    result_vulns_by_week.closed_vulnerabilities,
                    result_vulns_by_week.found_vulnerabilities,
                ]
            ):
                week_dates = create_weekly_date(first_day)
                all_registers[week_dates] = {
                    "found": found,
                    "closed": result_vulns_by_week.closed_vulnerabilities,
                    "accepted": result_vulns_by_week.accepted_vulnerabilities,
                    "assumed_closed": (
                        result_vulns_by_week.accepted_vulnerabilities
                        + result_vulns_by_week.closed_vulnerabilities
                    ),
                    "opened": found
                    - result_vulns_by_week.closed_vulnerabilities
                    - result_vulns_by_week.accepted_vulnerabilities,
                }
                all_registers_cvsff[week_dates] = {
                    "found": int(
                        found_cvssf.to_integral_exact(rounding=ROUND_CEILING)
                    ),
                    "closed": int(
                        result_vulns_by_week.closed_cvssf.to_integral_exact(
                            rounding=ROUND_CEILING
                        )
                    ),
                    "accepted": int(
                        result_vulns_by_week.accepted_cvssf.to_integral_exact(
                            rounding=ROUND_CEILING
                        )
                    ),
                    "assumed_closed": int(
                        (
                            result_vulns_by_week.accepted_cvssf
                            + result_vulns_by_week.closed_cvssf
                        ).to_integral_exact(rounding=ROUND_CEILING)
                    ),
                    "opened": int(
                        (
                            found_cvssf
                            - result_vulns_by_week.closed_cvssf
                            - result_vulns_by_week.accepted_cvssf
                        ).to_integral_exact(rounding=ROUND_CEILING)
                    ),
                }
            first_day = datetime_utils.get_as_str(
                datetime_utils.get_plus_delta(
                    datetime_utils.get_from_str(first_day), days=7
                )
            )
            last_day = datetime_utils.get_as_str(
                datetime_utils.get_plus_delta(
                    datetime_utils.get_from_str(last_day), days=7
                )
            )
    return RegisterByWeek(
        vulnerabilities=create_data_format_chart(all_registers),
        vulnerabilities_cvssf=create_data_format_chart(all_registers_cvsff),
    )


def create_weekly_date(first_date: str) -> str:
    """Create format weekly date"""
    first_date_ = datetime_utils.get_from_str(first_date)
    begin = datetime_utils.get_minus_delta(
        first_date_, days=(first_date_.isoweekday() - 1) % 7
    )
    end = datetime_utils.get_plus_delta(begin, days=6)
    if begin.year != end.year:
        date = "{0:%b} {0.day}, {0.year} - {1:%b} {1.day}, {1.year}"
    elif begin.month != end.month:
        date = "{0:%b} {0.day} - {1:%b} {1.day}, {1.year}"
    else:
        date = "{0:%b} {0.day} - {1.day}, {1.year}"
    return date.format(begin, end)


def get_accepted_vulns(
    vuln: Dict[str, FindingType],
    historic_state: List[Dict[str, str]],
    severity: Decimal,
    last_day: str,
    min_date: Optional[str] = None,
) -> VulnerabilityStatusByTimeRange:
    accepted_treatments = {"ACCEPTED", "ACCEPTED_UNDEFINED"}
    sorted_treatment = findings_utils.sort_historic_by_date(
        vuln.get("historic_treatment", [])
    )
    treatments = findings_utils.filter_by_date(
        sorted_treatment, datetime_utils.get_from_str(last_day)
    )
    if treatments and treatments[-1].get("treatment") in accepted_treatments:
        return get_by_time_range(historic_state, severity, last_day, min_date)
    return VulnerabilityStatusByTimeRange(
        vulnerabilities=0, cvssf=Decimal("0.0")
    )


def get_by_time_range(
    historic_state: List[Dict[str, str]],
    severity: Decimal,
    last_day: str,
    min_date: Optional[str] = None,
) -> VulnerabilityStatusByTimeRange:
    """Accepted vulnerability"""
    states = findings_utils.filter_by_date(
        historic_state, datetime_utils.get_from_str(last_day)
    )
    if (
        states
        and states[-1]["date"] <= last_day
        and states[-1]["state"] == "open"
        and not (
            min_date
            and datetime_utils.get_from_str(historic_state[0]["date"])
            < datetime_utils.get_from_str(min_date)
        )
    ):
        return VulnerabilityStatusByTimeRange(
            vulnerabilities=1, cvssf=get_cssvf(severity)
        )
    return VulnerabilityStatusByTimeRange(
        vulnerabilities=0, cvssf=Decimal("0.0")
    )


def get_closed_vulns(
    historic_state: List[Dict[str, str]],
    severity: Decimal,
    last_day: str,
    min_date: Optional[str] = None,
) -> VulnerabilityStatusByTimeRange:
    states = findings_utils.filter_by_date(
        historic_state, datetime_utils.get_from_str(last_day)
    )
    if (
        states
        and states[-1]["date"] <= last_day
        and states[-1]["state"] == "closed"
        and not (
            min_date
            and datetime_utils.get_from_str(historic_state[0]["date"])
            < datetime_utils.get_from_str(min_date)
        )
    ):
        return VulnerabilityStatusByTimeRange(
            vulnerabilities=1, cvssf=get_cssvf(severity)
        )
    return VulnerabilityStatusByTimeRange(
        vulnerabilities=0, cvssf=Decimal("0.0")
    )


def get_date_last_vulns(vulns: List[Dict[str, FindingType]]) -> str:
    """Get date of the last vulnerabilities"""
    last_date = max(
        [
            datetime_utils.get_from_str(
                cast(List[Dict[str, str]], vuln["historic_state"])[-1]["date"]
            )
            for vuln in vulns
        ]
    )
    day_week = last_date.weekday()
    first_day = datetime_utils.get_as_str(
        datetime_utils.get_minus_delta(last_date, days=day_week)
    )
    return first_day


def get_first_week_dates(
    vulns: List[Dict[str, FindingType]], min_date: Optional[datetime] = None
) -> Tuple[str, str]:
    """Get first week vulnerabilities"""
    first_date = min(
        [
            datetime_utils.get_from_str(
                cast(List[Dict[str, str]], vuln["historic_state"])[0]["date"]
            )
            for vuln in vulns
        ]
    )
    if min_date:
        first_date = min_date
    day_week = first_date.weekday()
    first_day_delta = datetime_utils.get_minus_delta(first_date, days=day_week)
    first_day = datetime.combine(
        first_day_delta, datetime.min.time(), tzinfo=datetime_utils.TZ
    )
    last_day_delta = datetime_utils.get_plus_delta(first_day, days=6)
    last_day = datetime.combine(
        last_day_delta,
        datetime.max.time().replace(microsecond=0),
        tzinfo=datetime_utils.TZ,
    )
    return (
        datetime_utils.get_as_str(first_day),
        datetime_utils.get_as_str(last_day),
    )


async def get_group_indicators(group: str) -> Dict[str, object]:
    context = get_new_context()
    findings = await context.group_findings.load(group)
    (
        last_closing_vuln_days,
        last_closing_vuln,
    ) = await findings_domain.get_last_closed_vulnerability_info(
        context, findings
    )
    (
        max_open_severity,
        max_open_severity_finding,
    ) = await findings_domain.get_max_open_severity(context, findings)

    (
        remediated_over_time,
        remediated_over_thirty_days,
        remediated_over_ninety_days,
    ) = await collect(
        [
            create_register_by_week(context, group),
            create_register_by_week(
                context,
                group,
                datetime.combine(
                    datetime_utils.get_now_minus_delta(days=30),
                    datetime.min.time(),
                ),
            ),
            create_register_by_week(
                context,
                group,
                datetime.combine(
                    datetime_utils.get_now_minus_delta(days=90),
                    datetime.min.time(),
                ),
            ),
        ]
    )

    (
        remediate_critical,
        remediate_high,
        remediate_medium,
        remediate_low,
    ) = await collect(
        [
            groups_domain.get_mean_remediate_severity(context, group, 9, 10),
            groups_domain.get_mean_remediate_severity(context, group, 7, 8.9),
            groups_domain.get_mean_remediate_severity(context, group, 4, 6.9),
            groups_domain.get_mean_remediate_severity(
                context, group, 0.1, 3.9
            ),
        ]
    )
    indicators = {
        "closed_vulnerabilities": (
            await groups_domain.get_closed_vulnerabilities(context, group)
        ),
        "last_closing_date": last_closing_vuln_days,
        "last_closing_vuln_finding": last_closing_vuln.get("finding_id", ""),
        "mean_remediate": await groups_domain.get_mean_remediate(
            context, group
        ),
        "mean_remediate_critical_severity": remediate_critical,
        "mean_remediate_high_severity": remediate_high,
        "mean_remediate_low_severity": remediate_low,
        "mean_remediate_medium_severity": remediate_medium,
        "max_open_severity": max_open_severity,
        "max_open_severity_finding": max_open_severity_finding.get(
            "finding_id", ""
        ),
        "open_findings": await groups_domain.get_open_finding(context, group),
        "open_vulnerabilities": (
            await groups_domain.get_open_vulnerabilities(context, group)
        ),
        "total_treatment": await findings_domain.get_total_treatment(
            context, findings
        ),
        "remediated_over_time": remediated_over_time.vulnerabilities,
        "remediated_over_time_cvssf": (
            remediated_over_time.vulnerabilities_cvssf
        ),
        "remediated_over_time_30": remediated_over_thirty_days.vulnerabilities,
        "remediated_over_time_cvssf_30": (
            remediated_over_thirty_days.vulnerabilities_cvssf
        ),
        "remediated_over_time_90": remediated_over_ninety_days.vulnerabilities,
        "remediated_over_time_cvssf_90": (
            remediated_over_ninety_days.vulnerabilities_cvssf
        ),
    }
    return indicators


def get_status_vulns_by_time_range(
    *,
    vulnerabilities: List[Dict[str, FindingType]],
    vulnerabilities_severity: List[Decimal],
    vulnerabilities_historic_states: List[List[Historic]],
    first_day: str,
    last_day: str,
    min_date: Optional[str] = None,
) -> VulnerabilitiesStatusByTimeRange:
    """Get total closed and found vulnerabilities by time range"""
    vulnerabilities_found = [
        get_found_vulnerabilities(
            vulnerability, historic_state, severity, first_day, last_day
        )
        for vulnerability, historic_state, severity in zip(
            vulnerabilities,
            vulnerabilities_historic_states,
            vulnerabilities_severity,
        )
    ]
    vulnerabilities_closed = [
        get_closed_vulns(historic_state, severity, last_day, min_date)
        for historic_state, severity in zip(
            vulnerabilities_historic_states, vulnerabilities_severity
        )
    ]
    vulnerabilities_accepted = [
        get_accepted_vulns(
            vulnerability, historic_state, severity, first_day, min_date
        )
        for vulnerability, historic_state, severity in zip(
            vulnerabilities,
            vulnerabilities_historic_states,
            vulnerabilities_severity,
        )
    ]
    return VulnerabilitiesStatusByTimeRange(
        found_vulnerabilities=sum(
            [found.vulnerabilities for found in vulnerabilities_found]
        ),
        found_cvssf=Decimal(
            sum([found.cvssf for found in vulnerabilities_found])
        ),
        accepted_vulnerabilities=sum(
            [accepted.vulnerabilities for accepted in vulnerabilities_accepted]
        ),
        accepted_cvssf=Decimal(
            sum([accepted.cvssf for accepted in vulnerabilities_accepted])
        ),
        closed_vulnerabilities=sum(
            [closed.vulnerabilities for closed in vulnerabilities_closed]
        ),
        closed_cvssf=Decimal(
            sum([closed.cvssf for closed in vulnerabilities_closed])
        ),
    )


def get_cssvf(severity: Decimal) -> Decimal:
    return Decimal(pow(Decimal("4.0"), severity - Decimal("4.0"))).quantize(
        Decimal("0.001")
    )


def get_found_vulnerabilities(
    vulnerability: Dict[str, FindingType],
    historic_state: List[Dict[str, str]],
    severity: Decimal,
    first_day: str,
    last_day: str,
) -> VulnerabilityStatusByTimeRange:
    last_state = vulns_utils.get_last_approved_state(vulnerability)

    if (
        last_state
        and first_day <= last_state["date"] <= last_day
        and last_state["state"] == "DELETED"
    ):
        return VulnerabilityStatusByTimeRange(
            vulnerabilities=-1, cvssf=(get_cssvf(severity) * Decimal("-1.0"))
        )
    if first_day <= historic_state[0]["date"] <= last_day:
        return VulnerabilityStatusByTimeRange(
            vulnerabilities=1, cvssf=get_cssvf(severity)
        )
    return VulnerabilityStatusByTimeRange(
        vulnerabilities=0, cvssf=Decimal("0.0")
    )


async def update_group_indicators(group_name: str) -> None:
    payload_data = {"group_name": group_name}
    indicators = await get_group_indicators(group_name)
    try:
        response = await groups_domain.update(group_name, indicators)
        if not response:
            msg = "Error: An error ocurred updating indicators in the database"
            LOGGER.error(msg, extra={"extra": payload_data})
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": payload_data})


async def update_indicators() -> None:
    """Update in dynamo indicators."""
    groups = await groups_domain.get_active_groups()
    await collect(map(update_group_indicators, groups), workers=32)


async def main() -> None:
    await update_indicators()
