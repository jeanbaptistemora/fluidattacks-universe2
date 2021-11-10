from . import (
    datetime as datetime_utils,
)
from custom_exceptions import (
    AlreadyRequested,
    AlreadyZeroRiskRequested,
    InvalidJustificationMaxLength,
    InvalidRange,
    NotVerificationRequested,
    NotZeroRiskRequested,
    VulnAlreadyClosed,
)
from custom_types import (
    Action,
    Finding as FindingType,
    Historic as HistoricType,
    Vulnerability as VulnerabilityType,
)
from datetime import (
    date as datetype,
    datetime,
)
from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.findings.types import (
    FindingVerification,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
import html
import itertools
import logging
from operator import (
    itemgetter,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    cast,
    Counter,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Union,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
Treatments = NamedTuple(
    "Treatments",
    [
        ("ACCEPTED", int),
        ("ACCEPTED_UNDEFINED", int),
        ("IN_PROGRESS", int),
        ("NEW", int),
    ],
)


def as_range(iterable: Iterable[Any]) -> str:
    """Convert range into string."""
    my_list = list(iterable)
    range_value = ""
    if len(my_list) > 1:
        range_value = f"{my_list[0]}-{my_list[-1]}"
    else:
        range_value = f"{my_list[0]}"
    return range_value


def is_last_reattack_requested(vuln: VulnerabilityType) -> bool:
    historic_verification: HistoricType = vuln.get("historic_verification")
    if historic_verification:
        last_historic = historic_verification[-1]
        return last_historic.get("status") == "REQUESTED"
    return False


def filter_non_deleted(
    vulnerabilities: List[VulnerabilityType],
) -> List[VulnerabilityType]:
    return [
        vuln
        for vuln in vulnerabilities
        if vuln["historic_state"][-1]["state"] != "DELETED"
    ]


def filter_open_vulns(
    vulnerabilities: List[VulnerabilityType],
) -> List[VulnerabilityType]:
    return [
        vuln
        for vuln in vulnerabilities
        if cast(HistoricType, vuln.get("historic_state", [{}]))[-1].get(
            "state"
        )
        == "open"
    ]


def filter_open_vulns_new(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if vuln.state.status == VulnerabilityStateStatus.OPEN
    )


def filter_closed_vulns(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if vuln.state.status == VulnerabilityStateStatus.CLOSED
    )


def filter_confirmed_zero_risk(
    vulnerabilities: List[Dict[str, FindingType]],
) -> List[Dict[str, FindingType]]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if cast(HistoricType, vulnerability.get("historic_zero_risk", [{}]))[
            -1
        ].get("status", "")
        == "CONFIRMED"
    ]


def filter_non_confirmed_zero_risk(
    vulnerabilities: List[VulnerabilityType],
) -> List[VulnerabilityType]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if cast(HistoricType, vulnerability.get("historic_zero_risk", [{}]))[
            -1
        ].get("status", "")
        != "CONFIRMED"
    ]


def filter_non_confirmed_zero_risk_new(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vulnerability
        for vulnerability in vulnerabilities
        if not vulnerability.zero_risk
        or vulnerability.zero_risk.status
        != VulnerabilityZeroRiskStatus.CONFIRMED
    )


def filter_requested_zero_risk(
    vulnerabilities: List[Dict[str, FindingType]],
) -> List[Dict[str, FindingType]]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if cast(HistoricType, vulnerability.get("historic_zero_risk", [{}]))[
            -1
        ].get("status", "")
        == "REQUESTED"
    ]


def filter_non_requested_zero_risk(
    vulnerabilities: List[VulnerabilityType],
) -> List[VulnerabilityType]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if cast(HistoricType, vulnerability.get("historic_zero_risk", [{}]))[
            -1
        ].get("status", "")
        != "REQUESTED"
    ]


def filter_remediated(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability.verification
        and vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    )


def filter_historic_date(
    historic: HistoricType,
    min_date: datetime,
) -> HistoricType:
    """Filter historics since a given date"""
    return [
        entry
        for entry in historic
        if min_date and datetime_utils.get_from_str(entry["date"]) >= min_date
    ]


def format_data(vuln: Dict[str, FindingType]) -> Dict[str, FindingType]:
    vuln["current_state"] = cast(
        List[Dict[str, str]], vuln.get("historic_state", [{}])
    )[-1].get("state")
    return vuln


