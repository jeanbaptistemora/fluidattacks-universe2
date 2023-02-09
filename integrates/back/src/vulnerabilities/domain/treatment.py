from aioextensions import (
    collect,
    schedule,
)
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidNotificationRequest,
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
    vulnerabilities as vulns_utils,
)
from stakeholders.domain import (
    get_stakeholder,
)
from typing import (
    Optional,
)
from vulnerabilities.domain.core import (
    should_send_update_treatment,
)
from vulnerabilities.domain.utils import (
    format_vulnerability_locations,
    get_finding,
    get_valid_assigned,
    validate_acceptance,
)
from vulnerabilities.domain.validations import (
    validate_accepted_treatment_change,
)
from vulnerabilities.types import (
    VulnerabilityTreatmentToUpdate,
)


async def add_vulnerability_treatment(
    *,
    modified_by: str,
    vulnerability: Vulnerability,
    treatment: VulnerabilityTreatmentToUpdate,
) -> None:
    await vulns_model.update_treatment(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        treatment=VulnerabilityTreatment(
            acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED
            if treatment.status
            == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
            else None,
            accepted_until=treatment.accepted_until,
            justification=treatment.justification,
            assigned=treatment.assigned or modified_by,
            modified_by=modified_by,
            modified_date=datetime_utils.get_utc_now(),
            status=treatment.status,
        ),
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
            if first_treatment.status == VulnerabilityTreatmentStatus.UNTREATED
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
                    status=VulnerabilityTreatmentStatus.UNTREATED,
                    modified_by=new_treatment.modified_by,
                ),
            )

    if treatments_to_add:
        current_value = vulnerability
        # Use for-await as update order is relevant for typed vuln
        for treatment in db_model_utils.adjust_historic_dates(
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


@validations.validate_field_length_deco("justification", limit=10000)
@validations.validate_fields_deco(["justification"])
async def handle_vulnerabilities_acceptance(
    *,
    loaders: Dataloaders,
    accepted_vulns: list[str],
    finding_id: str,
    justification: str,
    rejected_vulns: list[str],
    user_email: str,
) -> None:
    today = datetime_utils.get_utc_now()

    all_vulns = await loaders.finding_vulnerabilities.load(finding_id)
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
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
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
    old_vuln_values: Optional[
        Vulnerability
    ] = await loaders.vulnerability.load(vulnerability_id)
    if old_vuln_values:
        finding = await get_finding(loaders, old_vuln_values.finding_id)
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
        managers_email = await get_managers_by_size(
            loaders, finding.group_name, 3
        )
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
    else:
        raise VulnNotFound()


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


@validations.validate_fields_deco(
    ["treatment.justification", "treatment.assigned"]
)
@validations.validate_field_length_deco("treatment.justification", limit=10000)
async def update_vulnerabilities_treatment(
    *,
    loaders: Dataloaders,
    finding: Finding,
    finding_severity: Decimal,
    modified_by: str,
    vulnerability_id: str,
    treatment: VulnerabilityTreatmentToUpdate,
) -> None:
    vulnerability: Vulnerability = await loaders.vulnerability.load(
        vulnerability_id
    )
    vulns_utils.validate_closed(vulnerability)
    if vulnerability.finding_id != finding.id:
        raise VulnNotFound()
    valid_assigned = await get_valid_assigned(
        loaders=loaders,
        assigned=treatment.assigned or modified_by,
        email=modified_by,
        group_name=finding.group_name,
    )
    if (
        vulnerability.treatment
        and vulnerability.treatment.status == treatment.status
        and vulnerability.treatment.justification == treatment.justification
        and vulnerability.treatment.assigned == valid_assigned
        and vulnerability.treatment.accepted_until == treatment.accepted_until
    ):
        raise SameValues()

    if treatment.status == VulnerabilityTreatmentStatus.ACCEPTED:
        if not treatment.accepted_until:
            raise InvalidAcceptanceDays("Acceptance parameter missing")
        historic_treatment = (
            await loaders.vulnerability_historic_treatment.load(
                vulnerability.id
            )
        )
        await validate_accepted_treatment_change(
            loaders=loaders,
            accepted_until=treatment.accepted_until,
            finding_severity=finding_severity,
            group_name=finding.group_name,
            historic_treatment=historic_treatment,
        )

    await add_vulnerability_treatment(
        modified_by=modified_by,
        treatment=treatment._replace(assigned=valid_assigned),
        vulnerability=vulnerability,
    )


async def validate_and_send_notification_request(
    loaders: Dataloaders,
    finding: Finding,
    responsible: str,
    vulnerabilities: list[str],
) -> None:
    # Validate finding with vulns in group
    finding_vulns: list[
        Vulnerability
    ] = await loaders.finding_vulnerabilities_all.load(finding.id)
    assigned_vulns: list[Vulnerability] = list(
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
        justification = str(assigned_vulns[0].treatment.justification)
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

    stakeholder = await get_stakeholder(loaders, assigned)
    await send_treatment_change_mail(
        loaders=loaders,
        assigned=assigned,
        finding_id=finding.id,
        finding_title=finding.title,
        group_name=finding.group_name,
        justification=justification,
        min_date=datetime.now(timezone.utc) - timedelta(days=1),
        modified_by=responsible,
    )
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
