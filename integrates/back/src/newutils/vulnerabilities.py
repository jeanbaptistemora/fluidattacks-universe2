from . import (
    datetime as datetime_utils,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    AlreadyOnHold,
    AlreadyRequested,
    AlreadyZeroRiskRequested,
    InvalidJustificationMaxLength,
    InvalidRange,
    LineDoesNotExistInTheLinesOfCodeRange,
    NotVerificationRequested,
    NotZeroRiskRequested,
    OutdatedRepository,
    RootNotFound,
    ToeInputNotFound,
    ToeLinesNotFound,
    ToePortNotFound,
    VulnAlreadyClosed,
    VulnerabilityHasNotBeenReleased,
    VulnerabilityHasNotBeenSubmitted,
    VulnerabilityPathDoesNotExistInToeLines,
    VulnerabilityPortFieldDoNotExistInToePorts,
    VulnerabilityUrlFieldDoNotExistInToeInputs,
)
from datetime import (
    date as datetype,
    datetime,
    timezone,
)
from db_model.enums import (
    Source,
)
from db_model.roots.types import (
    GitRoot,
    Root,
)
from db_model.toe_inputs.types import (
    ToeInputRequest,
)
from db_model.toe_lines.types import (
    ToeLinesRequest,
)
from db_model.toe_ports.types import (
    ToePortRequest,
)
from db_model.utils import (
    adjust_historic_dates,
)
from db_model.vulnerabilities.constants import (
    RELEASED_FILTER_STATUSES,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTool,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from db_model.vulnerabilities.utils import (
    get_current_treatment_converted,
    get_inverted_treatment_converted,
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
import re
from typing import (
    Any,
    cast,
    Counter,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union,
)


class Action(NamedTuple):
    action: str
    assigned: str
    date: str
    justification: str
    times: int


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
        and vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    )


def is_reattack_requested(vulnerability: Vulnerability) -> bool:
    return bool(
        vulnerability.verification
        and vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    )


def is_reattack_on_hold(vulnerability: Vulnerability) -> bool:
    return bool(
        vulnerability.verification
        and vulnerability.verification.status
        == VulnerabilityVerificationStatus.ON_HOLD
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
        if vuln.state.status
        not in {
            VulnerabilityStateStatus.DELETED,
            VulnerabilityStateStatus.MASKED,
        }
    )


def filter_open_vulns(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    )


def filter_closed_vulns(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if vuln.state.status == VulnerabilityStateStatus.SAFE
    )


def filter_released_vulns(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if vuln.state.status in RELEASED_FILTER_STATUSES
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


def _format_tool_item(
    tool: VulnerabilityTool,
) -> Item:
    return {
        "name": tool.name,
        "impact": str(tool.impact.value).lower(),
    }


async def format_vulnerabilities(
    group_name: str, loaders: Any, vulnerabilities: Tuple[Vulnerability, ...]
) -> Dict[str, List[Dict[str, Union[str, Item]]]]:
    finding: Dict[str, List[Dict[str, Union[str, Item]]]] = {
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
        format_source = (
            str(vuln.state.source.value).lower()
            if vuln.state.source != Source.ASM
            else "analyst"
        )
        vuln_type = str(vuln.type.value).lower()
        finding[vuln_type].append(
            {
                vuln_values[vuln_type]["where"]: html.unescape(
                    vuln.state.where
                ),
                vuln_values[vuln_type]["specific"]: (
                    html.unescape(vuln.state.specific)
                ),
                "state": get_current_state_converted(
                    vuln.state.status.value
                ).lower(),
                "source": format_source,
                "tool": _format_tool_item(vuln.state.tool)
                if vuln.state.tool
                else _format_tool_item(
                    VulnerabilityTool(
                        name="none",
                        impact=VulnerabilityToolImpact.DIRECT,
                    )
                ),
            }
        )
        if vuln.state.commit:
            finding[vuln_type][-1]["commit_hash"] = vuln.state.commit
        if vuln.stream:
            finding[vuln_type][-1]["stream"] = ",".join(vuln.stream)
        if vuln.root_id:
            with suppress(RootNotFound):
                root: Root = await loaders.root.load(
                    (group_name, vuln.root_id)
                )
                finding[vuln_type][-1]["repo_nickname"] = root.state.nickname
    return finding


def format_where(
    where: str, vulnerabilities: Tuple[Vulnerability, ...]
) -> str:
    for vuln in vulnerabilities:
        where = f"{where}{vuln.state.where} ({vuln.state.specific})\n"
    return where


def get_opening_date(
    vuln: Vulnerability,
    min_date: Optional[datetype] = None,
) -> Optional[datetype]:
    opening_date: datetype = vuln.created_date.date()
    if min_date and min_date > opening_date:
        return None
    return opening_date


def get_closing_date(
    vulnerability: Vulnerability,
    min_date: Optional[datetype] = None,
) -> Optional[datetype]:
    closing_date: Optional[datetype] = None
    if vulnerability.state.status == VulnerabilityStateStatus.SAFE:
        closing_date = vulnerability.state.modified_date.date()
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
            current_day = datetime_utils.get_utc_now().date()
            total_days += Decimal(
                (current_day - filtered_open_vuln_dates[index]).days
                * closed_vuln_date[1]
            )
    total_cvssf: Decimal = Decimal(
        sum(
            finding_cvssf[vuln.finding_id]
            for vuln, open_date in zip(vulns, open_vuln_dates)
            if open_date
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
            current_day = datetime_utils.get_utc_now().date()
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
    return tuple(vuln.created_date for vuln in vulns)


def group_specific(
    vulns: Tuple[Vulnerability, ...], vuln_type: VulnerabilityType
) -> Tuple[Vulnerability, ...]:
    """Group vulnerabilities by its specific field."""
    sorted_by_where = sort_vulnerabilities(vulns)
    grouped_vulns = []
    for key, group_iter in itertools.groupby(
        sorted_by_where,
        key=lambda vuln: (vuln.state.where, vuln.state.commit),
    ):
        group = list(group_iter)
        specific_grouped = (
            ",".join([vuln.state.specific for vuln in group])
            if vuln_type == VulnerabilityType.INPUTS
            else get_ranges(
                sorted([int(vuln.state.specific) for vuln in group])
            )
        )
        grouped_vulns.append(
            Vulnerability(
                created_by=group[0].created_by,
                created_date=group[0].created_date,
                finding_id=group[0].finding_id,
                group_name=group[0].group_name,
                hacker_email=group[0].hacker_email,
                id=group[0].id,
                state=group[0].state._replace(
                    commit=(
                        group[0].state.commit[0:7]
                        if group[0].state.commit is not None
                        else None
                    ),
                    specific=specific_grouped,
                    where=key[0],
                ),
                type=group[0].type,
            )
        )
    return tuple(grouped_vulns)


def sort_vulnerabilities(
    item: Tuple[Vulnerability, ...]
) -> Tuple[Vulnerability, ...]:
    """Sort a vulnerability by its where field."""
    return tuple(
        sorted(item, key=lambda vulnerability: vulnerability.state.where)
    )


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


def adjust_historic_treatment_dates(
    historic: Tuple[VulnerabilityTreatment, ...],
) -> Tuple[VulnerabilityTreatment, ...]:
    return cast(
        Tuple[VulnerabilityTreatment, ...],
        adjust_historic_dates(historic),
    )


def get_treatment_from_org_finding_policy(
    *, modified_date: datetime, user_email: str
) -> Tuple[VulnerabilityTreatment, ...]:
    treatments: Tuple[
        VulnerabilityTreatment, ...
    ] = adjust_historic_treatment_dates(
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


def _get_vuln_state_action(
    historic_state: Tuple[VulnerabilityState, ...],
) -> List[Action]:
    actions: list[Action] = [
        Action(
            action=state.status.value,
            date=str(state.modified_date.date()),
            justification="",
            assigned="",
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
            date=str(treatment.modified_date.date()),
            justification=treatment.justification,
            assigned=treatment.assigned,
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
            and treatment.justification
            and treatment.assigned
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
    if vulnerability.state.status == VulnerabilityStateStatus.SAFE:
        raise VulnAlreadyClosed()
    return vulnerability


async def validate_requested_verification(
    loaders: Any,
    vulnerability: Vulnerability,
    is_closing_event: bool = False,
) -> Vulnerability:
    """Validate if the vulnerability is not requested. If no Event is being
    closed, vulnerabilities on hold count as requested"""
    if (
        vulnerability.verification
        and vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    ):
        raise AlreadyRequested()
    if (
        (not is_closing_event)
        and vulnerability.verification
        and vulnerability.verification.status
        == VulnerabilityVerificationStatus.ON_HOLD
    ):
        raise AlreadyRequested()
    if vulnerability.type == VulnerabilityType.LINES and vulnerability.root_id:
        with suppress(RootNotFound):
            root: GitRoot = await loaders.root.load(
                (vulnerability.group_name, vulnerability.root_id)
            )
            if (
                isinstance(root, GitRoot)
                and root.cloning.commit == vulnerability.state.commit
                and root.cloning.commit_date
                and (
                    datetime.now(timezone.utc) - root.cloning.commit_date
                ).seconds
                > (3600 * 20)
            ):
                raise OutdatedRepository()

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
        vulnerability.verification is None
        or vulnerability.verification
        and vulnerability.verification.status
        != VulnerabilityVerificationStatus.REQUESTED
    ):
        raise NotVerificationRequested()
    return vulnerability


def validate_reattack_requested(
    vulnerability: Vulnerability,
) -> Vulnerability:
    """Validate if the vulnerability does not have a reattack requested."""
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
) -> None:
    """Validate if zero risk vuln is not already resquested."""
    if (
        vulnerability.zero_risk
        and vulnerability.zero_risk.status
        == VulnerabilityZeroRiskStatus.REQUESTED
    ):
        raise AlreadyZeroRiskRequested()


def validate_released(
    vulnerability: Vulnerability,
) -> None:
    """Validate if the vulnerability is in a released status."""
    if vulnerability.state.status not in RELEASED_FILTER_STATUSES:
        raise VulnerabilityHasNotBeenReleased()


def validate_submitted(
    vulnerability: Vulnerability,
) -> None:
    """Validate if the vulnerability has been submitted."""
    if vulnerability.state.status is not VulnerabilityStateStatus.SUBMITTED:
        raise VulnerabilityHasNotBeenSubmitted()


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
    if state.status in {
        VulnerabilityStateStatus.DELETED,
        VulnerabilityStateStatus.MASKED,
    }:
        formatted_status = state.status.value
    else:
        formatted_status = get_current_state_converted(
            state.status.value
        ).lower()
    item = {
        "date": datetime_utils.get_as_str(state.modified_date),
        "hacker": state.modified_by,
        "source": str(state.source.value).lower(),
        "state": formatted_status,
        "status": str(state.status.value),
    }
    if state.reasons:
        item["justification"] = state.reasons[0].value

    return item


def format_vulnerability_treatment_item(
    treatment: VulnerabilityTreatment,
    should_convert: bool = False,
) -> Item:
    item = {
        "date": datetime_utils.get_as_str(treatment.modified_date),
        "treatment": get_inverted_treatment_converted(treatment.status.value)
        if should_convert
        else get_current_treatment_converted(treatment.status.value),
    }
    if treatment.accepted_until:
        item["acceptance_date"] = datetime_utils.get_as_str(
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
        "date": datetime_utils.get_as_str(verification.modified_date),
        "status": verification.status.value,
    }
    return item


def format_vulnerability_zero_risk_item(
    zero_risk: VulnerabilityZeroRisk,
) -> Item:
    item = {
        "comment_id": zero_risk.comment_id,
        "email": zero_risk.modified_by,
        "date": datetime_utils.get_as_str(zero_risk.modified_date),
        "status": zero_risk.status.value,
    }
    return item


def get_advisories(where: str) -> Optional[str]:
    result = re.search(r"(?P<name>(\(.*\))?(\s+\[.*\]))", where)
    if result:
        return result.group("name")
    return None


def ignore_advisories(where: Optional[str]) -> str:
    if where is not None:
        where = re.sub(r"(\s+\(.*\))?(\s+\[.*\])?", "", where)
    return str(where)


def is_machine_vuln(vuln: Vulnerability) -> bool:
    return (
        vuln.state.source == Source.MACHINE
        or vuln.hacker_email == "machine@fluidattacks.com"
    )


async def validate_vulnerability_in_toe(  # noqa # NOSONAR
    loaders: Any,
    group_name: str,
    vulnerability: Vulnerability,
    index: int,
    raises: bool = True,
) -> Optional[Vulnerability]:
    if vulnerability.root_id:
        where = html.unescape(vulnerability.state.where)
        # There are cases, like SCA vulns, where the `where` attribute
        # has additional information `filename (package) [CVE]`
        where = ignore_advisories(where)

        if vulnerability.type == VulnerabilityType.LINES:
            try:
                toe_lines = await loaders.toe_lines.load(
                    ToeLinesRequest(
                        filename=where,
                        group_name=group_name,
                        root_id=vulnerability.root_id,
                    )
                )
            except ToeLinesNotFound as exc:
                if raises:
                    raise VulnerabilityPathDoesNotExistInToeLines(
                        index=f"{index}"
                    ) from exc
                return None

            if not 0 <= int(vulnerability.state.specific) <= toe_lines.loc:
                if raises:
                    raise LineDoesNotExistInTheLinesOfCodeRange(
                        line=vulnerability.state.specific, index=f"{index}"
                    )
                return None

        if vulnerability.type == VulnerabilityType.INPUTS:
            specific = html.unescape(vulnerability.state.specific)
            if match_specific := re.match(
                r"(?P<specific>.*)\s\(.*\)(\s\[.*\])?$", specific
            ):
                specific = match_specific.groupdict()["specific"]

            try:
                await loaders.toe_input.load(
                    ToeInputRequest(
                        component=where,
                        entry_point=""
                        if is_machine_vuln(vulnerability)
                        else specific,
                        group_name=group_name,
                        root_id=vulnerability.root_id,
                    )
                )
            except ToeInputNotFound as exc:
                if vulnerability.skims_technique not in {"APK"}:
                    if raises:
                        raise VulnerabilityUrlFieldDoNotExistInToeInputs(
                            index=f"{index}"
                        ) from exc  # noqa
                    return None

        if vulnerability.type == VulnerabilityType.PORTS:
            try:
                await loaders.toe_port.load(
                    ToePortRequest(
                        address=where,
                        port=vulnerability.state.specific,
                        group_name=group_name,
                        root_id=vulnerability.root_id,
                    )
                )
            except ToePortNotFound as exc:
                if raises:
                    raise VulnerabilityPortFieldDoNotExistInToePorts(
                        index=f"{index}"
                    ) from exc
                return None

        return vulnerability
    return None


def get_current_state_converted(state: str) -> str:
    if state in {"SAFE", "VULNERABLE"}:
        translation: dict[str, str] = {
            "SAFE": "CLOSED",
            "VULNERABLE": "OPEN",
        }

        return translation[state]
    return state


def get_inverted_state_converted(state: str) -> str:
    if state in {"CLOSED", "OPEN"}:
        translation: dict[str, str] = {
            "CLOSED": "SAFE",
            "OPEN": "VULNERABLE",
        }

        return translation[state]
    return state
