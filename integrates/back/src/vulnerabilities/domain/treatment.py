from .core import (
    should_send_update_treatment,
)
from .utils import (
    compare_historic_treatments,
    format_vulnerability_locations,
    get_valid_assigned,
    validate_acceptance,
)
from aioextensions import (
    collect,
    in_thread,
)
import authz
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidDateFormat,
    InvalidNotificationRequest,
    InvalidNumberAcceptances,
    SameValues,
    VulnNotFound,
)
from custom_types import (
    Datetime,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Notification,
)
from db_model.findings.types import (
    Finding,
)
from db_model.users.types import (
    User,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
)
from decimal import (
    Decimal,
)
from mailer import (
    vulnerabilities as vulns_mailer,
)
from newutils import (
    datetime as datetime_utils,
    validations,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Any,
    Awaitable,
    Dict,
    List,
    Optional,
    Tuple,
)


def _validate_acceptance_date(values: Dict[str, str]) -> bool:
    """Check that the date set to temporarily accept a vuln is logical."""
    valid: bool = True
    if values["treatment"] == "ACCEPTED":
        if values.get("acceptance_date"):
            today = datetime_utils.get_now_as_str()
            values[
                "acceptance_date"
            ] = f'{values["acceptance_date"].split()[0]} {today.split()[1]}'
            if not datetime_utils.is_valid_format(values["acceptance_date"]):
                raise InvalidDateFormat()
        else:
            raise InvalidDateFormat()
    return valid


async def _validate_acceptance_days(
    loaders: Any, values: Dict[str, str], organization: str
) -> bool:
    """
    Check that the date during which the finding will be temporarily accepted
    complies with organization settings.
    """
    valid: bool = True
    is_valid_acceptance_date = await in_thread(
        _validate_acceptance_date, values
    )
    if values.get("treatment") == "ACCEPTED" and is_valid_acceptance_date:
        today = datetime_utils.get_now()
        acceptance_date = datetime_utils.get_from_str(
            values["acceptance_date"]
        )
        acceptance_days = Decimal((acceptance_date - today).days)
        organization_data = await loaders.organization.load(organization)
        max_acceptance_days: Optional[Decimal] = organization_data[
            "max_acceptance_days"
        ]
        if (
            max_acceptance_days is not None
            and acceptance_days > max_acceptance_days
        ) or acceptance_days < 0:
            raise InvalidAcceptanceDays(
                "Chosen date is either in the past or exceeds "
                "the maximum number of days allowed by the organization"
            )
    return valid


async def _validate_acceptance_severity(
    loaders: Any, values: Dict[str, str], severity: float, organization_id: str
) -> bool:
    """
    Check that the severity of the finding to temporaryly accept is inside
    the range set by the organization.
    """
    valid: bool = True
    if values.get("treatment") == "ACCEPTED":
        organization_data = await loaders.organization.load(organization_id)
        min_value: Decimal = organization_data["min_acceptance_severity"]
        max_value: Decimal = organization_data["max_acceptance_severity"]
        if not (
            min_value
            <= Decimal(severity).quantize(Decimal("0.1"))
            <= max_value
        ):
            raise InvalidAcceptanceSeverity(str(severity))
    return valid


async def _validate_number_acceptances(
    loaders: Any,
    values: Dict[str, str],
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
    organization_id: str,
) -> bool:
    """
    Check that a finding to temporarily accept does not exceed the maximum
    number of acceptances the organization set.
    """
    valid: bool = True
    if values["treatment"] == "ACCEPTED":
        organization_data = await loaders.organization.load(organization_id)
        max_acceptances: Optional[Decimal] = get_key_or_fallback(
            organization_data,
            "max_number_acceptances",
            "max_number_acceptations",
        )
        current_acceptances: int = sum(
            1
            for item in historic_treatment
            if item.status == VulnerabilityTreatmentStatus.ACCEPTED
        )
        if (
            max_acceptances is not None
            and current_acceptances + 1 > max_acceptances
        ):
            raise InvalidNumberAcceptances(
                str(current_acceptances) if current_acceptances else "-"
            )
    return valid


async def validate_treatment_change(
    finding_severity: float,
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
    loaders: Any,
    organization: str,
    values: Dict[str, str],
) -> bool:
    validate_acceptance_days_coroutine = _validate_acceptance_days(
        loaders, values, organization
    )
    validate_acceptance_severity_coroutine = _validate_acceptance_severity(
        loaders, values, finding_severity, organization
    )
    validate_number_acceptances_coroutine = _validate_number_acceptances(
        loaders,
        values,
        historic_treatment,
        organization,
    )
    return all(
        await collect(
            [
                validate_acceptance_days_coroutine,
                validate_acceptance_severity_coroutine,
                validate_number_acceptances_coroutine,
            ]
        )
    )