def format_vulnerabilities(
    vulnerabilities: List[Dict[str, FindingType]]
) -> Dict[str, List[FindingType]]:
    """Format vulnerabilitites."""
    finding: Dict[str, List[FindingType]] = {
        "ports": [],
        "lines": [],
        "inputs": [],
    }
    vulns_types = ["ports", "lines", "inputs"]
    vuln_values = {
        "ports": {
            "where": "host",
            "specific": "port",
        },
        "lines": {"where": "path", "specific": "line"},
        "inputs": {"where": "url", "specific": "field"},
    }
    for vuln in vulnerabilities:
        all_states = cast(
            List[Dict[str, FindingType]], vuln.get("historic_state")
        )
        current_state = all_states[-1].get("state")
        vuln_type = str(vuln.get("vuln_type", ""))
        if vuln_type in vulns_types:
            finding[vuln_type].append(
                {
                    vuln_values[vuln_type]["where"]: (
                        html.unescape(vuln.get("where"))  # type: ignore
                    ),
                    vuln_values[vuln_type]["specific"]: (
                        html.unescape(vuln.get("specific"))  # type: ignore
                    ),
                    "state": str(current_state),
                }
            )
            for attr in ("commit_hash", "repo_nickname"):
                if vuln.get(attr):
                    finding[vuln_type][-1][attr] = vuln[attr]
        else:
            LOGGER.error(
                "Vulnerability does not have the right type",
                extra={
                    "extra": {
                        "vuln_uuid": vuln.get("UUID"),
                        "finding_id": vuln.get("finding_id"),
                    }
                },
            )
    return finding


def format_where(where: str, vulnerabilities: List[Dict[str, str]]) -> str:
    for vuln in vulnerabilities:
        where = f'{where}{vuln.get("where")} ({vuln.get("specific")})\n'
    return where


def get_last_approved_state(vuln: Dict[str, FindingType]) -> Dict[str, str]:
    historic_state = cast(HistoricType, vuln.get("historic_state", [{}]))
    return historic_state[-1]


def get_opening_date(
    historic: Tuple[VulnerabilityState, ...],
    min_date: Optional[datetype] = None,
) -> Optional[datetype]:
    opening_date: Optional[datetype] = None
    open_state = next(
        (
            state
            for state in reversed(historic)
            if state.status == VulnerabilityStateStatus.OPEN
        ),
        None,
    )
    if open_state:
        iso8601utc_date = datetime.fromisoformat(open_state.modified_date)
        opening_date = datetime_utils.get_from_str(
            datetime_utils.get_as_str(iso8601utc_date)
        ).date()
        if min_date and min_date > opening_date:
            opening_date = None
    return opening_date


def get_closing_date(
    vulnerability: Vulnerability,
    min_date: Optional[datetype] = None,
) -> Optional[datetype]:
    closing_date: Optional[datetype] = None
    if vulnerability.state.status == VulnerabilityStateStatus.CLOSED:
        iso8601utc_date = datetime.fromisoformat(
            vulnerability.state.modified_date
        )
        closing_date = datetime_utils.get_from_str(
            datetime_utils.get_as_str(iso8601utc_date)
        ).date()
        if min_date and min_date > closing_date:
            return None
    return closing_date


def get_last_status(vuln: Dict[str, FindingType]) -> str:
    historic_state = cast(HistoricType, vuln.get("historic_state", [{}]))
    return historic_state[-1].get("state", "")


