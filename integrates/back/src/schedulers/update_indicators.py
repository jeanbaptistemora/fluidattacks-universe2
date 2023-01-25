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
from custom_exceptions import (
    GroupNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timezone,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
    GroupUnreliableIndicators,
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
from newutils import (
    datetime as datetime_utils,
    vulnerabilities as vulns_utils,
)
from operator import (
    attrgetter,
)
from organizations import (
    domain as orgs_domain,
)
from pandas import (
    Timestamp,
)
from schedulers.common import (
    error,
    info,
)
from time import (
    strptime,
)
from typing import (
    cast,
    NamedTuple,
    Optional,
    Union,
)
from unreliable_indicators.enums import (
    Entity,
)
from unreliable_indicators.model import (
    ENTITIES,
)
from unreliable_indicators.operations import (
    update_vulnerabilities_unreliable_indicators,
)


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
    vulnerabilities: list[list[dict[str, Union[str, Decimal]]]]
    vulnerabilities_cvssf: list[list[dict[str, Union[str, Decimal]]]]
    exposed_cvssf: list[list[dict[str, Union[str, Decimal]]]]
    vulnerabilities_yearly: list[list[dict[str, Union[str, Decimal]]]]
    vulnerabilities_cvssf_yearly: list[list[dict[str, Union[str, Decimal]]]]
    exposed_cvssf_yearly: list[list[dict[str, Union[str, Decimal]]]]


class CvssfExposureByTimeRange(NamedTuple):
    low: Decimal
    medium: Decimal
    high: Decimal
    critical: Decimal


def create_data_format_chart(
    all_registers: dict[str, dict[str, Decimal]]
) -> list[list[dict[str, Union[str, Decimal]]]]:
    result_data = []
    plot_points: dict[str, list[dict[str, Union[str, Decimal]]]] = {
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
    all_registers: dict[str, dict[str, Decimal]]
) -> list[list[dict[str, Union[str, Decimal]]]]:
    result_data = []
    plot_points: dict[str, list[dict[str, Union[str, Decimal]]]] = {
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
    all_registers: dict[str, dict[str, Decimal]]
) -> list[list[dict[str, Union[str, Decimal]]]]:
    result_data = []
    plot_points: dict[str, list[dict[str, Union[str, Decimal]]]] = {
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
    all_registers: dict[str, dict[str, Decimal]]
) -> list[list[dict[str, Union[str, Decimal]]]]:
    result_data = []
    plot_points: dict[str, list[dict[str, Union[str, Decimal]]]] = {
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


async def update_vulnerabilities_indicators(
    loaders: Dataloaders, group: str
) -> None:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(group)
    vulnerabilities = await loaders.finding_vulnerabilities.load_many_chained(
        [finding.id for finding in findings]
    )
    await update_vulnerabilities_unreliable_indicators(
        [vulnerability.id for vulnerability in vulnerabilities],
        set(cast(dict, ENTITIES[Entity.vulnerability]["attrs"]).keys()),
    )


async def _get_historic_treatment(
    loaders: Dataloaders, vulnerability_id: str
) -> tuple[VulnerabilityTreatment, ...]:
    return await loaders.vulnerability_historic_treatment.load(
        vulnerability_id
    )


async def _get_historic_state(
    loaders: Dataloaders, vulnerability_id: str
) -> tuple[VulnerabilityState, ...]:
    return tuple(
        await loaders.vulnerability_historic_state.load(vulnerability_id)
    )


async def _get_vulnerability_data(
    loaders: Dataloaders, vuln_id: str
) -> tuple[
    tuple[VulnerabilityTreatment, ...],
    tuple[VulnerabilityState, ...],
]:
    historics = await collect(
        (
            _get_historic_treatment(loaders, vuln_id),
            _get_historic_state(loaders, vuln_id),
        )
    )

    return (
        cast(tuple[VulnerabilityTreatment, ...], historics[0]),
        cast(tuple[VulnerabilityState, ...], historics[1]),
    )


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    max_attempts=10,
    sleep_seconds=5,
)
async def create_register_by_week(  # pylint: disable=too-many-locals
    loaders: Dataloaders, group: str, min_date: Optional[datetime] = None
) -> RegisterByTime:
    """Create weekly vulnerabilities registry by group."""
    found: int = 0
    accepted: int = 0
    closed: int = 0
    exposed_cvssf: Decimal = Decimal(0.0)
    found_cvssf = Decimal(0.0)
    all_registers = OrderedDict()
    all_registers_cvsff = OrderedDict()
    all_registers_exposed_cvsff = OrderedDict()

    findings: tuple[Finding, ...] = await loaders.group_findings.load(group)
    vulns = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in findings]
        )
    )
    findings_severity: dict[str, Decimal] = {
        finding.id: get_severity_score(finding.severity)
        for finding in findings
    }
    vulnerabilities_severity = [
        findings_severity[vuln.finding_id] for vuln in vulns
    ]
    vulnerabilities_historics: tuple[
        tuple[
            tuple[VulnerabilityTreatment, ...],
            tuple[VulnerabilityState, ...],
        ],
        ...,
    ] = await collect(
        tuple(
            _get_vulnerability_data(loaders, str(vulnerability.id))
            for vulnerability in vulns
        ),
        workers=48,
    )

    historic_states: tuple[tuple[VulnerabilityState, ...], ...] = tuple(
        historic[1] for historic in vulnerabilities_historics
    )
    historic_treatments: tuple[
        tuple[VulnerabilityTreatment, ...], ...
    ] = tuple(historic[0] for historic in vulnerabilities_historics)

    if vulns:
        first_day, last_day = get_first_week_dates(tuple(vulns), min_date)
        first_day_last_week = get_date_last_vulns(tuple(vulns))
        while first_day <= first_day_last_week:
            result_vulns_by_week: VulnerabilitiesStatusByTimeRange = (
                get_status_vulns_by_time_range(
                    vulnerabilities=tuple(vulns),
                    vulnerabilities_severity=vulnerabilities_severity,
                    vulnerabilities_historic_states=historic_states,
                    vulnerabilities_historic_treatments=historic_treatments,
                    first_day=first_day,
                    last_day=last_day,
                    min_date=min_date,
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
            first_day = datetime_utils.get_plus_delta(first_day, days=7)
            last_day = datetime_utils.get_plus_delta(last_day, days=7)

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
    loaders: Dataloaders, group: str
) -> RegisterByTime:
    found: int = 0
    accepted: int = 0
    closed: int = 0
    exposed_cvssf: Decimal = Decimal(0.0)
    found_cvssf = Decimal(0.0)
    all_registers = OrderedDict()
    all_registers_cvsff = OrderedDict()
    all_registers_exposed_cvsff = OrderedDict()

    findings: tuple[Finding, ...] = await loaders.group_findings.load(group)
    vulns_nzr = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in findings]
        )
    )
    findings_severity: dict[str, Decimal] = {
        finding.id: get_severity_score(finding.severity)
        for finding in findings
    }
    vulnerabilities_severity = [
        findings_severity[vuln.finding_id] for vuln in vulns_nzr
    ]
    vulnerabilities_historics: tuple[
        tuple[
            tuple[VulnerabilityTreatment, ...],
            tuple[VulnerabilityState, ...],
        ],
        ...,
    ] = await collect(
        tuple(
            _get_vulnerability_data(loaders, str(vulnerability.id))
            for vulnerability in vulns_nzr
        ),
        workers=48,
    )

    historic_states: tuple[tuple[VulnerabilityState, ...], ...] = tuple(
        historic[1] for historic in vulnerabilities_historics
    )
    historic_treatments: tuple[
        tuple[VulnerabilityTreatment, ...], ...
    ] = tuple(historic[0] for historic in vulnerabilities_historics)

    if vulns_nzr:
        first_day, last_day = get_first_dates(historic_states)
        first_day_last_month = get_last_vulnerabilities_date(tuple(vulns_nzr))
        while first_day <= first_day_last_month:
            result_vulns_by_month: VulnerabilitiesStatusByTimeRange = (
                get_status_vulns_by_time_range(
                    vulnerabilities=tuple(vulns_nzr),
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
            first_day = datetime_utils.get_plus_delta(
                first_day,
                days=monthrange(
                    int(first_day.strftime("%Y")),
                    int(first_day.strftime("%m")),
                )[1],
            )
            last_day_one = datetime_utils.get_plus_delta(last_day, days=1)
            last_day = datetime_utils.get_plus_delta(
                last_day,
                days=monthrange(
                    int(last_day_one.strftime("%Y")),
                    int(last_day_one.strftime("%m")),
                )[1],
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


def create_weekly_date(first_date: datetime) -> str:
    """Create format weekly date."""
    begin = datetime_utils.get_minus_delta(
        first_date, days=(first_date.isoweekday() - 1) % 7
    )
    end = datetime_utils.get_plus_delta(begin, days=6)
    if begin.year != end.year:
        date = "{0:%b} {0.day}, {0.year} - {1:%b} {1.day}, {1.year}"
    elif begin.month != end.month:
        date = "{0:%b} {0.day} - {1:%b} {1.day}, {1.year}"
    else:
        date = "{0:%b} {0.day} - {1.day}, {1.year}"

    return date.format(begin, end)


def create_date(first_date: datetime) -> str:
    month_days: int = monthrange(
        int(first_date.strftime("%Y")), int(first_date.strftime("%m"))
    )[1]
    begin = datetime_utils.get_minus_delta(
        first_date, days=(int(first_date.strftime("%d")) - 1) % month_days
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
    historic_state: tuple[VulnerabilityState, ...],
    historic_treatment: tuple[VulnerabilityTreatment, ...],
    severity: Decimal,
    last_day: datetime,
    min_date: Optional[datetime] = None,
) -> VulnerabilityStatusByTimeRange:
    accepted_treatments = {
        VulnerabilityTreatmentStatus.ACCEPTED,
        VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
    }
    treatments = tuple(
        treatment
        for treatment in historic_treatment
        if treatment.modified_date.timestamp() <= last_day.timestamp()
    )
    if treatments and treatments[-1].status in accepted_treatments:
        return get_by_time_range(
            historic_state,
            VulnerabilityStateStatus.VULNERABLE,
            severity,
            last_day,
            min_date,
        )

    return VulnerabilityStatusByTimeRange(
        vulnerabilities=0, cvssf=Decimal("0.0")
    )


def get_open_vulnerabilities(
    *,
    historic_state: tuple[VulnerabilityState, ...],
    historic_treatment: tuple[VulnerabilityTreatment, ...],
    severity: Decimal,
    last_day: datetime,
    min_date: Optional[datetime] = None,
) -> VulnerabilityStatusByTimeRange:
    accepted_treatments = {
        VulnerabilityTreatmentStatus.ACCEPTED,
        VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
    }
    treatments = tuple(
        treatment
        for treatment in historic_treatment
        if treatment.modified_date.timestamp() <= last_day.timestamp()
    )
    states = tuple(
        state
        for state in historic_state
        if state.modified_date.timestamp() <= last_day.timestamp()
    )
    if (
        states
        and states[-1].modified_date.timestamp() <= last_day.timestamp()
        and states[-1].status == VulnerabilityStateStatus.VULNERABLE
        and not (
            min_date
            and historic_state[0].modified_date.timestamp()
            < min_date.timestamp()
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
    historic_state: tuple[VulnerabilityState, ...],
    status: VulnerabilityStateStatus,
    severity: Decimal,
    last_day: datetime,
    min_date: Optional[datetime] = None,
) -> VulnerabilityStatusByTimeRange:
    states = tuple(
        state
        for state in historic_state
        if state.modified_date.timestamp() <= last_day.timestamp()
    )
    if (
        states
        and states[-1].modified_date.timestamp() <= last_day.timestamp()
        and states[-1].status == status
        and not (
            min_date
            and historic_state[0].modified_date.timestamp()
            < min_date.timestamp()
        )
    ):
        return VulnerabilityStatusByTimeRange(
            vulnerabilities=1, cvssf=vulns_utils.get_cvssf(severity)
        )

    return VulnerabilityStatusByTimeRange(
        vulnerabilities=0, cvssf=Decimal("0.0")
    )


def get_date_last_vulns(vulns: tuple[Vulnerability, ...]) -> datetime:
    """Get date of the last vulnerabilities."""
    last_date = max(vuln.state.modified_date for vuln in vulns)
    day_week = last_date.weekday()
    first_day = datetime_utils.get_minus_delta(last_date, days=day_week)

    return first_day


def get_last_vulnerabilities_date(
    vulns: tuple[Vulnerability, ...],
) -> datetime:
    last_date = max(vuln.state.modified_date for vuln in vulns)
    day_month: int = int(last_date.strftime("%d"))
    first_day_delta = datetime_utils.get_minus_delta(
        last_date, days=day_month - 1
    )
    first_day = datetime.combine(
        first_day_delta, datetime.min.time()
    ).astimezone(tz=timezone.utc)

    return first_day


def get_first_week_dates(
    vulns: tuple[Vulnerability, ...],
    min_date: Optional[datetime] = None,
) -> tuple[datetime, datetime]:
    """Get first week vulnerabilities."""
    if min_date:
        first_date = min_date
    else:
        first_date = min(vuln.created_date for vuln in vulns)
    day_week = first_date.weekday()
    first_day_delta = datetime_utils.get_minus_delta(first_date, days=day_week)
    first_day = datetime.combine(
        first_day_delta, datetime.min.time()
    ).astimezone(tz=timezone.utc)
    last_day_delta = datetime_utils.get_plus_delta(first_day, days=6)
    last_day = datetime.combine(
        last_day_delta,
        datetime.max.time().replace(microsecond=0),
    ).astimezone(tz=timezone.utc)

    return (first_day, last_day)


def get_first_dates(
    historic_states: tuple[tuple[VulnerabilityState, ...], ...]
) -> tuple[datetime, datetime]:
    first_date = min(historic[0].modified_date for historic in historic_states)
    day_month: int = int(first_date.strftime("%d"))
    first_day_delta = datetime_utils.get_minus_delta(
        first_date, days=day_month - 1
    )
    first_day = datetime.combine(
        first_day_delta, datetime.min.time()
    ).astimezone(tz=timezone.utc)
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
    ).astimezone(tz=timezone.utc)

    return (first_day, last_day)


def get_status_vulns_by_time_range(
    *,
    vulnerabilities: tuple[Vulnerability, ...],
    vulnerabilities_severity: list[Decimal],
    vulnerabilities_historic_states: tuple[
        tuple[VulnerabilityState, ...], ...
    ],
    vulnerabilities_historic_treatments: tuple[
        tuple[VulnerabilityTreatment, ...], ...
    ],
    first_day: datetime,
    last_day: datetime,
    min_date: Optional[datetime] = None,
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
            VulnerabilityStateStatus.SAFE,
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
    vulnerabilities_open: tuple[VulnerabilityStatusByTimeRange, ...] = tuple(
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
    vulnerabilities_severity: list[Decimal],
    vulnerabilities_historic_states: tuple[
        tuple[VulnerabilityState, ...], ...
    ],
    last_day: datetime,
) -> CvssfExposureByTimeRange:
    exposed_cvssf: list[CvssfExposureByTimeRange] = [
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
    first_day: datetime,
    last_day: datetime,
) -> VulnerabilityStatusByTimeRange:
    found = VulnerabilityStatusByTimeRange(
        vulnerabilities=0, cvssf=Decimal("0.0")
    )
    if (
        first_day.timestamp()
        <= vulnerability.state.modified_date.timestamp()
        <= last_day.timestamp()
        and vulnerability.state.status
        in {
            VulnerabilityStateStatus.DELETED,
            VulnerabilityStateStatus.MASKED,
        }
    ):
        found = VulnerabilityStatusByTimeRange(
            vulnerabilities=found.vulnerabilities - 1,
            cvssf=found.cvssf
            + (vulns_utils.get_cvssf(severity) * Decimal("-1.0")),
        )
    if first_day <= vulnerability.created_date <= last_day:
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
    historic_state: tuple[VulnerabilityState, ...],
    severity: Decimal,
    last_day: datetime,
) -> CvssfExposureByTimeRange:
    states = tuple(
        state
        for state in historic_state
        if state.modified_date.timestamp() <= last_day.timestamp()
    )
    cvssf: Decimal = Decimal("0.0")
    severity_level = get_severity_level(severity)

    if (
        states
        and states[-1].modified_date.timestamp() <= last_day.timestamp()
        and states[-1].status == VulnerabilityStateStatus.VULNERABLE
    ):
        cvssf = vulns_utils.get_cvssf(severity)

    return CvssfExposureByTimeRange(
        low=cvssf if severity_level == "low" else Decimal("0.0"),
        medium=cvssf if severity_level == "medium" else Decimal("0.0"),
        high=cvssf if severity_level == "high" else Decimal("0.0"),
        critical=cvssf if severity_level == "critical" else Decimal("0.0"),
    )


async def get_group_indicators(  # pylint: disable=too-many-locals
    group: Group,
) -> GroupUnreliableIndicators:
    loaders: Dataloaders = get_new_context()
    current_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group.name)
    )
    findings = await loaders.group_findings.load(group.name)

    (
        last_closed_vulnerability_days,
        last_closed_vulnerability,
    ) = await findings_domain.get_last_closed_vulnerability_info(
        loaders, findings
    )
    (
        max_open_severity,
        max_open_severity_finding,
    ) = await findings_domain.get_max_open_severity(loaders, findings)
    max_severity = await groups_domain.get_max_severity(loaders, group.name)
    mean_remediate = await groups_domain.get_mean_remediate_severity(
        loaders, group.name, Decimal("0.0"), Decimal("10.0")
    )
    closed_vulnerabilities = await groups_domain.get_closed_vulnerabilities(
        loaders, group.name
    )
    open_findings = await groups_domain.get_open_findings(loaders, group.name)
    open_vulnerabilities = await groups_domain.get_open_vulnerabilities(
        loaders, group.name
    )

    remediate_critical = await groups_domain.get_mean_remediate_severity(
        loaders, group.name, Decimal("9.0"), Decimal("10.0")
    )
    remediate_high = await groups_domain.get_mean_remediate_severity(
        loaders, group.name, Decimal("7.0"), Decimal("8.9")
    )
    remediate_medium = await groups_domain.get_mean_remediate_severity(
        loaders, group.name, Decimal("4.0"), Decimal("6.9")
    )
    remediate_low = await groups_domain.get_mean_remediate_severity(
        loaders, group.name, Decimal("0.1"), Decimal("3.9")
    )
    remediated_over_time = await create_register_by_week(loaders, group.name)
    remediated_over_thirty_days = await create_register_by_week(
        loaders,
        group.name,
        datetime.combine(
            datetime_utils.get_now_minus_delta(days=30),
            datetime.min.time(),
        ).astimezone(tz=timezone.utc),
    )
    remediated_over_ninety_days = await create_register_by_week(
        loaders,
        group.name,
        datetime.combine(
            datetime_utils.get_now_minus_delta(days=90),
            datetime.min.time(),
        ).astimezone(tz=timezone.utc),
    )
    over_time_month: RegisterByTime = await create_register_by_month(
        loaders=loaders, group=group.name
    )
    treatment_summary = await groups_domain.get_treatment_summary(
        loaders, group.name
    )
    await update_vulnerabilities_indicators(loaders, group.name)

    return GroupUnreliableIndicators(
        closed_vulnerabilities=closed_vulnerabilities,
        code_languages=current_indicators.code_languages,
        last_closed_vulnerability_days=last_closed_vulnerability_days,
        last_closed_vulnerability_finding=(
            last_closed_vulnerability.finding_id
            if last_closed_vulnerability
            else ""
        ),
        max_open_severity=max_open_severity,
        max_open_severity_finding=max_open_severity_finding.id
        if max_open_severity_finding
        else "",
        max_severity=max_severity,
        mean_remediate=mean_remediate,
        open_findings=open_findings,
        mean_remediate_critical_severity=remediate_critical,
        mean_remediate_high_severity=remediate_high,
        mean_remediate_low_severity=remediate_low,
        mean_remediate_medium_severity=remediate_medium,
        open_vulnerabilities=open_vulnerabilities,
        remediated_over_time=remediated_over_time.vulnerabilities[-18:],
        remediated_over_time_month=over_time_month.vulnerabilities[-80:],
        remediated_over_time_year=over_time_month.vulnerabilities_yearly[-18:],
        remediated_over_time_cvssf=(
            remediated_over_time.vulnerabilities_cvssf[-18:]
        ),
        remediated_over_time_month_cvssf=(
            over_time_month.vulnerabilities_cvssf[-80:]
        ),
        remediated_over_time_year_cvssf=(
            over_time_month.vulnerabilities_cvssf_yearly[-18:]
        ),
        exposed_over_time_cvssf=remediated_over_time.exposed_cvssf[-18:],
        exposed_over_time_month_cvssf=over_time_month.exposed_cvssf[-80:],
        exposed_over_time_year_cvssf=over_time_month.exposed_cvssf_yearly[
            -18:
        ],
        remediated_over_time_30=remediated_over_thirty_days.vulnerabilities,
        remediated_over_time_cvssf_30=(
            remediated_over_thirty_days.vulnerabilities_cvssf
        ),
        remediated_over_time_90=remediated_over_ninety_days.vulnerabilities,
        remediated_over_time_cvssf_90=(
            remediated_over_ninety_days.vulnerabilities_cvssf
        ),
        treatment_summary=treatment_summary,
        unfulfilled_standards=current_indicators.unfulfilled_standards,
    )


async def update_group_indicators(group: Group, progress: float) -> None:
    try:
        indicators = await get_group_indicators(group)
        await groups_domain.update_indicators(
            group_name=group.name, indicators=indicators
        )
        info(
            "Group indicators processed",
            extra={"group_name": group.name, "progress": round(progress, 2)},
        )
    except (ClientError, GroupNotFound, TypeError, UnavailabilityError) as ex:
        msg = "Error: An error ocurred updating indicators in the database"
        error(msg, extra={"group_name": group.name, "ex": ex})


async def update_indicators() -> None:
    """Update in dynamo indicators."""
    groups = await orgs_domain.get_all_active_groups(loaders=get_new_context())
    groups_sorted_by_name = sorted(groups, key=attrgetter("name"))
    len_groups_sorted_by_name = len(groups_sorted_by_name)
    await collect(
        tuple(
            update_group_indicators(
                group=group,
                progress=count / len_groups_sorted_by_name,
            )
            for count, group in enumerate(groups_sorted_by_name)
        ),
        workers=1,
    )


async def main() -> None:
    await update_indicators()