async def add_vulnerability_treatment(
    *,
    finding_id: str,
    updated_values: Dict[str, str],
    vuln: Vulnerability,
    user_email: str,
) -> bool:
    new_status = VulnerabilityTreatmentStatus[
        updated_values["treatment"].replace(" ", "_").upper()
    ]
    treatment_to_add = VulnerabilityTreatment(
        acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED
        if new_status == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        else None,
        accepted_until=datetime_utils.convert_to_iso_str(
            updated_values["acceptance_date"]
        )
        if new_status == VulnerabilityTreatmentStatus.ACCEPTED
        else None,
        justification=updated_values.get("justification"),
        assigned=updated_values.get("assigned") or user_email,
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        status=new_status,
    )
    await vulns_model.update_treatment(
        current_value=vuln.treatment,
        finding_id=finding_id,
        vulnerability_id=vuln.id,
        treatment=treatment_to_add,
    )
    return True


def get_treatment_change(
    vulnerability: Vulnerability, min_date: Datetime
) -> Optional[Tuple[str, Vulnerability]]:
    if vulnerability.treatment is not None:
        last_treatment_date = datetime.fromisoformat(
            vulnerability.treatment.modified_date
        )
        if last_treatment_date > min_date:
            treatment = str(vulnerability.treatment.status.value)
            status = (
                f"_{vulnerability.treatment.acceptance_status.value}"
                if vulnerability.treatment.acceptance_status is not None
                else ""
            )
            return treatment + status, vulnerability
        return None
    return None


async def get_treatment_changes(
    loaders: Any,
    vuln: Vulnerability,
) -> int:
    historic: Tuple[
        VulnerabilityTreatment, ...
    ] = await loaders.vulnerability_historic_treatment.load(vuln.id)
    if historic:
        first_treatment = historic[0]
        return (
            len(historic) - 1
            if first_treatment.status == VulnerabilityTreatmentStatus.NEW
            else len(historic)
        )
    return 0


async def _handle_vulnerability_acceptance(
    *,
    loaders: Any,
    finding_id: str,
    new_treatment: VulnerabilityTreatment,
    vulnerability: Vulnerability,
) -> None:
    treatments_to_add: Tuple[VulnerabilityTreatment, ...] = tuple()
    if (
        new_treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.APPROVED
        and vulnerability.treatment
        and vulnerability.treatment.assigned
    ):
        treatments_to_add = (
            new_treatment._replace(assigned=vulnerability.treatment.assigned),
        )
    elif (
        new_treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.REJECTED
    ):
        # Restore previous treatment as request was REJECTED
        treatment_loader = loaders.vulnerability_historic_treatment
        historic_treatment = await treatment_loader.load(vulnerability.id)
        if len(historic_treatment) > 1:
            treatments_to_add = (
                new_treatment,
                historic_treatment[-2]._replace(
                    modified_date=new_treatment.modified_date,
                ),
            )
        else:
            treatments_to_add = (
                new_treatment,
                VulnerabilityTreatment(
                    modified_date=new_treatment.modified_date,
                    status=VulnerabilityTreatmentStatus.NEW,
                    modified_by=new_treatment.modified_by,
                ),
            )

    if treatments_to_add:
        current_value = vulnerability.treatment
        # Use for-await as update order is relevant for typed vuln
        for treatment in vulns_model.utils.adjust_historic_dates(
            treatments_to_add
        ):
            if isinstance(treatment, VulnerabilityTreatment):
                await vulns_model.update_treatment(
                    current_value=current_value,
                    finding_id=finding_id,
                    vulnerability_id=vulnerability.id,
                    treatment=treatment,
                )
                current_value = treatment


async def handle_vulnerabilities_acceptance(
    *,
    loaders: Any,
    accepted_vulns: List[str],
    finding_id: str,
    justification: str,
    rejected_vulns: List[str],
    user_email: str,
) -> None:
    validations.validate_field_length(justification, 10000)
    validations.validate_fields([justification])
    today = datetime_utils.get_iso_date()
    coroutines: List[Awaitable[None]] = []

    all_vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load(finding_id)
    vulnerabilities = tuple(
        vuln
        for vuln in all_vulns
        if vuln.id in accepted_vulns + rejected_vulns
    )
    if not vulnerabilities:
        raise VulnNotFound()
    for vuln in vulnerabilities:
        validate_acceptance(vuln)

    if rejected_vulns:
        rejected_treatment = VulnerabilityTreatment(
            acceptance_status=VulnerabilityAcceptanceStatus.REJECTED,
            justification=justification,
            modified_date=today,
            modified_by=user_email,
            status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
        )
        coroutines.extend(
            [
                _handle_vulnerability_acceptance(
                    loaders=loaders,
                    finding_id=finding_id,
                    new_treatment=rejected_treatment,
                    vulnerability=vuln,
                )
                for vuln in vulnerabilities
                if vuln.id in rejected_vulns
            ]
        )
    if accepted_vulns:
        approved_treatment = VulnerabilityTreatment(
            acceptance_status=VulnerabilityAcceptanceStatus.APPROVED,
            justification=justification,
            modified_date=today,
            modified_by=user_email,
            status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
        )
        coroutines.extend(
            [
                _handle_vulnerability_acceptance(
                    loaders=loaders,
                    finding_id=finding_id,
                    new_treatment=approved_treatment,
                    vulnerability=vuln,
                )
                for vuln in vulnerabilities
                if vuln.id in accepted_vulns
            ]
        )
    await collect(coroutines)