def get_mean_remediate_vulnerabilities_cvssf(
    vulns: Tuple[Vulnerability, ...],
    vulns_historic_state: Tuple[Tuple[VulnerabilityState, ...]],
    finding_cvssf: Dict[str, Decimal],
    min_date: Optional[datetype] = None,
) -> Decimal:
    total_days: Decimal = Decimal("0.0")
    open_vuln_dates = [
        get_opening_date(historic, min_date)
        for historic in vulns_historic_state
    ]
    filtered_open_vuln_dates = [date for date in open_vuln_dates if date]
    closed_vuln_dates: List[Tuple[Optional[datetype], Decimal]] = [
        (
            get_closing_date(vuln, min_date),
            finding_cvssf[vuln.finding_id],
        )
        for vuln, open_vuln in zip(vulns, open_vuln_dates)
        if open_vuln
    ]
    for index, closed_vuln_date in enumerate(closed_vuln_dates):
        if closed_vuln_date[0] is not None:
            total_days += Decimal(
                (closed_vuln_date[0] - filtered_open_vuln_dates[index]).days
                * closed_vuln_date[1]
            )
        else:
            current_day = datetime_utils.get_now().date()
            total_days += Decimal(
                (current_day - filtered_open_vuln_dates[index]).days
                * closed_vuln_date[1]
            )
    total_cvssf: Decimal = Decimal(
        sum(
            [
                finding_cvssf[vuln.finding_id]
                for vuln, open_date in zip(vulns, open_vuln_dates)
                if open_date
            ]
        )
    )
    if total_cvssf:
        mean_vulnerabilities = Decimal(total_days / total_cvssf).quantize(
            Decimal("0.001")
        )
    else:
        mean_vulnerabilities = Decimal(0).quantize(Decimal("0.1"))

    return mean_vulnerabilities


def get_mean_remediate_vulnerabilities(
    vulns: Tuple[Vulnerability, ...],
    vulns_historic_state: Tuple[Tuple[VulnerabilityState, ...]],
    min_date: Optional[datetype] = None,
) -> Decimal:
    """Get mean time to remediate a vulnerability."""
    total_vuln = 0
    total_days = 0
    open_vuln_dates = [
        get_opening_date(historic, min_date)
        for historic in vulns_historic_state
    ]
    filtered_open_vuln_dates = [date for date in open_vuln_dates if date]
    closed_vuln_dates = [
        get_closing_date(vuln, min_date)
        for vuln, open_vuln in zip(vulns, open_vuln_dates)
        if open_vuln
    ]
    for index, closed_vuln_date in enumerate(closed_vuln_dates):
        if closed_vuln_date:
            total_days += int(
                (closed_vuln_date - filtered_open_vuln_dates[index]).days
            )
        else:
            current_day = datetime_utils.get_now().date()
            total_days += int(
                (current_day - filtered_open_vuln_dates[index]).days
            )
    total_vuln = len(filtered_open_vuln_dates)
    if total_vuln:
        mean_vulnerabilities = Decimal(
            round(total_days / float(total_vuln))
        ).quantize(Decimal("0.1"))
    else:
        mean_vulnerabilities = Decimal(0).quantize(Decimal("0.1"))

    return mean_vulnerabilities.to_integral_exact(rounding=ROUND_CEILING)


def get_cvssf(severity: Decimal) -> Decimal:
    return Decimal(pow(Decimal("4.0"), severity - Decimal("4.0"))).quantize(
        Decimal("0.001")
    )


def get_ranges(numberlist: List[int]) -> str:
    """Transform list into ranges."""
    range_str = ",".join(
        as_range(g)
        for _, g in itertools.groupby(
            numberlist,
            key=lambda n, c=itertools.count(): n - next(c),  # type: ignore
        )
    )
    return range_str


def get_reattack_requesters(
    historic_verification: Tuple[FindingVerification, ...],
    vulnerability_ids: Set[str],
) -> List[str]:
    reversed_historic_verification = tuple(reversed(historic_verification))
    users: Set[str] = set()
    for verification in reversed_historic_verification:
        if verification.status == FindingVerificationStatus.REQUESTED and (
            [
                vuln_id
                for vuln_id in verification.vulnerability_ids
                if vuln_id in vulnerability_ids
            ]
        ):
            vulnerability_ids = {
                vuln_id
                for vuln_id in vulnerability_ids
                if vuln_id not in verification.vulnerability_ids
            }
            users.add(verification.modified_by)
        if not vulnerability_ids:
            break
    return list(users)


def get_report_dates(
    historics: Tuple[Tuple[VulnerabilityState, ...]]
) -> Tuple[datetime, ...]:
    """Get report dates for vulnerabilities, given the historic state."""
    return tuple(
        datetime.fromisoformat(historic[0].modified_date)
        for historic in historics
    )


def get_specific(value: Dict[str, str]) -> int:
    """Get specific value."""
    return int(value.get("specific", ""))


