from aioextensions import (
    collect,
    schedule,
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
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model import (
    utils as db_model_utils,
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Notification,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.stakeholders.types import (
    Stakeholder,
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
from group_access import (
    domain as group_access_domain,
)
from itertools import (
    islice,
)
from mailer import (
    vulnerabilities as vulns_mailer,
)
from newutils import (
    datetime as datetime_utils,
    validations,
)
from newutils.groups import (
    get_group_max_acceptance_days,
    get_group_max_acceptance_severity,
    get_group_max_number_acceptances,
    get_group_min_acceptance_severity,
)
from newutils.vulnerabilities import (
    validate_closed,
)
from typing import (
    Optional,
)
from vulnerabilities.domain.core import (
    should_send_update_treatment,
)
from vulnerabilities.domain.utils import (
    compare_historic_treatments,
    format_vulnerability_locations,
    get_valid_assigned,
    validate_acceptance,
)


def _validate_acceptance_date(values: dict[str, str]) -> None:
    """Check that the date set to temporarily accept a vuln is logical."""
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


async def _validate_acceptance_days(
    loaders: Dataloaders, values: dict[str, str], group_name: str
) -> None:
    """
    Check that the date during which the finding will be temporarily accepted
    complies with organization settings.
    """
    _validate_acceptance_date(values)
    if values.get("treatment") == "ACCEPTED":
        today = datetime_utils.get_now()
        acceptance_date = datetime_utils.get_from_str(
            values["acceptance_date"]
        )
        acceptance_days = Decimal((acceptance_date - today).days)
        group: Group = await loaders.group.load(group_name)
        max_acceptance_days = await get_group_max_acceptance_days(
            loaders=loaders, group=group
        )
        if (
            max_acceptance_days is not None
            and acceptance_days > max_acceptance_days
        ) or acceptance_days < 0:
            raise InvalidAcceptanceDays(
                "Chosen date is either in the past or exceeds "
                "the maximum number of days allowed by the defined policy"
            )


async def _validate_acceptance_severity(
    loaders: Dataloaders,
    values: dict[str, str],
    severity: float,
    group_name: str,
) -> None:
    """
    Check that the severity of the finding to temporaryly accept is inside
    the range set by the defined policy.
    """
    if values.get("treatment") == "ACCEPTED":
        group: Group = await loaders.group.load(group_name)
        min_value: Decimal = await get_group_min_acceptance_severity(
            loaders=loaders,
            group=group,
        )
        max_value: Decimal = await get_group_max_acceptance_severity(
            loaders=loaders,
            group=group,
        )
        if not (
            min_value
            <= Decimal(severity).quantize(Decimal("0.1"))
            <= max_value
        ):
            raise InvalidAcceptanceSeverity(str(severity))


async def _validate_number_acceptances(
    loaders: Dataloaders,
    values: dict[str, str],
    historic_treatment: tuple[VulnerabilityTreatment, ...],
    group_name: str,
) -> None:
    """
    Check that a finding to temporarily accept does not exceed the maximum
    number of acceptances the organization set.
    """
    if values["treatment"] == "ACCEPTED":
        group: Group = await loaders.group.load(group_name)
        max_acceptances = await get_group_max_number_acceptances(
            loaders=loaders,
            group=group,
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


async def validate_treatment_change(
    *,
    finding_severity: float,
    group_name: str,
    historic_treatment: tuple[VulnerabilityTreatment, ...],
    loaders: Dataloaders,
    values: dict[str, str],
) -> None:
    await collect(
        [
            _validate_acceptance_days(loaders, values, group_name),
            _validate_acceptance_severity(
                loaders, values, finding_severity, group_name
            ),
            _validate_number_acceptances(
                loaders,
                values,
                historic_treatment,
                group_name,
            ),
        ]
    )


async def add_vulnerability_treatment(
    *,
    finding_id: str,
    updated_values: dict[str, str],
    vuln: Vulnerability,
    user_email: str,
) -> None:
    new_status = VulnerabilityTreatmentStatus[
        updated_values["treatment"].replace(" ", "_").upper()
    ]
    treatment_to_add = VulnerabilityTreatment(
        acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED
        if new_status == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        else None,
        accepted_until=datetime.fromisoformat(
            updated_values["acceptance_date"]
        ).astimezone(tz=timezone.utc)
        if new_status == VulnerabilityTreatmentStatus.ACCEPTED
        else None,
        justification=updated_values.get("justification"),
        assigned=updated_values.get("assigned") or user_email,
        modified_by=user_email,
        modified_date=datetime_utils.get_utc_now(),
        status=new_status,
    )
    await vulns_model.update_treatment(
        current_value=vuln,
        finding_id=finding_id,
        vulnerability_id=vuln.id,
        treatment=treatment_to_add,
    )


def get_treatment_change(
    vulnerability: Vulnerability, min_date: datetime
) -> Optional[tuple[str, Vulnerability]]:
    if vulnerability.treatment is not None:
        last_treatment_date = vulnerability.treatment.modified_date
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
    loaders: Dataloaders,
    vuln: Vulnerability,
) -> int:
    historic: tuple[
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
    loaders: Dataloaders,
    finding_id: str,
    new_treatment: VulnerabilityTreatment,
    vulnerability: Vulnerability,
) -> None:
    treatments_to_add: tuple[VulnerabilityTreatment, ...] = tuple()
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
        current_value = vulnerability
        # Use for-await as update order is relevant for typed vuln
        for treatment in db_model_utils.adjust_historic_dates_datetime(
            treatments_to_add
        ):
            if isinstance(treatment, VulnerabilityTreatment):
                await vulns_model.update_treatment(
                    current_value=current_value,
                    finding_id=finding_id,
                    vulnerability_id=vulnerability.id,
                    treatment=treatment,
                )
                current_value = current_value._replace(treatment=treatment)

        if (
            new_treatment.acceptance_status
            == VulnerabilityAcceptanceStatus.APPROVED
        ):
            schedule(
                send_treatment_report_mail(
                    loaders=loaders,
                    modified_by=new_treatment.modified_by,
                    justification=new_treatment.justification,
                    vulnerability_id=vulnerability.id,
                    is_approved=True,
                )
            )


async def handle_vulnerabilities_acceptance(
    *,
    loaders: Dataloaders,
    accepted_vulns: list[str],
    finding_id: str,
    justification: str,
    rejected_vulns: list[str],
    user_email: str,
) -> None:
    validations.validate_field_length(justification, 10000)
    validations.validate_fields([justification])
    today = datetime_utils.get_utc_now()

    all_vulns: tuple[
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
        await collect(
            tuple(
                _handle_vulnerability_acceptance(
                    loaders=loaders,
                    finding_id=finding_id,
                    new_treatment=rejected_treatment,
                    vulnerability=vuln,
                )
                for vuln in vulnerabilities
                if vuln.id in rejected_vulns
            ),
            workers=40,
        )
    if accepted_vulns:
        approved_treatment = VulnerabilityTreatment(
            acceptance_status=VulnerabilityAcceptanceStatus.APPROVED,
            justification=justification,
            modified_date=today,
            modified_by=user_email,
            status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
        )
        await collect(
            tuple(
                _handle_vulnerability_acceptance(
                    loaders=loaders,
                    finding_id=finding_id,
                    new_treatment=approved_treatment,
                    vulnerability=vuln,
                )
                for vuln in vulnerabilities
                if vuln.id in accepted_vulns
            ),
            workers=100,
        )


async def send_treatment_change_mail(
    *,
    loaders: Dataloaders,
    assigned: str,
    finding_id: str,
    finding_title: str,
    group_name: str,
    justification: str,
    min_date: datetime,
    modified_by: str,
) -> bool:
    vulns: tuple[
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
            assigned=assigned,
            finding_id=finding_id,
            finding_title=finding_title,
            group_name=group_name,
            justification=justification,
            treatment=treatment,
            updated_vulns=tuple(change[1] for change in treatments_change),
            modified_by=modified_by,
        )
    return bool(treatments)


async def send_treatment_report_mail(
    *,
    loaders: Dataloaders,
    modified_by: Optional[str],
    justification: Optional[str],
    vulnerability_id: str,
    is_approved: bool = False,
) -> None:
    old_vuln_values: Vulnerability = await loaders.vulnerability.load(
        vulnerability_id
    )
    finding: Finding = await loaders.finding.load(old_vuln_values.finding_id)
    roles: set[str] = {
        "resourcer",
        "customer_manager",
        "user_manager",
        "vulnerability_manager",
    }
    users_email = (
        await group_access_domain.get_stakeholders_email_by_preferences(
            loaders=loaders,
            group_name=finding.group_name,
            notification=Notification.UPDATED_TREATMENT,
            roles=roles,
        )
    )
    managers_email = await get_managers_by_size(loaders, finding.group_name, 3)
    await vulns_mailer.send_mail_treatment_report(
        loaders=loaders,
        finding_id=old_vuln_values.finding_id,
        finding_title=finding.title,
        group_name=finding.group_name,
        justification=justification,
        managers_email=managers_email,
        modified_by=modified_by,
        modified_date=datetime_utils.get_utc_now(),
        location=old_vuln_values.state.where,
        email_to=users_email,
        is_approved=is_approved,
    )


async def get_managers_by_size(
    loaders: Dataloaders, group_name: str, list_size: int
) -> list[str]:
    """Returns a list of managers with an specific length for the array"""
    managers = list(
        islice(
            await group_access_domain.get_managers(loaders, group_name),
            list_size,
        )
    )
    return managers


async def update_vulnerabilities_treatment(
    *,
    loaders: Dataloaders,
    finding_id: str,
    updated_values: dict[str, str],
    finding_severity: float,
    user_email: str,
    vulnerability_id: str,
    group_name: str,
) -> None:
    if "assigned" not in updated_values:
        updated_values["assigned"] = user_email

    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_all.load(finding_id)
    vulnerability = next(
        iter(vuln for vuln in vulnerabilities if vuln.id == vulnerability_id)
    )
    validate_closed(vulnerability)
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
        role: str = await authz.get_group_level_role(
            loaders, user_email, group_name
        )
        updated_values["assigned"] = await get_valid_assigned(
            loaders=loaders,
            assigned=updated_values["assigned"],
            is_manager=role
            in {"user_manager", "customer_manager", "vulnerability_manager"},
            email=user_email,
            group_name=group_name,
        )

    validations.validate_fields(list(updated_values.values()))
    if updated_values["treatment"] != "NEW":
        validations.validate_fields([updated_values["justification"]])
        validations.validate_field_length(
            updated_values["justification"], 10000
        )
    if vulnerability.treatment and not compare_historic_treatments(
        vulnerability.treatment, updated_values
    ):
        raise SameValues()

    historic_treatment = await loaders.vulnerability_historic_treatment.load(
        vulnerability.id
    )
    await validate_treatment_change(
        finding_severity=finding_severity,
        group_name=group_name,
        historic_treatment=historic_treatment,
        loaders=loaders,
        values=updated_values,
    )
    await add_vulnerability_treatment(
        finding_id=finding_id,
        updated_values=updated_values,
        vuln=vulnerability,
        user_email=user_email,
    )


async def validate_and_send_notification_request(
    loaders: Dataloaders,
    finding: Finding,
    responsible: str,
    vulnerabilities: list[str],
) -> None:
    # Validate finding with vulns in group
    finding_vulns: tuple[
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
        if not assigned:
            raise InvalidNotificationRequest(
                "Some of the provided vulns don't have any assigned hackers"
            )
    # Validate recent changes in treatment
    for vuln in assigned_vulns:
        if vuln.treatment:
            if not (
                timedelta(minutes=10)
                > datetime_utils.get_utc_now() - vuln.treatment.modified_date
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
        list(vuln.state.where for vuln in assigned_vulns)
    )

    stakeholder: Stakeholder = await loaders.stakeholder.load(assigned)
    if (
        Notification.VULNERABILITY_ASSIGNED
        in stakeholder.state.notifications_preferences.email
    ):
        await vulns_mailer.send_mail_assigned_vulnerability(
            loaders=loaders,
            email_to=[assigned],
            is_finding_released=bool(finding.approval),
            group_name=finding.group_name,
            finding_id=finding.id,
            finding_title=finding.title,
            responsible=responsible,
            where=where_str,
        )
