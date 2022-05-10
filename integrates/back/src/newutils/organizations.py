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
            status=organization_state["status"],
        )

    return None


def format_organization_policies(item: Item) -> OrganizationPolicies:
    historic_policies = get_key_or_fallback(
        item,
        "historic_max_number_acceptances",
        "historic_max_number_acceptations",
        fallback=[],
    )
    last_entry_policies = historic_policies[-1] if historic_policies else {}
    max_number_acceptances = get_key_or_fallback(
        last_entry_policies,
        "max_number_acceptances",
        "max_number_acceptations",
    )

    return OrganizationPolicies(
        max_acceptance_days=int(item["max_acceptance_days"])
        if item.get("max_acceptance_days") is not None
        else None,
        max_acceptance_severity=item.get("max_acceptance_severity"),
        max_number_acceptances=int(max_number_acceptances)
        if max_number_acceptances is not None
        else None,
        min_acceptance_severity=item.get("min_acceptance_severity"),
        min_breaking_severity=item.get("min_breaking_severity"),
        modified_date=convert_to_iso_str(last_entry_policies["date"])
        if last_entry_policies.get("date")
        else None,
        modified_by=last_entry_policies.get("user"),
        vulnerability_grace_period=int(item["vulnerability_grace_period"])
        if item.get("vulnerability_grace_period") is not None
        else None,
    )


def format_organization(item: Item) -> Organization:
    historic_state = format_historic_state(item.get("historic_state"))

    return Organization(
        id=item["id"],
        name=item["name"],
        state=historic_state,
        billing_customer=item.get("billing_customer"),
        pending_deletion_date=(
            convert_to_iso_str(item["pending_deletion_date"])
            if item.get("pending_deletion_date")
            else None
        ),
        policies=format_organization_policies(item),
    )