def get_treatments(
    vulnerabilities: List[Dict[str, FindingType]]
) -> Treatments:
    treatment_counter = Counter(
        [
            vuln["historic_treatment"][-1]["treatment"]
            for vuln in vulnerabilities
            if vuln["historic_treatment"]
            and vuln["historic_state"][-1]["state"] == "open"
        ]
    )
    return Treatments(
        ACCEPTED=treatment_counter["ACCEPTED"],
        ACCEPTED_UNDEFINED=treatment_counter["ACCEPTED_UNDEFINED"],
        IN_PROGRESS=treatment_counter["IN PROGRESS"],
        NEW=treatment_counter["NEW"],
    )


def group_specific(
    specific: List[Dict[str, str]], vuln_type: str
) -> List[Dict[str, FindingType]]:
    """Group vulnerabilities by its specific field."""
    sorted_specific = sort_vulnerabilities(specific)
    lines = []
    vuln_keys = ["historic_state", "vuln_type", "UUID", "finding_id"]
    for key, group in itertools.groupby(
        sorted_specific,
        key=lambda x: (
            x["where"],
            x["commit_hash"],
        ),
    ):
        vuln_info = list(group)
        if vuln_type == "inputs":
            specific_grouped: List[Union[int, str]] = [
                i.get("specific", "") for i in vuln_info
            ]
            dictlines: Dict[str, FindingType] = {
                "where": key[0],
                "specific": ",".join(cast(List[str], specific_grouped)),
            }
        else:
            specific_grouped = [get_specific(i) for i in vuln_info]
            specific_grouped.sort()
            dictlines = {
                "where": key[0],
                "specific": get_ranges(cast(List[int], specific_grouped)),
                "commit_hash": str(
                    cast(Dict[str, FindingType], vuln_info[0])["commit_hash"]
                )[0:7],
            }
        if vuln_info and all(
            key_vuln in vuln_info[0] for key_vuln in vuln_keys
        ):
            dictlines.update(
                {
                    key_vuln: cast(Dict[str, FindingType], vuln_info[0]).get(
                        key_vuln
                    )
                    for key_vuln in vuln_keys
                }
            )
        else:
            # Vulnerability doesn't have more attributes.
            pass
        lines.append(dictlines)
    return lines


def is_accepted_undefined_vulnerability(
    vulnerability: Dict[str, FindingType]
) -> bool:
    historic_treatment = cast(
        HistoricType, vulnerability["historic_treatment"]
    )
    return (
        historic_treatment[-1]["treatment"] == "ACCEPTED_UNDEFINED"
        and get_last_status(vulnerability) == "open"
    )


def is_accepted_undefined_vulnerability_new(
    vulnerability: Vulnerability,
) -> bool:
    return (
        vulnerability.treatment
        and vulnerability.treatment.status
        == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        and vulnerability.state.status == VulnerabilityStateStatus.OPEN
    )


def is_range(specific: str) -> bool:
    """Validate if a specific field has range value."""
    return "-" in specific


def is_reattack_requested(vuln: Dict[str, FindingType]) -> bool:
    response = False
    historic_verification = vuln.get("historic_verification", [{}])
    if (
        cast(List[Dict[str, str]], historic_verification)[-1].get("status", "")
        == "REQUESTED"
    ):
        response = True
    return response


def is_sequence(specific: str) -> bool:
    """Validate if a specific field has secuence value."""
    return "," in specific


