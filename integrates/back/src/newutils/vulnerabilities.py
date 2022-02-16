from . import (
    datetime as datetime_utils,
)
from custom_exceptions import (
    AlreadyOnHold,
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
)
from datetime import (
    date as datetype,
    datetime,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from db_model.vulnerabilities.utils import (
    adjust_historic_dates,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from dynamodb.types import (
    Item,
)
import html
import itertools
from newutils.datetime import (
    convert_from_iso_str,
)
from operator import (
    attrgetter,
)
from typing import (
    Any,
    Counter,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
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


def is_accepted_undefined_vulnerability(
    vulnerability: Vulnerability,
) -> bool:
    return bool(
        vulnerability.treatment
        and vulnerability.treatment.status
        == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        and vulnerability.state.status == VulnerabilityStateStatus.OPEN
    )


def is_reattack_requested(vulnerability: Vulnerability) -> bool:
    return bool(
        vulnerability.verification
        and vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    )


def is_range(specific: str) -> bool:
    """Validate if a specific field has range value."""
    return "-" in specific


def is_sequence(specific: str) -> bool:
    """Validate if a specific field has secuence value."""
    return "," in specific


def filter_no_treatment_vulns(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if vuln.treatment
        and vuln.treatment.status == VulnerabilityTreatmentStatus.NEW
    )


def filter_non_deleted(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if vuln.state.status != VulnerabilityStateStatus.DELETED
    )


def filter_open_vulns(
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


def filter_non_confirmed_zero_risk(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vulnerability
        for vulnerability in vulnerabilities
        if not vulnerability.zero_risk
        or vulnerability.zero_risk.status
        != VulnerabilityZeroRiskStatus.CONFIRMED
    )


def filter_non_zero_risk(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if not vuln.zero_risk
        or vuln.zero_risk.status
        not in (
            VulnerabilityZeroRiskStatus.CONFIRMED,
            VulnerabilityZeroRiskStatus.REQUESTED,
        )
    )


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


def format_vulnerabilities(
    vulnerabilities: Tuple[Vulnerability, ...]
) -> Dict[str, List[Dict[str, str]]]:
    finding: Dict[str, List[Dict[str, str]]] = {
        "ports": [],
        "lines": [],
        "inputs": [],
    }
    vuln_values = {
        "ports": {"where": "host", "specific": "port"},
        "lines": {"where": "path", "specific": "line"},
        "inputs": {"where": "url", "specific": "field"},
    }
    for vuln in vulnerabilities:
        vuln_type = str(vuln.type.value).lower()
        finding[vuln_type].append(
            {
                vuln_values[vuln_type]["where"]: html.unescape(vuln.where),
                vuln_values[vuln_type]["specific"]: (
                    html.unescape(vuln.specific)
                ),
                "state": str(vuln.state.status.value).lower(),
            }
        )
        if vuln.commit:
            finding[vuln_type][-1]["commit_hash"] = vuln.commit
        if vuln.stream:
            finding[vuln_type][-1]["stream"] = ",".join(vuln.stream)
        if vuln.repo:
            finding[vuln_type][-1]["repo_nickname"] = vuln.repo
    return finding


def format_where(
    where: str, vulnerabilities: Tuple[Vulnerability, ...]
) -> str:
    for vuln in vulnerabilities:
        where = f"{where}{vuln.where} ({vuln.specific})\n"
    return where


def get_opening_date(
    vuln: Vulnerability,
    min_date: Optional[datetype] = None,
) -> Optional[datetype]:
    opening_date: datetype = datetime_utils.get_date_from_iso_str(
        vuln.unreliable_indicators.unreliable_report_date
    )
    if min_date and min_date > opening_date:
        return None
    return opening_date


def get_closing_date(
    vulnerability: Vulnerability,
    min_date: Optional[datetype] = None,
) -> Optional[datetype]:
    closing_date: Optional[datetype] = None
    if vulnerability.state.status == VulnerabilityStateStatus.CLOSED:
        closing_date = datetime_utils.get_date_from_iso_str(
            vulnerability.state.modified_date
        )
        if min_date and min_date > closing_date:
            return None
    return closing_date


def get_mean_remediate_vulnerabilities_cvssf(
    vulns: Tuple[Vulnerability, ...],
    finding_cvssf: Dict[str, Decimal],
    min_date: Optional[datetype] = None,
) -> Decimal:
    total_days: Decimal = Decimal("0.0")
    open_vuln_dates = [get_opening_date(vuln, min_date) for vuln in vulns]
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
    min_date: Optional[datetype] = None,
) -> Decimal:
    """Get mean time to remediate a vulnerability."""
    total_vuln = 0
    total_days = 0
    open_vuln_dates = [get_opening_date(vuln, min_date) for vuln in vulns]
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


def get_report_dates(
    vulns: Tuple[Vulnerability, ...],
) -> Tuple[datetime, ...]:
    """Get report dates for vulnerabilities."""
    return tuple(
        datetime.fromisoformat(
            vuln.unreliable_indicators.unreliable_report_date
        )
        for vuln in vulns
    )


def group_specific(
    vulns: Tuple[Vulnerability, ...], vuln_type: VulnerabilityType
) -> Tuple[Vulnerability, ...]:
    """Group vulnerabilities by its specific field."""
    sorted_by_where = sort_vulnerabilities(vulns)
    grouped_vulns = []
    for key, group_iter in itertools.groupby(
        sorted_by_where,
        key=lambda vuln: (vuln.where, vuln.commit),
    ):
        group = list(group_iter)
        specific_grouped = (
            ",".join([vuln.specific for vuln in group])
            if vuln_type == VulnerabilityType.INPUTS
            else get_ranges(sorted([int(vuln.specific) for vuln in group]))
        )
        grouped_vulns.append(
            Vulnerability(
                finding_id=group[0].finding_id,
                id=group[0].id,
                specific=specific_grouped,
                state=group[0].state,
                type=group[0].type,
                where=key[0],
                commit=(
                    group[0].commit[0:7]
                    if group[0].commit is not None
                    else None
                ),
            )
        )
    return tuple(grouped_vulns)


def sort_vulnerabilities(
    item: Tuple[Vulnerability, ...]
) -> Tuple[Vulnerability, ...]:
    """Sort a vulnerability by its where field."""
    return tuple(sorted(item, key=attrgetter("where")))


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


def get_treatment_from_org_finding_policy(
    *, modified_date: str, user_email: str
) -> Tuple[VulnerabilityTreatment, VulnerabilityTreatment]:
    treatments: Tuple[
        VulnerabilityTreatment, VulnerabilityTreatment
    ] = adjust_historic_dates(
        (
            VulnerabilityTreatment(
                acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED,
                justification="From organization findings policy",
                assigned=user_email,
                modified_by=user_email,
                modified_date=modified_date,
                status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
            ),
            VulnerabilityTreatment(
                acceptance_status=VulnerabilityAcceptanceStatus.APPROVED,
                justification="From organization findings policy",
                assigned=user_email,
                modified_by=user_email,
                modified_date=modified_date,
                status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
            ),
        )
    )
    return treatments


def get_total_treatment_date(
    vulns: Tuple[Vulnerability, ...],
    min_date: datetime,
) -> Dict[str, int]:
    """Get the total treatment of all the vulns filtered by date."""
    status_count: Counter[VulnerabilityTreatmentStatus] = Counter()
    acceptance_count: Counter[VulnerabilityAcceptanceStatus] = Counter()
    treatments = tuple(
        vuln.treatment
        for vuln in vulns
        if vuln.treatment
        and datetime.fromisoformat(vuln.treatment.modified_date) >= min_date
    )

    for treatment in treatments:
        # Check if any of these states occurred in the period
        status_count.update([treatment.status])
        acceptance_count.update([treatment.acceptance_status])

    return {
        "accepted": status_count[VulnerabilityTreatmentStatus.ACCEPTED],
        "accepted_undefined_submitted": acceptance_count[
            VulnerabilityAcceptanceStatus.SUBMITTED
        ],
        "accepted_undefined_approved": acceptance_count[
            VulnerabilityAcceptanceStatus.APPROVED
        ],
        "undefined_treatment": status_count[VulnerabilityTreatmentStatus.NEW],
    }


def _get_effective_reattacks(
    vulns: Tuple[Vulnerability, ...],
    min_date: datetime,
) -> int:
    """Get count for closed and remediated vulns since the given date."""
    vulns_effective_reattack = [
        vuln
        for vuln in vulns
        if vuln.verification
        and vuln.verification.status
        == VulnerabilityVerificationStatus.VERIFIED
        and datetime.fromisoformat(vuln.verification.modified_date) >= min_date
        and vuln.state.status == VulnerabilityStateStatus.CLOSED
    ]
    return len(vulns_effective_reattack)


def _get_reattacks_requested(
    vulns: Tuple[Vulnerability, ...],
    min_date: datetime,
) -> int:
    """Get count for vulns with reattacks requested since the given date."""
    vulns_reattack_requested = [
        vuln
        for vuln in vulns
        if vuln.verification
        and vuln.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
        and datetime.fromisoformat(vuln.verification.modified_date) >= min_date
    ]
    return len(vulns_reattack_requested)


def _get_last_reattack_requested_date(
    vulns: Tuple[Vulnerability, ...],
) -> str:
    """Get the most recent reattack request date for these vulns."""
    dates_reattack_requested = [
        datetime_utils.convert_from_iso_str(vuln.verification.modified_date)
        for vuln in vulns
        if vuln.verification
        and vuln.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    ]
    if not dates_reattack_requested:
        return ""
    return max(dates_reattack_requested)


def _get_reattacks_executed(
    vulns: Tuple[Vulnerability, ...],
    min_date: datetime,
) -> int:
    """Get count for vulns with reattacks executed since the given date."""
    vulns_reattack_executed = [
        vuln
        for vuln in vulns
        if vuln.verification
        and vuln.verification.status
        == VulnerabilityVerificationStatus.VERIFIED
        and datetime.fromisoformat(vuln.verification.modified_date) >= min_date
    ]
    return len(vulns_reattack_executed)


def _get_last_reattack_executed_date(
    vulns: Tuple[Vulnerability, ...],
) -> str:
    """Get the most recent reattack/verification date for these vulns."""
    dates_reattack_executed = [
        datetime_utils.convert_from_iso_str(vuln.verification.modified_date)
        for vuln in vulns
        if vuln.verification
        and vuln.verification.status
        == VulnerabilityVerificationStatus.VERIFIED
    ]
    if not dates_reattack_executed:
        return ""
    return max(dates_reattack_executed)


async def get_total_reattacks_stats(
    vulns: Tuple[Vulnerability, ...],
    min_date: datetime,
) -> Dict[str, Union[int, str]]:
    """Get the total reattacks of all the vulns."""
    default_date: datetime = datetime_utils.get_from_str(
        datetime_utils.DEFAULT_STR
    )
    return {
        "effective_reattacks": _get_effective_reattacks(vulns, min_date),
        "effective_reattacks_total": _get_effective_reattacks(
            vulns, default_date
        ),
        "reattacks_requested": _get_reattacks_requested(vulns, min_date),
        "last_requested_date": _get_last_reattack_requested_date(vulns),
        "reattacks_executed": _get_reattacks_executed(vulns, min_date),
        "reattacks_executed_total": _get_reattacks_executed(
            vulns, default_date
        ),
        "last_executed_date": _get_last_reattack_executed_date(vulns),
        "pending_attacks": _get_reattacks_requested(vulns, default_date),
    }


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
            manager=treatment.assigned,
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


def get_treatment_changes(
    historic_treatment: Tuple[VulnerabilityTreatment, ...]
) -> int:
    if historic_treatment:
        first_treatment = historic_treatment[0]
        return (
            len(historic_treatment) - 1
            if first_treatment.status == VulnerabilityTreatmentStatus.NEW
            else len(historic_treatment)
        )
    return 0


def validate_closed(vulnerability: Vulnerability) -> Vulnerability:
    """Validate if the vulnerability is closed."""
    if vulnerability.state.status == VulnerabilityStateStatus.CLOSED:
        raise VulnAlreadyClosed()
    return vulnerability


def validate_requested_verification(
    vulnerability: Vulnerability,
) -> Vulnerability:
    """Validate if the vulnerability is not requested."""
    if (
        vulnerability.verification
        and vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    ):
        raise AlreadyRequested()
    return vulnerability


def validate_requested_hold(
    vulnerability: Vulnerability,
) -> Vulnerability:
    """Validate if the vulnerability is not on hold and a reattack has been
    requested beforehand"""
    if (
        vulnerability.verification
        and vulnerability.verification.status
        == VulnerabilityVerificationStatus.ON_HOLD
    ):
        raise AlreadyOnHold()
    if (
        vulnerability.verification
        and vulnerability.verification.status
        != VulnerabilityVerificationStatus.REQUESTED
    ):
        raise NotVerificationRequested()
    return vulnerability


def validate_reattack_requested(
    vulnerability: Vulnerability,
) -> Vulnerability:
    """Validate if the vulnerability does not have a reattack resquested."""
    if (
        not vulnerability.verification
        or vulnerability.verification.status
        != VulnerabilityVerificationStatus.REQUESTED
    ):
        raise NotVerificationRequested()
    return vulnerability


def validate_justification_length(justification: str) -> None:
    """Validate justification length."""
    max_justification_length = 10000
    if len(justification) > max_justification_length:
        raise InvalidJustificationMaxLength(max_justification_length)


def validate_non_zero_risk_requested(
    vulnerability: Vulnerability,
) -> Vulnerability:
    """Validate if zero risk vuln is not already resquested."""
    if (
        vulnerability.zero_risk
        and vulnerability.zero_risk.status
        == VulnerabilityZeroRiskStatus.REQUESTED
    ):
        raise AlreadyZeroRiskRequested()
    return vulnerability


def validate_zero_risk_requested(
    vulnerability: Vulnerability,
) -> Vulnerability:
    """Validate if zero risk vuln is already resquested."""
    if (
        not vulnerability.zero_risk
        or vulnerability.zero_risk.status
        != VulnerabilityZeroRiskStatus.REQUESTED
    ):
        raise NotZeroRiskRequested()
    return vulnerability


def format_vulnerability_state_item(
    state: VulnerabilityState,
) -> Item:
    if state.status == VulnerabilityStateStatus.DELETED:
        formatted_status = state.status.value
    else:
        formatted_status = str(state.status.value).lower()
    item = {
        "date": convert_from_iso_str(state.modified_date),
        "hacker": state.modified_by,
        "source": str(state.source.value).lower(),
        "state": formatted_status,
    }
    if state.justification:
        item["justification"] = state.justification.value
    return item


def format_vulnerability_treatment_item(
    treatment: VulnerabilityTreatment,
) -> Item:
    item = {
        "date": convert_from_iso_str(treatment.modified_date),
        "treatment": treatment.status.value,
    }
    if treatment.accepted_until:
        item["acceptance_date"] = convert_from_iso_str(
            treatment.accepted_until
        )
    if treatment.justification:
        item["justification"] = treatment.justification
    if treatment.modified_by:
        item["user"] = treatment.modified_by
    if treatment.acceptance_status:
        item["acceptance_status"] = treatment.acceptance_status.value
    if treatment.assigned:
        item["assigned"] = treatment.assigned
    return item


def format_vulnerability_verification_item(
    verification: VulnerabilityVerification,
) -> Item:
    item = {
        "date": convert_from_iso_str(verification.modified_date),
        "status": verification.status.value,
    }
    return item


def format_vulnerability_zero_risk_item(
    zero_risk: VulnerabilityZeroRisk,
) -> Item:
    item = {
        "comment_id": zero_risk.comment_id,
        "email": zero_risk.modified_by,
        "date": convert_from_iso_str(zero_risk.modified_date),
        "status": zero_risk.status.value,
    }
    return item
