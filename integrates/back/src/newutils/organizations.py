from db_model.organization.constants import (
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
from db_model.organization.types import (
    Organization,
    OrganizationPolicies,
    OrganizationState,
)
from dynamodb.types import (
    Item,
)
from newutils.datetime import (
    convert_to_iso_str,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Any,
    Optional,
)


def is_deleted(organization: dict[str, Any]) -> bool:
    historic_state = organization.get("historic_state", [{}])
    state_status = historic_state[-1].get("status", "")

    return state_status == "DELETED"


def filter_active_organizations(
    organizations: tuple[dict[str, Any], ...]
) -> tuple[dict[str, Any], ...]:
    return tuple(
        organization
        for organization in organizations
        if not is_deleted(organization)
    )


def format_historic_policies(
    item: Optional[list[Item]],
) -> OrganizationPolicies:
    if item:
        organization_historic_policies = item[-1]
        return OrganizationPolicies(
            modified_date=(
                convert_to_iso_str(organization_historic_policies["date"])
            ),
            modified_by=organization_historic_policies["user"],
            max_number_acceptations=int(
                get_key_or_fallback(
                    organization_historic_policies,
                    "max_number_acceptances",
                    "max_number_acceptations",
                )
            ),
        )
    return None


def format_historic_state(
    item: Optional[list[Item]],
) -> OrganizationState:
    if item:
        organization_state = item[-1]
        return OrganizationState(
            modified_date=(
                convert_to_iso_str(organization_state["modified_date"])
            ),
            modified_by=organization_state["modified_by"],
            max_number_acceptations=organization_state["status"],
        )
    return None


def format_organization(
    item: Item,
    organization_id: str,
) -> Organization:
    historic_policies = format_historic_policies(
        item["historic_max_number_acceptances"]
        if item.get("historic_max_number_acceptances")
        else item["historic_max_number_acceptations"]
    )
    historic_state = format_historic_state(item.get("historic_state", None))
    return Organization(
        id=organization_id,
        name=item["name"],
        historic_policies=historic_policies,
        historic_status=historic_state,
        billing_customer=item.get("billing_customer", None),
        pending_deletion_date=(
            convert_to_iso_str(item.get("pending_deletion_date", None))
        ),
        max_acceptance_days=int(item.get("max_acceptance_days", None)),
        max_acceptance_severity=item.get(
            "max_acceptance_severity", DEFAULT_MAX_SEVERITY
        ),
        min_acceptance_severity=item.get(
            "min_acceptance_severity", DEFAULT_MIN_SEVERITY
        ),
        min_breaking_severity=item.get(
            "min_breaking_severity", DEFAULT_MIN_SEVERITY
        ),
        vulnerability_grace_period=int(
            item.get("vulnerability_grace_period", None)
        ),
    )