def sort_vulnerabilities(item: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Sort a vulnerability by its where field."""
    sorted_item = sorted(item, key=itemgetter("where"))
    return sorted_item


def range_to_list(range_value: str) -> List[str]:
    """Convert a range value into list."""
    limits = range_value.split("-")
    init_val = int(limits[0])
    end_val = int(limits[1]) + 1
    if end_val <= init_val:
        error_value = f'"values": "{init_val} >= {end_val}"'
        raise InvalidRange(expr=error_value)
    specific_values = list(map(str, list(range(init_val, end_val))))
    return specific_values


def ungroup_specific(specific: str) -> List[str]:
    """Ungroup specific value."""
    values = specific.split(",")
    specific_values = []
    for val in values:
        if is_range(val):
            range_list = range_to_list(val)
            specific_values.extend(range_list)
        else:
            specific_values.append(val)
    return specific_values


def update_treatment_values(updated_values: Dict[str, str]) -> Dict[str, str]:
    if updated_values["treatment"] == "NEW":
        updated_values["acceptance_date"] = ""
    elif updated_values["treatment"] == "ACCEPTED_UNDEFINED":
        updated_values["acceptance_status"] = "SUBMITTED"
        days = [
            datetime_utils.get_now_plus_delta(days=x + 1) for x in range(5)
        ]
        weekend_days = sum(1 for day in days if day.weekday() >= 5)
        updated_values["acceptance_date"] = datetime_utils.get_as_str(
            datetime_utils.get_now_plus_delta(days=5 + weekend_days)
        )
    return updated_values


def get_treatment_from_org_finding_policy(
    *, current_day: str, user_email: str
) -> List[Dict[str, str]]:
    return [
        {
            "treatment": "ACCEPTED_UNDEFINED",
            "justification": "From organization findings policy",
            "user": user_email,
            "date": current_day,
            "treatment_manager": user_email,
            "acceptance_status": "SUBMITTED",
        },
        {
            "treatment": "ACCEPTED_UNDEFINED",
            "justification": "From organization findings policy",
            "user": user_email,
            "date": current_day,
            "treatment_manager": user_email,
            "acceptance_status": "APPROVED",
        },
    ]


async def get_total_treatment_date(
    vulns: List[Dict[str, FindingType]],
    min_date: datetime,
) -> Dict[str, int]:
    """Get the total treatment of all the vulns filtered by date"""
    accepted_vuln: int = 0
    accepted_undefined_submited_vuln: int = 0
    accepted_undefined_approved_vuln: int = 0
    undefined_treatment_vuln: int = 0

    for vuln in vulns:
        filtered_historic_as_str = str(
            filter_historic_date(
                vuln.get("historic_treatment", [{}]), min_date
            )
        )
        # Check if any of these states occurred in the period
        if "'ACCEPTED'" in filtered_historic_as_str:
            accepted_vuln += 1
        if "SUBMITTED" in filtered_historic_as_str:
            accepted_undefined_submited_vuln += 1
        if "APPROVED" in filtered_historic_as_str:
            accepted_undefined_approved_vuln += 1
        if "NEW" in filtered_historic_as_str:
            undefined_treatment_vuln += 1
    return {
        "accepted": accepted_vuln,
        "accepted_undefined_submitted": accepted_undefined_submited_vuln,
        "accepted_undefined_approved": accepted_undefined_approved_vuln,
        "undefined_treatment": undefined_treatment_vuln,
    }


async def get_total_reattacks_stats(
    vulns: List[Dict[str, FindingType]],
    min_date: datetime,
) -> Dict[str, Union[int, str]]:
    """Get the total reattacks of all the vulns"""
    default_date: datetime = datetime_utils.get_from_str(
        datetime_utils.DEFAULT_STR
    )
    reattacks_requested: int = 0
    reattacks_executed: int = 0
    reattacks_executed_total: int = 0  # No filtered by date
    pending_attacks: int = 0
    effective_reattacks: int = 0
    effective_reattacks_total: int = 0  # No filtered by date
    min_requested_date: datetime = default_date
    min_executed_date: datetime = default_date

    for vuln in vulns:
        if vuln.get("last_requested_reattack_date", ""):
            last_requested_reattack_date = datetime_utils.get_from_str(
                vuln.get("last_requested_reattack_date", "")
            )
            # Get oldest reattack request date
            min_requested_date = max(
                min_requested_date, last_requested_reattack_date
            )
            if min_date and last_requested_reattack_date >= min_date:
                reattacks_requested += 1
        if vuln.get("last_reattack_date", ""):
            # Increment totals, no date filtered
            reattacks_executed_total += 1
            if vuln.get("current_state", "") == "closed":
                effective_reattacks_total += 1
            # Get oldest executed reattack date
            last_reattack_date = datetime_utils.get_from_str(
                vuln.get("last_reattack_date", "")
            )
            min_executed_date = max(min_executed_date, last_reattack_date)
            if min_date and last_reattack_date >= min_date:
                reattacks_executed += 1
                if vuln.get("current_state", "") == "closed":
                    effective_reattacks += 1
        if vuln.get("verification", "") == "Requested":
            pending_attacks += 1

    return {
        "effective_reattacks": effective_reattacks,
        "effective_reattacks_total": effective_reattacks_total,
        "reattacks_requested": reattacks_requested,
        "last_requested_date": datetime_utils.get_as_str(min_requested_date)
        if min_requested_date != default_date
        else "",
        "reattacks_executed": reattacks_executed,
        "reattacks_executed_total": reattacks_executed_total,
        "last_executed_date": datetime_utils.get_as_str(min_executed_date)
        if min_executed_date != default_date
        else "",
        "pending_attacks": pending_attacks,
    }


def sort_historic_by_date(historic: Any) -> HistoricType:
    historic_sort = sorted(historic, key=lambda i: i["date"])
    return historic_sort


def _get_vuln_state_action(
    historic_state: Tuple[VulnerabilityState, ...],
) -> List[Action]:
    actions: List[Action] = [
        Action(
            action=state.status.value,
            date=str(
                datetime_utils.get_date_from_iso_str(state.modified_date)
            ),
            justification="",
            manager="",
            times=1,
        )
        for state in historic_state
    ]
    return list({action.date: action for action in actions}.values())


def get_state_actions(
    vulns_state: Tuple[Tuple[VulnerabilityState, ...], ...],
) -> List[Action]:
    states_actions = list(
        itertools.chain.from_iterable(
            _get_vuln_state_action(historic_state)
            for historic_state in vulns_state
        )
    )
    actions = [
        action._replace(times=times)
        for action, times in Counter(states_actions).most_common()
    ]
    return actions


def _get_vuln_treatment_actions(
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
) -> List[Action]:
    actions: List[Action] = [
        Action(
            action=treatment.status.value,
            date=str(
                datetime_utils.get_date_from_iso_str(treatment.modified_date)
            ),
            justification=treatment.justification,
            manager=treatment.manager,
            times=1,
        )
        for treatment in historic_treatment
        if (
            treatment.status
            in {
                VulnerabilityTreatmentStatus.ACCEPTED,
                VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
            }
            and treatment.acceptance_status
            not in {
                VulnerabilityAcceptanceStatus.REJECTED,
                VulnerabilityAcceptanceStatus.SUBMITTED,
            }
        )
    ]
    return list({action.date: action for action in actions}.values())


def get_treatment_actions(
    vulns_treatment: Tuple[Tuple[VulnerabilityTreatment, ...], ...],
) -> List[Action]:
    treatments_actions = list(
        itertools.chain.from_iterable(
            _get_vuln_treatment_actions(historic_treatment)
            for historic_treatment in vulns_treatment
        )
    )
    actions = [
        action._replace(times=times)
        for action, times in Counter(treatments_actions).most_common()
    ]
    return actions


def validate_closed(vuln: Dict[str, FindingType]) -> Dict[str, FindingType]:
    """Validate vuln closed."""
    if (
        cast(List[Dict[str, FindingType]], vuln.get("historic_state", [{}]))[
            -1
        ].get("state")
        == "closed"
    ):
        raise VulnAlreadyClosed()
    return vuln


def validate_requested_verification(
    vuln: Dict[str, FindingType]
) -> Dict[str, FindingType]:
    """Validate vuln is not resquested."""
    historic_verification = cast(
        List[Dict[str, FindingType]], vuln.get("historic_verification", [{}])
    )
    if historic_verification[-1].get("status", "") == "REQUESTED":
        raise AlreadyRequested()
    return vuln


def validate_verify(vuln: Dict[str, FindingType]) -> Dict[str, FindingType]:
    """Validate vuln is resquested."""
    if not is_reattack_requested(vuln):
        raise NotVerificationRequested()
    return vuln


def validate_justification_length(justification: str) -> None:
    """Validate justification length."""
    max_justification_length = 5000
    if len(justification) > max_justification_length:
        raise InvalidJustificationMaxLength(max_justification_length)


def validate_not_requested_zero_risk_vuln(
    vuln: Dict[str, FindingType]
) -> Dict[str, FindingType]:
    """Validate zero risk vuln is not already resquested."""
    historic_zero_risk = cast(
        List[Dict[str, FindingType]], vuln.get("historic_zero_risk", [{}])
    )
    if historic_zero_risk[-1].get("status", "") == "REQUESTED":
        raise AlreadyZeroRiskRequested()
    return vuln


def validate_requested_vuln_zero_risk(
    vuln: Dict[str, FindingType]
) -> Dict[str, FindingType]:
    """Validate zero risk vuln is already resquested."""
    historic_zero_risk = cast(
        List[Dict[str, FindingType]], vuln.get("historic_zero_risk", [{}])
    )
    if historic_zero_risk[-1].get("status", "") != "REQUESTED":
        raise NotZeroRiskRequested()
    return vuln
