from .core import (
    should_send_update_treatment,
)
from .utils import (
    compare_historic_treatments,
    validate_acceptance,
    validate_treatment_manager,
)
from aioextensions import (
    collect,
    in_thread,
)
import authz
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidNumberAcceptances,
    SameValues,
    VulnNotFound,
)
from custom_types import (
    Datetime,
    Historic,
)
from datetime import (
    datetime,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
)
from decimal import (
    Decimal,
)
from newutils import (
    datetime as datetime_utils,
    findings as finding_utils,
    validations,
    vulnerabilities as vulns_utils,
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
from vulnerabilities import (
    dal as vulns_dal,
)


async def _validate_acceptance_days(
    loaders: Any, values: Dict[str, str], organization: str
) -> bool:
    """
    Check that the date during which the finding will be temporarily accepted
    complies with organization settings
    """
    valid: bool = True
    is_valid_acceptance_date = await in_thread(
        finding_utils.validate_acceptance_date, values
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
    the range set by the organization
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
    number of acceptances the organization set
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
    date: str,
) -> bool:
    updated_values = vulns_utils.update_treatment_values(updated_values)
    new_treatment = updated_values["treatment"]
    new_state = {
        "date": date,
        "treatment": new_treatment,
    }

    if user_email:
        new_state["user"] = user_email
        new_state["treatment_manager"] = user_email
    if "treatment_manager" in updated_values:
        new_state["treatment_manager"] = updated_values["treatment_manager"]
    if new_treatment != "NEW":
        validations.validate_fields([updated_values["justification"]])
        validations.validate_field_length(
            updated_values["justification"], 5000
        )
        new_state["justification"] = updated_values["justification"]

    if new_treatment == "ACCEPTED":
        new_state["acceptance_date"] = updated_values["acceptance_date"]
    elif new_treatment == "ACCEPTED_UNDEFINED":
        new_state["acceptance_status"] = updated_values["acceptance_status"]

    await vulns_dal.append(
        finding_id=finding_id,
        vulnerability_id=vuln.id,
        elements={"historic_treatment": (new_state,)},
    )
    return True


def get_treatment_change(
    vulnerability: Vulnerability, min_date: Datetime
) -> Optional[Tuple[str, Vulnerability]]:
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


async def handle_vuln_acceptance(
    *,
    finding_id: str,
    new_treatments: Historic,
    vuln: Vulnerability,
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
) -> bool:
    if (
        historic_treatment
        and new_treatments[-1].get("acceptance_status") == "APPROVED"
        and vuln.treatment
        and vuln.treatment.manager
    ):
        new_treatments[-1]["treatment_manager"] = vuln.treatment.manager

    if new_treatments[-1].get("acceptance_status") == "REJECTED":
        if len(historic_treatment) > 1:
            new_treatments.append(
                vulns_utils.format_vulnerability_treatment_item(
                    historic_treatment[-2]
                )
            )
        else:
            new_treatments.append(
                {
                    "treatment": "NEW",
                    "date": datetime_utils.get_now_as_str(),
                    "user": new_treatments[-1]["user"],
                }
            )

    await vulns_dal.append(
        finding_id=finding_id,
        vulnerability_id=vuln.id,
        elements={"historic_treatment": new_treatments},
    )
    return True


async def handle_vulnerabilities_acceptance(
    *,
    loaders: Any,
    accepted_vulns: List[str],
    finding_id: str,
    justification: str,
    rejected_vulns: List[str],
    user_email: str,
) -> bool:
    validations.validate_field_length(justification, 5000)
    validations.validate_fields([justification])
    today = datetime_utils.get_now_as_str()
    coroutines: List[Awaitable[bool]] = []

    all_vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulns_typed.load(finding_id)
    vulnerabilities = tuple(
        vuln
        for vuln in all_vulns
        if vuln.id in accepted_vulns + rejected_vulns
    )
    historics = await loaders.vulnerability_historic_treatment.load_many(
        [vuln.id for vuln in vulnerabilities]
    )
    if not vulnerabilities:
        raise VulnNotFound()

    for vuln in vulnerabilities:
        validate_acceptance(vuln)

    new_treatment = {
        "treatment": "ACCEPTED_UNDEFINED",
        "justification": justification,
        "user": user_email,
        "date": today,
    }
    if rejected_vulns:
        treatments = [{**new_treatment, "acceptance_status": "REJECTED"}]
        coroutines.extend(
            [
                handle_vuln_acceptance(
                    finding_id=finding_id,
                    new_treatments=treatments,
                    vuln=vuln,
                    historic_treatment=historic_treatment,
                )
                for vuln, historic_treatment in zip(vulnerabilities, historics)
                if vuln.id in rejected_vulns
            ]
        )
    if accepted_vulns:
        treatments = [{**new_treatment, "acceptance_status": "APPROVED"}]
        coroutines.extend(
            [
                handle_vuln_acceptance(
                    finding_id=finding_id,
                    new_treatments=treatments,
                    vuln=vuln,
                    historic_treatment=historic_treatment,
                )
                for vuln, historic_treatment in zip(vulnerabilities, historics)
                if vuln.id in accepted_vulns
            ]
        )
    return all(await collect(coroutines))


async def send_treatment_change_mail(
    loaders: Any,
    finding_id: str,
    finding_title: str,
    group_name: str,
    min_date: Datetime,
) -> bool:
    vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulns_nzr_typed.load(finding_id)
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
    success: bool = False
    if (
        updated_values.get("treatment") in {"ACCEPTED_UNDEFINED", "ACCEPTED"}
        and "treatment_manager" not in updated_values
    ):
        updated_values["treatment_manager"] = user_email

    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulns_all_typed.load(finding_id)
    vulnerability = next(
        iter(vuln for vuln in vulnerabilities if vuln.id == vulnerability_id)
    )
    today = datetime_utils.get_now_as_str()
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

    if "treatment_manager" in updated_values:
        role: str = await authz.get_group_level_role(user_email, group_name)
        updated_values["treatment_manager"] = await validate_treatment_manager(
            treatment_manager=updated_values["treatment_manager"],
            is_customer_admin=role
            in {"customeradmin", "system_owner", "group_manager"},
            user_email=user_email,
            group_name=group_name,
        )

    validations.validate_fields(list(updated_values.values()))
    if compare_historic_treatments(vulnerability.treatment, updated_values):
        historic_treatment = (
            await loaders.vulnerability_historic_treatment.load(
                vulnerability.id
            )
        )
        if await validate_treatment_change(
            finding_severity,
            historic_treatment,
            loaders,
            organization_id,
            updated_values,
        ):
            success = await add_vulnerability_treatment(
                finding_id=finding_id,
                updated_values=updated_values,
                vuln=vulnerability,
                user_email=user_email,
                date=today,
            )
    else:
        raise SameValues()

    return success
