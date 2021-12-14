# pylint:disable=too-many-lines

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
)
from datetime import (
    date as datetype,
    datetime,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
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
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
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
import logging
from newutils.datetime import (
    convert_from_iso_str,
    convert_to_iso_str,
)
from newutils.requests import (
    map_source,
)
from operator import (
    attrgetter,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Counter,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


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


def filter_zero_risk(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if vuln.zero_risk
        and vuln.zero_risk.status
        in (
            VulnerabilityZeroRiskStatus.CONFIRMED,
            VulnerabilityZeroRiskStatus.REQUESTED,
        )
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


def filter_historic_date(
    historic: Tuple[VulnerabilityTreatment, ...],
    min_date: datetime,
) -> Tuple[VulnerabilityTreatment, ...]:
    """Filter historics since a given date."""
    return tuple(
        entry
        for entry in historic
        if min_date
        and datetime_utils.get_date_from_iso_str(entry.modified_date)
        >= min_date.date()
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
    return finding


def format_where(
    where: str, vulnerabilities: Tuple[Vulnerability, ...]
) -> str:
    for vuln in vulnerabilities:
        where = f"{where}{vuln.where} ({vuln.specific})\n"
    return where


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
        opening_date = datetime_utils.get_date_from_iso_str(
            open_state.modified_date
        )
        if min_date and min_date > opening_date:
            opening_date = None
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
    return (
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


def get_total_treatment_date(
    historics: Tuple[Tuple[VulnerabilityTreatment, ...], ...],
    min_date: datetime,
) -> Dict[str, int]:
    """Get the total treatment of all the vulns filtered by date"""
    status_count: Counter[VulnerabilityTreatmentStatus] = Counter()
    acceptance_count: Counter[VulnerabilityAcceptanceStatus] = Counter()
    treatments = tuple(
        treatment
        for historic in historics
        for treatment in filter_historic_date(historic, min_date)
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


def get_last_requested_reattack_date(
    historic: Tuple[VulnerabilityVerification, ...],
) -> Optional[str]:
    """Get last requested reattack date in ISO8601 UTC format."""
    return next(
        (
            verification.modified_date
            for verification in reversed(historic)
            if verification.status == VulnerabilityVerificationStatus.REQUESTED
        ),
        None,
    )


def get_last_reattack_date(
    historic: Tuple[VulnerabilityVerification, ...],
) -> Optional[str]:
    """Get last reattack date in ISO8601 UTC format."""
    return next(
        (
            verification.modified_date
            for verification in reversed(historic)
            if verification.status == VulnerabilityVerificationStatus.VERIFIED
        ),
        None,
    )


def get_total_reattacks_stats(  # pylint: disable=too-many-locals
    vulns: Tuple[Vulnerability, ...],
    historics: Tuple[Tuple[VulnerabilityVerification, ...], ...],
    min_date: datetime,
) -> Dict[str, Union[int, str]]:
    """Get the total reattacks of all the vulns."""
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

    for vuln, historic in zip(vulns, historics):
        request_date = get_last_requested_reattack_date(historic)
        if request_date:
            last_requested_reattack_date = datetime.fromisoformat(request_date)
            # Get oldest reattack request date
            min_requested_date = max(
                min_requested_date, last_requested_reattack_date
            )
            if min_date and last_requested_reattack_date >= min_date:
                reattacks_requested += 1
        verified_date = get_last_reattack_date(historic)
        if verified_date:
            # Increment totals, no date filtered
            reattacks_executed_total += 1
            if vuln.state.status == VulnerabilityStateStatus.CLOSED:
                effective_reattacks_total += 1
            # Get oldest executed reattack date
            last_reattack_date = datetime.fromisoformat(verified_date)
            min_executed_date = max(min_executed_date, last_reattack_date)
            if min_date and last_reattack_date >= min_date:
                reattacks_executed += 1
                if vuln.state.status == VulnerabilityStateStatus.CLOSED:
                    effective_reattacks += 1
        if (
            vuln.verification
            and vuln.verification.status
            == VulnerabilityVerificationStatus.REQUESTED
        ):
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


def validate_closed(vulnerability: Vulnerability) -> Vulnerability:
    """Validate if the vulnerability is closed."""
    if vulnerability.state.status == VulnerabilityStateStatus.CLOSED:
        raise VulnAlreadyClosed()
    return vulnerability


def validate_requested_verification(
    vulnerability: Vulnerability,
) -> Vulnerability:
    """Validate if the vulnerability is not resquested."""
    if (
        vulnerability.verification
        and vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    ):
        raise AlreadyRequested()
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


def format_vulnerability_metadata_item(
    metadata: VulnerabilityMetadataToUpdate,
) -> Item:
    item = {
        "external_bts": metadata.bug_tracking_system_url,
        "commit_hash": metadata.commit,
        "skims_method": metadata.skims_method,
        "severity": metadata.custom_severity,
        "repo_nickname": metadata.repo,
        "specific": metadata.specific,
        "stream": ",".join(metadata.stream) if metadata.stream else None,
        "tag": metadata.tags,
        "vuln_type": metadata.type,
        "where": metadata.where,
    }
    return {
        key: None if not value else value
        for key, value in item.items()
        if value is not None
    }


def format_vulnerability_state_item(
    state: VulnerabilityState,
) -> Item:
    if state.status == VulnerabilityStateStatus.DELETED:
        formatted_status = state.status.value
    else:
        formatted_status = str(state.status.value).lower()
    item = {
        "analyst": state.modified_by,
        "date": convert_from_iso_str(state.modified_date),
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


def format_vulnerability_item(  # noqa: MC0001
    vulnerability: Vulnerability,
) -> Item:
    item = {
        "finding_id": vulnerability.finding_id,
        "UUID": vulnerability.id,
        "vuln_type": str(vulnerability.type.value).lower(),
        "where": vulnerability.where,
        "source": str(vulnerability.state.source.value).lower(),
        "specific": vulnerability.specific,
        "historic_state": [
            format_vulnerability_state_item(vulnerability.state)
        ],
    }
    if vulnerability.commit:
        item["commit_hash"] = vulnerability.commit
    if vulnerability.custom_severity:
        item["severity"] = vulnerability.custom_severity
    if vulnerability.bug_tracking_system_url:
        item["external_bts"] = vulnerability.bug_tracking_system_url
    if vulnerability.repo:
        item["repo_nickname"] = vulnerability.repo
    if vulnerability.skims_method:
        item["skims_method"] = vulnerability.skims_method
    if vulnerability.stream:
        item["stream"] = ",".join(vulnerability.stream)
    if vulnerability.tags:
        item["tag"] = vulnerability.tags
    if vulnerability.treatment:
        item["historic_treatment"] = [
            format_vulnerability_treatment_item(vulnerability.treatment)
        ]
    if vulnerability.verification:
        item["historic_verification"] = [
            format_vulnerability_verification_item(vulnerability.verification)
        ]
    if vulnerability.zero_risk:
        item["historic_zero_risk"] = [
            format_vulnerability_zero_risk_item(vulnerability.zero_risk)
        ]
    return item


def exists(key: str, item: Dict[str, Any]) -> bool:
    return key in item and item[key] is not None


def get_optional(key: str, item: Dict[str, Any], fallback: Any = None) -> Any:
    if exists(key, item):
        return item[key]
    return fallback


def format_vulnerability_state(state: Dict[str, Any]) -> VulnerabilityState:
    return VulnerabilityState(
        modified_by=state["analyst"],
        modified_date=convert_to_iso_str(state["date"]),
        source=Source[map_source(state["source"]).upper()],
        status=VulnerabilityStateStatus[state["state"].upper()],
        justification=(
            StateRemovalJustification[state["justification"]]
            if exists("justification", state)
            else None
        ),
    )


def format_vulnerability_treatment(
    treatment: Dict[str, Any]
) -> VulnerabilityTreatment:
    accepted_until: Optional[str] = get_optional("acceptance_date", treatment)
    if accepted_until:
        accepted_until = convert_to_iso_str(accepted_until)
    return VulnerabilityTreatment(
        modified_by=get_optional("user", treatment),
        modified_date=convert_to_iso_str(treatment["date"]),
        status=VulnerabilityTreatmentStatus(
            treatment["treatment"].replace(" ", "_").upper()
        ),
        accepted_until=accepted_until,
        acceptance_status=(
            VulnerabilityAcceptanceStatus[treatment["acceptance_status"]]
            if exists("acceptance_status", treatment)
            else None
        ),
        justification=get_optional("justification", treatment),
        assigned=get_optional("assigned", treatment),
    )


def format_vulnerability_verification(
    verification: Dict[str, str]
) -> VulnerabilityVerification:
    return VulnerabilityVerification(
        modified_date=convert_to_iso_str(verification["date"]),
        status=VulnerabilityVerificationStatus(verification["status"]),
    )


def format_vulnerability_zero_risk(
    zero_risk: Dict[str, str]
) -> VulnerabilityZeroRisk:
    return VulnerabilityZeroRisk(
        comment_id=zero_risk["comment_id"],
        modified_by=zero_risk["email"],
        modified_date=convert_to_iso_str(zero_risk["date"]),
        status=VulnerabilityZeroRiskStatus(zero_risk["status"]),
    )


def format_vulnerability(item: Dict[str, Any]) -> Vulnerability:
    current_state: Dict[str, str] = item["historic_state"][-1]
    current_treatment: Optional[Dict[str, str]] = (
        item["historic_treatment"][-1]
        if exists("historic_treatment", item)
        else None
    )
    current_verification: Optional[Dict[str, str]] = (
        item["historic_verification"][-1]
        if exists("historic_verification", item)
        else None
    )
    current_zero_risk: Optional[Dict[str, str]] = (
        item["historic_zero_risk"][-1]
        if exists("historic_zero_risk", item)
        else None
    )

    return Vulnerability(
        finding_id=item["finding_id"],
        id=item["UUID"],
        specific=item["specific"],
        state=format_vulnerability_state(current_state),
        treatment=(
            format_vulnerability_treatment(current_treatment)
            if current_treatment
            else None
        ),
        type=VulnerabilityType(item["vuln_type"].upper()),
        where=item["where"],
        bug_tracking_system_url=get_optional("external_bts", item),
        commit=get_optional("commit_hash", item),
        custom_severity=(
            int(item["severity"])
            if exists("severity", item) and item["severity"]
            else None
        ),
        hash=None,
        repo=get_optional("repo_nickname", item),
        skims_method=get_optional("skims_method", item),
        stream=item["stream"].split(",") if exists("stream", item) else None,
        tags=sorted(item["tag"]) if exists("tag", item) else None,
        verification=(
            format_vulnerability_verification(current_verification)
            if current_verification
            else None
        ),
        zero_risk=(
            format_vulnerability_zero_risk(current_zero_risk)
            if current_zero_risk
            else None
        ),
    )