async def send_treatment_change_mail(  # pylint: disable=too-many-arguments
    loaders: Any,
    finding_id: str,
    finding_title: str,
    group_name: str,
    min_date: Datetime,
    modified_by: str,
) -> bool:
    vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load(finding_id)
    changes = list(
        filter(None, [get_treatment_change(vuln, min_date) for vuln in vulns])
    )
    treatments = {change[0] for change in changes}
    for treatment in treatments:
        treatments_change = [
            change for change in changes if change[0] == treatment
        ]
        await should_send_update_treatment(
            loaders=loaders,
            finding_id=finding_id,
            finding_title=finding_title,
            group_name=group_name,
            treatment=treatment,
            updated_vulns=tuple(change[1] for change in treatments_change),
            modified_by=modified_by,
        )
    return bool(treatments)


async def update_vulnerabilities_treatment(
    *,
    loaders: Any,
    finding_id: str,
    updated_values: Dict[str, str],
    organization_id: str,
    finding_severity: float,
    user_email: str,
    vulnerability_id: str,
    group_name: str,
) -> bool:
    if "assigned" not in updated_values:
        updated_values["assigned"] = user_email

    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_all.load(finding_id)
    vulnerability = next(
        iter(vuln for vuln in vulnerabilities if vuln.id == vulnerability_id)
    )
    if (
        "acceptance_date" in updated_values
        and updated_values.get("acceptance_date")
        and len(updated_values["acceptance_date"].split(" ")) == 1
    ):
        today = datetime_utils.get_now_as_str()
        updated_values["acceptance_date"] = (
            f'{updated_values["acceptance_date"].split()[0]}'
            f" {today.split()[1]}"
        )

    if "assigned" in updated_values:
        role: str = await authz.get_group_level_role(user_email, group_name)
        updated_values["assigned"] = await get_valid_assigned(
            assigned=updated_values["assigned"],
            is_manager=role
            in {"user_manager", "customer_manager", "vulnerability_manager"},
            user_email=user_email,
            group_name=group_name,
        )

    validations.validate_fields(list(updated_values.values()))
    if updated_values["treatment"] != "NEW":
        validations.validate_fields([updated_values["justification"]])
        validations.validate_field_length(
            updated_values["justification"], 10000
        )
    if vulnerability.treatment:
        if not compare_historic_treatments(
            vulnerability.treatment, updated_values
        ):
            raise SameValues()

    historic_treatment = await loaders.vulnerability_historic_treatment.load(
        vulnerability.id
    )
    if not await validate_treatment_change(
        finding_severity,
        historic_treatment,
        loaders,
        organization_id,
        updated_values,
    ):
        return False

    return await add_vulnerability_treatment(
        finding_id=finding_id,
        updated_values=updated_values,
        vuln=vulnerability,
        user_email=user_email,
    )


async def validate_and_send_notification_request(
    loaders: Any,
    finding: Finding,
    vulnerabilities: List[str],
) -> bool:
    # Validate finding with vulns in group
    finding_vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_all.load(finding.id)
    assigned_vulns = list(
        vuln
        for vuln in finding_vulns
        for vulnerability_id in vulnerabilities
        if vuln.id == vulnerability_id
    )
    if len(assigned_vulns) != len(vulnerabilities):
        raise InvalidNotificationRequest(
            "Some of the provided vulns ids don't match existing vulns"
        )
    # Validate assigned
    if assigned_vulns[0].treatment:
        assigned = str(assigned_vulns[0].treatment.assigned)
        if assigned is None:
            raise InvalidNotificationRequest(
                "Some of the provided vulns don't have any assigned hackers"
            )
    # Validate recent changes in treatment
    for vuln in assigned_vulns:
        if vuln.treatment:
            if not (
                timedelta(minutes=10)
                > datetime_utils.get_now()
                - datetime.fromisoformat(vuln.treatment.modified_date)
                and vuln.treatment.assigned == assigned
            ):
                raise InvalidNotificationRequest(
                    "Too much time has passed to notify some of these changes"
                )
            if vuln.treatment.assigned != assigned:
                raise InvalidNotificationRequest(
                    "Not all the vulns provided have the same assigned hacker"
                )
    where_str = format_vulnerability_locations(
        list(vuln.where for vuln in assigned_vulns)
    )

    user: User = await loaders.user.load(assigned)
    if (
        Notification.VULNERABILITY_ASSIGNED
        in user.notifications_preferences.email
    ):
        await vulns_mailer.send_mail_assigned_vulnerability(
            loaders=loaders,
            email_to=[assigned],
            is_finding_released=bool(finding.approval),
            group_name=finding.group_name,
            finding_id=finding.id,
            finding_title=finding.title,
            where=where_str,
        )
    return True
