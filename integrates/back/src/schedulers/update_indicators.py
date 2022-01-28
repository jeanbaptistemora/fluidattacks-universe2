# pylint: disable=too-many-lines
from aioextensions import (
    collect,
)
from botocore.exceptions import (
    ClientError,
)
from calendar import (
    monthrange,
)
from collections import (
    OrderedDict,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
)
from decimal import (
    Decimal,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from findings import (
    domain as findings_domain,
)
from findings.domain.core import (
    get_severity_score,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
    vulnerabilities as vulns_utils,
)
from pandas import (
    Timestamp,
)
from settings import (
    LOGGING,
)
from time import (
    strptime,
)
from typing import (
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
LOGGER_CONSOLE = logging.getLogger("console")


class VulnerabilityStatusByTimeRange(NamedTuple):
    vulnerabilities: int
    cvssf: Decimal


class VulnerabilitiesStatusByTimeRange(NamedTuple):
    accepted_vulnerabilities: int
    closed_vulnerabilities: int
    found_vulnerabilities: int
    open_vulnerabilities: int
    accepted_cvssf: Decimal
    closed_cvssf: Decimal
    found_cvssf: Decimal
    open_cvssf: Decimal


class RegisterByTime(NamedTuple):
    vulnerabilities: List[List[Dict[str, Union[str, Decimal]]]]
    vulnerabilities_cvssf: List[List[Dict[str, Union[str, Decimal]]]]
    exposed_cvssf: List[List[Dict[str, Union[str, Decimal]]]]
    vulnerabilities_yearly: List[List[Dict[str, Union[str, Decimal]]]]
    vulnerabilities_cvssf_yearly: List[List[Dict[str, Union[str, Decimal]]]]
    exposed_cvssf_yearly: List[List[Dict[str, Union[str, Decimal]]]]


class CvssfExposureByTimeRange(NamedTuple):
    low: Decimal
    medium: Decimal
    high: Decimal
    critical: Decimal


def create_data_format_chart(
    all_registers: Dict[str, Dict[str, Decimal]]
) -> List[List[Dict[str, Union[str, Decimal]]]]:
    result_data = []
    plot_points: Dict[str, List[Dict[str, Union[str, Decimal]]]] = {
        "found": [],
        "closed": [],
        "accepted": [],
        "assumed_closed": [],
        "opened": [],
    }
    for week, dict_status in list(all_registers.items()):
        for key, value in plot_points.items():
            value.append({"x": week, "y": dict_status[key]})
    for _, value in plot_points.items():
        result_data.append(value)
    return result_data


def format_exposed_chart(
    all_registers: Dict[str, Dict[str, Decimal]]
) -> List[List[Dict[str, Union[str, Decimal]]]]:
    result_data = []
    plot_points: Dict[str, List[Dict[str, Union[str, Decimal]]]] = {
        "low": [],
        "medium": [],
        "high": [],
        "critical": [],
    }
    for week, dict_status in list(all_registers.items()):
        for key, value in plot_points.items():
            value.append({"x": week, "y": dict_status[key]})
    for key, value in plot_points.items():
        result_data.append(value)
    return result_data


def translate_date_last(date_str: str) -> datetime:
    parts = date_str.replace(",", "").replace("- ", "").split(" ")

    if len(parts) == 6:
        date_year, date_month, date_day = parts[5], parts[3], parts[4]
    elif len(parts) == 5:
        date_year, date_month, date_day = parts[4], parts[2], parts[3]
    elif len(parts) == 4:
        date_year, date_month, date_day = parts[3], parts[0], parts[2]
    else:
        raise ValueError(f"Unexpected number of parts: {parts}")

    return datetime(
        int(date_year), strptime(date_month, "%b").tm_mon, int(date_day)
    )


def get_yearly(x_date: str) -> str:
    data_date = translate_date_last(x_date)
    yearly_day = Timestamp(data_date).to_period("Y").end_time.date()

    if yearly_day < datetime.now().date():
        return datetime.combine(yearly_day, datetime.min.time()).strftime(
            "%Y - %m - %d"
        )

    return datetime.combine(
        datetime.now(),
        datetime.min.time(),
    ).strftime("%Y - %m - %d")


def format_data_chart_yearly(
    all_registers: Dict[str, Dict[str, Decimal]]
) -> List[List[Dict[str, Union[str, Decimal]]]]:
    result_data = []
    plot_points: Dict[str, List[Dict[str, Union[str, Decimal]]]] = {
        "found": [],
        "closed": [],
        "accepted": [],
        "assumed_closed": [],
        "opened": [],
    }
    for week, dict_status in list(all_registers.items()):
        for key, value in plot_points.items():
            value.append({"x": get_yearly(week), "y": dict_status[key]})
    for _, value in plot_points.items():
        result_data.append(list({data["x"]: data for data in value}.values()))
    return result_data


def format_exposed_chart_yearly(
    all_registers: Dict[str, Dict[str, Decimal]]
) -> List[List[Dict[str, Union[str, Decimal]]]]:
    result_data = []
    plot_points: Dict[str, List[Dict[str, Union[str, Decimal]]]] = {
        "low": [],
        "medium": [],
        "high": [],
        "critical": [],
    }
    for week, dict_status in list(all_registers.items()):
        for key, value in plot_points.items():
            value.append({"x": get_yearly(week), "y": dict_status[key]})
    for key, value in plot_points.items():
        result_data.append(list({data["x"]: data for data in value}.values()))
    return result_data


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    max_attempts=10,
    sleep_seconds=5,
)
async def create_register_by_week(  # pylint: disable=too-many-locals
    loaders: Dataloaders, group: str, min_date: Optional[datetime] = None
) -> RegisterByTime:
    """Create weekly vulnerabilities registry by group"""
    found: int = 0
    accepted: int = 0
    closed: int = 0
    exposed_cvssf: Decimal = Decimal(0.0)
    found_cvssf = Decimal(0.0)
    all_registers = OrderedDict()
    all_registers_cvsff = OrderedDict()
    all_registers_exposed_cvsff = OrderedDict()

    findings: Tuple[Finding, ...] = await loaders.group_findings.load(group)
    vulns = await loaders.finding_vulns_nzr_typed.load_many_chained(
        [finding.id for finding in findings]
    )
    findings_severity: Dict[str, Decimal] = {
        finding.id: get_severity_score(finding.severity)
        for finding in findings
    }
    vulnerabilities_severity = [
        findings_severity[vulnerability.finding_id] for vulnerability in vulns
    ]
    historic_states = await loaders.vulnerability_historic_state.load_many(
        [vuln.id for vuln in vulns]
    )
    historic_treatments = (
        await loaders.vulnerability_historic_treatment.load_many(
            [vuln.id for vuln in vulns]
        )
    )

    if vulns:
        first_day, last_day = get_first_week_dates(vulns, min_date)
        first_day_last_week = get_date_last_vulns(vulns)
        while first_day <= first_day_last_week:
            result_vulns_by_week: VulnerabilitiesStatusByTimeRange = (
                get_status_vulns_by_time_range(
                    vulnerabilities=vulns,
                    vulnerabilities_severity=vulnerabilities_severity,
                    vulnerabilities_historic_states=historic_states,
                    vulnerabilities_historic_treatments=historic_treatments,
                    first_day=first_day,
                    last_day=last_day,
                    min_date=datetime_utils.get_as_str(min_date)
                    if min_date
                    else None,
                )
            )
            result_cvssf_by_week: CvssfExposureByTimeRange = (
                get_exposed_cvssf_by_time_range(
                    vulnerabilities_severity=vulnerabilities_severity,
                    vulnerabilities_historic_states=historic_states,
                    last_day=last_day,
                )
            )
            found += result_vulns_by_week.found_vulnerabilities
            found_cvssf += result_vulns_by_week.found_cvssf
            week_dates = create_weekly_date(first_day)
            if any(
                [
                    result_vulns_by_week.found_vulnerabilities,
                    accepted != result_vulns_by_week.accepted_vulnerabilities,
                    closed != result_vulns_by_week.closed_vulnerabilities,
                ]
            ):
                all_registers[week_dates] = {
                    "found": Decimal(found),
                    "closed": Decimal(
                        result_vulns_by_week.closed_vulnerabilities
                    ),
                    "accepted": Decimal(
                        result_vulns_by_week.accepted_vulnerabilities
                    ),
                    "assumed_closed": Decimal(
                        result_vulns_by_week.accepted_vulnerabilities
                        + result_vulns_by_week.closed_vulnerabilities
                    ),
                    "opened": Decimal(
                        result_vulns_by_week.open_vulnerabilities
                    ),
                }
                all_registers_cvsff[week_dates] = {
                    "found": found_cvssf.quantize(Decimal("0.1")),
                    "closed": result_vulns_by_week.closed_cvssf.quantize(
                        Decimal("0.1")
                    ),
                    "accepted": result_vulns_by_week.accepted_cvssf.quantize(
                        Decimal("0.1")
                    ),
                    "assumed_closed": (
                        result_vulns_by_week.accepted_cvssf
                        + result_vulns_by_week.closed_cvssf
                    ).quantize(Decimal("0.1")),
                    "opened": result_vulns_by_week.open_cvssf.quantize(
                        Decimal("0.1")
                    ),
                }
            if exposed_cvssf != (
                result_cvssf_by_week.low
                + result_cvssf_by_week.medium
                + result_cvssf_by_week.high
                + result_cvssf_by_week.critical
            ):
                all_registers_exposed_cvsff[week_dates] = {
                    "low": result_cvssf_by_week.low.quantize(Decimal("0.1")),
                    "medium": result_cvssf_by_week.medium.quantize(
                        Decimal("0.1")
                    ),
                    "high": result_cvssf_by_week.high.quantize(Decimal("0.1")),
                    "critical": result_cvssf_by_week.critical.quantize(
                        Decimal("0.1")
                    ),
                }

            exposed_cvssf = (
                result_cvssf_by_week.low
                + result_cvssf_by_week.medium
                + result_cvssf_by_week.high
                + result_cvssf_by_week.critical
            )
            accepted = result_vulns_by_week.accepted_vulnerabilities
            closed = result_vulns_by_week.closed_vulnerabilities
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

    return RegisterByTime(
        vulnerabilities=create_data_format_chart(all_registers),
        vulnerabilities_cvssf=create_data_format_chart(all_registers_cvsff),
        exposed_cvssf=format_exposed_chart(all_registers_exposed_cvsff),
        vulnerabilities_yearly=[],
        vulnerabilities_cvssf_yearly=[],
        exposed_cvssf_yearly=[],
    )


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    max_attempts=10,
    sleep_seconds=5,
)
async def create_register_by_month(  # pylint: disable=too-many-locals
    *, loaders: Dataloaders, group: str
) -> RegisterByTime:
    found: int = 0
    accepted: int = 0
    closed: int = 0
    exposed_cvssf: Decimal = Decimal(0.0)
    found_cvssf = Decimal(0.0)
    all_registers = OrderedDict()
    all_registers_cvsff = OrderedDict()
    all_registers_exposed_cvsff = OrderedDict()

    findings: Tuple[Finding, ...] = await loaders.group_findings.load(group)
    vulns_nzr = await loaders.finding_vulns_nzr_typed.load_many_chained(
        [finding.id for finding in findings]
    )
    findings_severity: Dict[str, Decimal] = {
        finding.id: get_severity_score(finding.severity)
        for finding in findings
    }
    vulnerabilities_severity = [
        findings_severity[vuln.finding_id] for vuln in vulns_nzr
    ]
    historic_states = await loaders.vulnerability_historic_state.load_many(
        [vuln.id for vuln in vulns_nzr]
    )
    historic_treatments = (
        await loaders.vulnerability_historic_treatment.load_many(
            [vuln.id for vuln in vulns_nzr]
        )
    )

    if vulns_nzr:
        first_day, last_day = get_first_dates(historic_states)
        first_day_last_month = get_last_vulnerabilities_date(vulns_nzr)
        while first_day <= first_day_last_month:
            result_vulns_by_month: VulnerabilitiesStatusByTimeRange = (
                get_status_vulns_by_time_range(
                    vulnerabilities=vulns_nzr,
                    vulnerabilities_severity=vulnerabilities_severity,
                    vulnerabilities_historic_states=historic_states,
                    vulnerabilities_historic_treatments=historic_treatments,
                    first_day=first_day,
                    last_day=last_day,
                    min_date=None,
                )
            )
            result_cvssf_by_month: CvssfExposureByTimeRange = (
                get_exposed_cvssf_by_time_range(
                    vulnerabilities_severity=vulnerabilities_severity,
                    vulnerabilities_historic_states=historic_states,
                    last_day=last_day,
                )
            )
            found += result_vulns_by_month.found_vulnerabilities
            found_cvssf += result_vulns_by_month.found_cvssf
            month_dates = create_date(first_day)
            if any(
                [
                    result_vulns_by_month.found_vulnerabilities,
                    accepted != result_vulns_by_month.accepted_vulnerabilities,
                    closed != result_vulns_by_month.closed_vulnerabilities,
                ]
            ):
                all_registers[month_dates] = {
                    "found": Decimal(found),
                    "closed": Decimal(
                        result_vulns_by_month.closed_vulnerabilities
                    ),
                    "accepted": Decimal(
                        result_vulns_by_month.accepted_vulnerabilities
                    ),
                    "assumed_closed": Decimal(
                        result_vulns_by_month.accepted_vulnerabilities
                        + result_vulns_by_month.closed_vulnerabilities
                    ),
                    "opened": Decimal(
                        result_vulns_by_month.open_vulnerabilities
                    ),
                }
                all_registers_cvsff[month_dates] = {
                    "found": found_cvssf.quantize(Decimal("0.1")),
                    "closed": result_vulns_by_month.closed_cvssf.quantize(
                        Decimal("0.1")
                    ),
                    "accepted": result_vulns_by_month.accepted_cvssf.quantize(
                        Decimal("0.1")
                    ),
                    "assumed_closed": (
                        result_vulns_by_month.accepted_cvssf
                        + result_vulns_by_month.closed_cvssf
                    ).quantize(Decimal("0.1")),
                    "opened": result_vulns_by_month.open_cvssf.quantize(
                        Decimal("0.1")
                    ),
                }

            if exposed_cvssf != (
                result_cvssf_by_month.low
                + result_cvssf_by_month.medium
                + result_cvssf_by_month.high
                + result_cvssf_by_month.critical
            ):
                all_registers_exposed_cvsff[month_dates] = {
                    "low": result_cvssf_by_month.low.quantize(Decimal("0.1")),
                    "medium": result_cvssf_by_month.medium.quantize(
                        Decimal("0.1")
                    ),
                    "high": result_cvssf_by_month.high.quantize(
                        Decimal("0.1")
                    ),
                    "critical": result_cvssf_by_month.critical.quantize(
                        Decimal("0.1")
                    ),
                }

            exposed_cvssf = (
                result_cvssf_by_month.low
                + result_cvssf_by_month.medium
                + result_cvssf_by_month.high
                + result_cvssf_by_month.critical
            )

            accepted = result_vulns_by_month.accepted_vulnerabilities
            closed = result_vulns_by_month.closed_vulnerabilities
            first_day_ = datetime_utils.get_from_str(first_day)
            first_day = datetime_utils.get_as_str(
                datetime_utils.get_plus_delta(
                    first_day_,
                    days=monthrange(
                        int(first_day_.strftime("%Y")),
                        int(first_day_.strftime("%m")),
                    )[1],
                )
            )
            last_day_ = datetime_utils.get_from_str(last_day)
            last_day_one = datetime_utils.get_plus_delta(last_day_, days=1)
            last_day = datetime_utils.get_as_str(
                datetime_utils.get_plus_delta(
                    last_day_,
                    days=monthrange(
                        int(last_day_one.strftime("%Y")),
                        int(last_day_one.strftime("%m")),
                    )[1],
                )
            )

    return RegisterByTime(
        vulnerabilities=create_data_format_chart(all_registers),
        vulnerabilities_cvssf=create_data_format_chart(all_registers_cvsff),
        exposed_cvssf=format_exposed_chart(all_registers_exposed_cvsff),
        vulnerabilities_yearly=format_data_chart_yearly(all_registers),
        vulnerabilities_cvssf_yearly=format_data_chart_yearly(
            all_registers_cvsff
        ),
        exposed_cvssf_yearly=format_exposed_chart_yearly(
            all_registers_exposed_cvsff
        ),
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


def create_date(first_date: str) -> str:
    first_date_ = datetime_utils.get_from_str(first_date)
    month_days: int = monthrange(
        int(first_date_.strftime("%Y")), int(first_date_.strftime("%m"))
    )[1]
    begin = datetime_utils.get_minus_delta(
        first_date_, days=(int(first_date_.strftime("%d")) - 1) % month_days
    )
    end = datetime_utils.get_plus_delta(begin, days=month_days - 1)
    if begin.year != end.year:
        date = "{0:%b} {0.day}, {0.year} - {1:%b} {1.day}, {1.year}"
    elif begin.month != end.month:
        date = "{0:%b} {0.day} - {1:%b} {1.day}, {1.year}"
    else:
        date = "{0:%b} {0.day} - {1.day}, {1.year}"
    return date.format(begin, end)


def get_accepted_vulns(
    historic_state: Tuple[VulnerabilityState, ...],
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
    severity: Decimal,
    last_day: str,
    min_date: Optional[str] = None,
) -> VulnerabilityStatusByTimeRange:
    accepted_treatments = {
        VulnerabilityTreatmentStatus.ACCEPTED,
        VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
    }
    treatments = tuple(
        treatment
        for treatment in historic_treatment
        if datetime.fromisoformat(treatment.modified_date)
        <= datetime_utils.get_from_str(last_day)
    )
    if treatments and treatments[-1].status in accepted_treatments:
        return get_by_time_range(
            historic_state,
            VulnerabilityStateStatus.OPEN,
            severity,
            last_day,
            min_date,
        )
    return VulnerabilityStatusByTimeRange(
        vulnerabilities=0, cvssf=Decimal("0.0")
    )


def get_open_vulnerabilities(
    *,
    historic_state: Tuple[VulnerabilityState, ...],
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
    severity: Decimal,
    last_day: str,
    min_date: Optional[str] = None,
) -> VulnerabilityStatusByTimeRange:
    accepted_treatments = {
        VulnerabilityTreatmentStatus.ACCEPTED,
        VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
    }
    treatments = tuple(
        treatment
        for treatment in historic_treatment
        if datetime.fromisoformat(treatment.modified_date)
        <= datetime_utils.get_from_str(last_day)
    )
    states = tuple(
        state
        for state in historic_state
        if datetime.fromisoformat(state.modified_date)
        <= datetime_utils.get_from_str(last_day)
    )
    if (
        states
        and datetime.fromisoformat(states[-1].modified_date)
        <= datetime_utils.get_from_str(last_day)
        and states[-1].status == VulnerabilityStateStatus.OPEN
        and not (
            min_date
            and datetime.fromisoformat(historic_state[0].modified_date)
            < datetime_utils.get_from_str(min_date)
        )
    ):
        if treatments and treatments[-1].status in accepted_treatments:
            return VulnerabilityStatusByTimeRange(
                vulnerabilities=0, cvssf=Decimal("0.0")
            )

        return VulnerabilityStatusByTimeRange(
            vulnerabilities=1, cvssf=vulns_utils.get_cvssf(severity)
        )
    return VulnerabilityStatusByTimeRange(
        vulnerabilities=0, cvssf=Decimal("0.0")
    )


def get_by_time_range(
    historic_state: Tuple[VulnerabilityState, ...],
    status: VulnerabilityStateStatus,
    severity: Decimal,
    last_day: str,
    min_date: Optional[str] = None,
) -> VulnerabilityStatusByTimeRange:
    states = tuple(
        state
        for state in historic_state
        if datetime.fromisoformat(state.modified_date)
        <= datetime_utils.get_from_str(last_day)
    )
    if (
        states
        and datetime.fromisoformat(states[-1].modified_date)
        <= datetime_utils.get_from_str(last_day)
        and states[-1].status == status
        and not (
            min_date
            and datetime.fromisoformat(historic_state[0].modified_date)
            < datetime_utils.get_from_str(min_date)
        )
    ):
        return VulnerabilityStatusByTimeRange(
            vulnerabilities=1, cvssf=vulns_utils.get_cvssf(severity)
        )
    return VulnerabilityStatusByTimeRange(
        vulnerabilities=0, cvssf=Decimal("0.0")
    )


def get_date_last_vulns(vulns: Tuple[Vulnerability, ...]) -> str:
    """Get date of the last vulnerabilities"""
    last_date = max(
        [datetime.fromisoformat(vuln.state.modified_date) for vuln in vulns]
    )
    day_week = last_date.weekday()
    first_day = datetime_utils.get_as_str(
        datetime_utils.get_minus_delta(last_date, days=day_week)
    )
    return first_day


def get_last_vulnerabilities_date(
    vulns: Tuple[Vulnerability, ...],
) -> str:
    last_date = max(
        [datetime.fromisoformat(vuln.state.modified_date) for vuln in vulns]
    )
    day_month: int = int(last_date.strftime("%d"))
    first_day_delta = datetime_utils.get_minus_delta(
        last_date, days=day_month - 1
    )
    first_day = datetime.combine(
        first_day_delta, datetime.min.time(), tzinfo=datetime_utils.TZ
    )

    return datetime_utils.get_as_str(first_day)


def get_first_week_dates(
    vulns: Tuple[Vulnerability, ...],
    min_date: Optional[datetime] = None,
) -> Tuple[str, str]:
    """Get first week vulnerabilities."""
    first_date = min(
        datetime.fromisoformat(
            vuln.unreliable_indicators.unreliable_report_date
        )
        for vuln in vulns
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


def get_first_dates(
    historic_states: Tuple[Tuple[VulnerabilityState, ...], ...]
) -> Tuple[str, str]:
    first_date = min(
        [
            datetime.fromisoformat(historic[0].modified_date)
            for historic in historic_states
        ]
    )
    day_month: int = int(first_date.strftime("%d"))
    first_day_delta = datetime_utils.get_minus_delta(
        first_date, days=day_month - 1
    )
    first_day = datetime.combine(
        first_day_delta, datetime.min.time(), tzinfo=datetime_utils.TZ
    )
    last_day_delta = datetime_utils.get_plus_delta(
        first_day,
        days=monthrange(
            int(first_date.strftime("%Y")), int(first_date.strftime("%m"))
        )[1]
        - 1,
    )
    last_day = datetime.combine(
        last_day_delta,
        datetime.max.time().replace(microsecond=0),
        tzinfo=datetime_utils.TZ,
    )

    return (
        datetime_utils.get_as_str(first_day),
        datetime_utils.get_as_str(last_day),
    )


async def _get_group_indicators(
    group: str, loaders: Dataloaders, findings: Tuple[Finding, ...]
) -> Dict[str, object]:
    (
        last_closing_vuln_days,
        last_closing_vuln,
    ) = await findings_domain.get_last_closed_vulnerability_info(
        loaders, findings
    )
    (
        max_open_severity,
        max_open_severity_finding,
    ) = await findings_domain.get_max_open_severity(loaders, findings)
    mean_remediate = await groups_domain.get_mean_remediate_severity(
        loaders, group, Decimal("0.0"), Decimal("10.0")
    )
    closed_vulnerabilities = await groups_domain.get_closed_vulnerabilities(
        loaders, group
    )
    open_findings = await groups_domain.get_open_findings(loaders, group)

    return {
        "last_closing_date": last_closing_vuln_days,
        "last_closing_vuln_finding": (
            last_closing_vuln.finding_id if last_closing_vuln else ""
        ),
        "max_open_severity": max_open_severity,
        "max_open_severity_finding": max_open_severity_finding.id
        if max_open_severity_finding
        else "",
        "closed_vulnerabilities": closed_vulnerabilities,
        "mean_remediate": mean_remediate,
        "open_findings": open_findings,
    }


async def get_group_indicators(group: str) -> Dict[str, object]:
    LOGGER_CONSOLE.info(
        "Getting group indicator", extra={"extra": {"group_name": group}}
    )
    loaders: Dataloaders = get_new_context()
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(group)
    _indicators = await _get_group_indicators(group, loaders, findings)
    remediate_critical = await groups_domain.get_mean_remediate_severity(
        loaders, group, Decimal("9.0"), Decimal("10.0")
    )
    remediate_high = await groups_domain.get_mean_remediate_severity(
        loaders, group, Decimal("7.0"), Decimal("8.9")
    )
    remediate_medium = await groups_domain.get_mean_remediate_severity(
        loaders, group, Decimal("4.0"), Decimal("6.9")
    )
    remediate_low = await groups_domain.get_mean_remediate_severity(
        loaders, group, Decimal("0.1"), Decimal("3.9")
    )
    total_treatment = await findings_domain.get_total_treatment(
        loaders, findings
    )
    remediated_over_time = await create_register_by_week(loaders, group)
    remediated_over_thirty_days = await create_register_by_week(
        loaders,
        group,
        datetime.combine(
            datetime_utils.get_now_minus_delta(days=30),
            datetime.min.time(),
        ),
    )
    remediated_over_ninety_days = await create_register_by_week(
        loaders,
        group,
        datetime.combine(
            datetime_utils.get_now_minus_delta(days=90),
            datetime.min.time(),
        ),
    )
    over_time_month: RegisterByTime = await create_register_by_month(
        loaders=loaders, group=group
    )
    indicators = {
        **_indicators,
        "mean_remediate_critical_severity": remediate_critical,
        "mean_remediate_high_severity": remediate_high,
        "mean_remediate_low_severity": remediate_low,
        "mean_remediate_medium_severity": remediate_medium,
        "open_vulnerabilities": (
            await groups_domain.get_open_vulnerabilities(loaders, group)
        ),
        "total_treatment": total_treatment,
        "remediated_over_time": remediated_over_time.vulnerabilities[-18:],
        "remediated_over_time_month": over_time_month.vulnerabilities[-80:],
        "remediated_over_time_year": over_time_month.vulnerabilities_yearly[
            -18:
        ],
        "remediated_over_time_cvssf": (
            remediated_over_time.vulnerabilities_cvssf[-18:]
        ),
        "remediated_over_time_month_cvssf": (
            over_time_month.vulnerabilities_cvssf[-80:]
        ),
        "remediated_over_time_year_cvssf": (
            over_time_month.vulnerabilities_cvssf_yearly[-18:]
        ),
        "exposed_over_time_cvssf": remediated_over_time.exposed_cvssf[-18:],
        "exposed_over_time_month_cvssf": over_time_month.exposed_cvssf[-80:],
        "exposed_over_time_year_cvssf": over_time_month.exposed_cvssf_yearly[
            -18:
        ],
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
    vulnerabilities: Tuple[Vulnerability, ...],
    vulnerabilities_severity: List[Decimal],
    vulnerabilities_historic_states: Tuple[
        Tuple[VulnerabilityState, ...], ...
    ],
    vulnerabilities_historic_treatments: Tuple[
        Tuple[VulnerabilityTreatment, ...], ...
    ],
    first_day: str,
    last_day: str,
    min_date: Optional[str] = None,
) -> VulnerabilitiesStatusByTimeRange:
    """Get total closed and found vulnerabilities by time range."""
    vulnerabilities_found = [
        get_found_vulnerabilities(vulnerability, severity, first_day, last_day)
        for vulnerability, severity in zip(
            vulnerabilities,
            vulnerabilities_severity,
        )
    ]
    vulnerabilities_closed = [
        get_by_time_range(
            historic_state,
            VulnerabilityStateStatus.CLOSED,
            severity,
            last_day,
            min_date,
        )
        for historic_state, severity in zip(
            vulnerabilities_historic_states, vulnerabilities_severity
        )
    ]
    vulnerabilities_accepted = [
        get_accepted_vulns(
            historic_state, historic_treatment, severity, last_day, min_date
        )
        for historic_state, historic_treatment, severity in zip(
            vulnerabilities_historic_states,
            vulnerabilities_historic_treatments,
            vulnerabilities_severity,
        )
    ]
    vulnerabilities_open: Tuple[VulnerabilityStatusByTimeRange, ...] = tuple(
        get_open_vulnerabilities(
            historic_state=historic_state,
            historic_treatment=historic_treatment,
            severity=severity,
            last_day=last_day,
            min_date=min_date,
        )
        for historic_state, historic_treatment, severity in zip(
            vulnerabilities_historic_states,
            vulnerabilities_historic_treatments,
            vulnerabilities_severity,
        )
    )

    return VulnerabilitiesStatusByTimeRange(
        found_vulnerabilities=sum(
            found.vulnerabilities for found in vulnerabilities_found
        ),
        found_cvssf=Decimal(
            sum(found.cvssf for found in vulnerabilities_found)
        ),
        open_vulnerabilities=sum(
            vulnerability_open.vulnerabilities
            for vulnerability_open in vulnerabilities_open
        ),
        open_cvssf=Decimal(
            sum(
                vulnerability_open.cvssf
                for vulnerability_open in vulnerabilities_open
            )
        ),
        accepted_vulnerabilities=sum(
            accepted.vulnerabilities for accepted in vulnerabilities_accepted
        ),
        accepted_cvssf=Decimal(
            sum(accepted.cvssf for accepted in vulnerabilities_accepted)
        ),
        closed_vulnerabilities=sum(
            closed.vulnerabilities for closed in vulnerabilities_closed
        ),
        closed_cvssf=Decimal(
            sum(closed.cvssf for closed in vulnerabilities_closed)
        ),
    )


def get_exposed_cvssf_by_time_range(
    *,
    vulnerabilities_severity: List[Decimal],
    vulnerabilities_historic_states: Tuple[
        Tuple[VulnerabilityState, ...], ...
    ],
    last_day: str,
) -> CvssfExposureByTimeRange:
    exposed_cvssf: List[CvssfExposureByTimeRange] = [
        get_exposed_cvssf(historic_state, severity, last_day)
        for historic_state, severity in zip(
            vulnerabilities_historic_states, vulnerabilities_severity
        )
    ]

    return CvssfExposureByTimeRange(
        low=Decimal(sum(cvssf.low for cvssf in exposed_cvssf)),
        medium=Decimal(sum(cvssf.medium for cvssf in exposed_cvssf)),
        high=Decimal(sum(cvssf.high for cvssf in exposed_cvssf)),
        critical=Decimal(sum(cvssf.critical for cvssf in exposed_cvssf)),
    )


def get_found_vulnerabilities(
    vulnerability: Vulnerability,
    severity: Decimal,
    first_day: str,
    last_day: str,
) -> VulnerabilityStatusByTimeRange:
    found = VulnerabilityStatusByTimeRange(
        vulnerabilities=0, cvssf=Decimal("0.0")
    )
    if (
        first_day <= vulnerability.state.modified_date <= last_day
        and vulnerability.state.status == VulnerabilityStateStatus.DELETED
    ):
        found = VulnerabilityStatusByTimeRange(
            vulnerabilities=found.vulnerabilities - 1,
            cvssf=found.cvssf
            + (vulns_utils.get_cvssf(severity) * Decimal("-1.0")),
        )
    report_date = vulnerability.unreliable_indicators.unreliable_report_date
    if first_day <= report_date <= last_day:
        found = VulnerabilityStatusByTimeRange(
            vulnerabilities=found.vulnerabilities + 1,
            cvssf=found.cvssf + vulns_utils.get_cvssf(severity),
        )

    return found


def get_severity_level(severity: Decimal) -> str:
    if severity <= 3.9:
        return "low"
    if 4 <= severity <= 6.9:
        return "medium"
    if 7 <= severity <= 8.9:
        return "high"

    return "critical"


def get_exposed_cvssf(
    historic_state: Tuple[VulnerabilityState, ...],
    severity: Decimal,
    last_day: str,
) -> CvssfExposureByTimeRange:
    states = tuple(
        state
        for state in historic_state
        if datetime.fromisoformat(state.modified_date)
        <= datetime_utils.get_from_str(last_day)
    )
    cvssf: Decimal = Decimal("0.0")
    severity_level = get_severity_level(severity)

    if (
        states
        and datetime.fromisoformat(states[-1].modified_date)
        <= datetime_utils.get_from_str(last_day)
        and states[-1].status == VulnerabilityStateStatus.OPEN
    ):
        cvssf = vulns_utils.get_cvssf(severity)

    return CvssfExposureByTimeRange(
        low=cvssf if severity_level == "low" else Decimal("0.0"),
        medium=cvssf if severity_level == "medium" else Decimal("0.0"),
        high=cvssf if severity_level == "high" else Decimal("0.0"),
        critical=cvssf if severity_level == "critical" else Decimal("0.0"),
    )


async def update_group_indicators(group_name: str) -> None:
    try:
        payload_data = {"group_name": group_name}
        indicators = await get_group_indicators(group_name)
        response = await groups_domain.update(group_name, indicators)
        if not response:
            msg = "Error: An error ocurred updating indicators in the database"
            LOGGER.error(msg, extra={"extra": payload_data})
    except (ClientError, TypeError, UnavailabilityError) as ex:
        LOGGER.exception(ex, extra={"extra": payload_data})


async def update_indicators() -> None:
    """Update in dynamo indicators."""
    groups = sorted(await groups_domain.get_alive_group_names())
    await collect(map(update_group_indicators, groups), workers=1)


async def main() -> None:
    await update_indicators()
