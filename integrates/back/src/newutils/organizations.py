from db_model.organizations.constants import (
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationPolicies,
    OrganizationPoliciesToUpdate,
    OrganizationState,
)
from dynamodb.types import (
    Item,
)
from newutils.datetime import (
    convert_from_iso_str,
    convert_to_iso_str,
    get_iso_date,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Any,
)

ORGANIZATION_ID_PREFIX = "ORG#"


def add_org_id_prefix(organization_id: str) -> str:
    no_prefix_id = remove_org_id_prefix(organization_id)
    return f"{ORGANIZATION_ID_PREFIX}{no_prefix_id}"


def remove_org_id_prefix(organization_id: str) -> str:
    return organization_id.lstrip(ORGANIZATION_ID_PREFIX)


def is_deleted_typed(organization: Organization) -> bool:
    return organization.state.status == OrganizationStateStatus.DELETED


def is_deleted(organization: dict[str, Any]) -> bool:
    historic_state = organization.get("historic_state", [{}])
    state_status = historic_state[-1].get("status", "")

    return state_status == "DELETED"


def filter_active_organizations_typed(
    organizations: tuple[Organization, ...]
) -> tuple[Organization, ...]:
    return tuple(
        organization
        for organization in organizations
        if not is_deleted_typed(organization)
    )


def filter_active_organizations(
    organizations: tuple[dict[str, Any], ...]
) -> tuple[dict[str, Any], ...]:
    return tuple(
        organization
        for organization in organizations
        if not is_deleted(organization)
    )


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
        max_acceptance_severity=item.get(
            "max_acceptance_severity", DEFAULT_MAX_SEVERITY
        ),
        max_number_acceptances=int(max_number_acceptances)
        if max_number_acceptances is not None
        else None,
        min_acceptance_severity=item.get(
            "min_acceptance_severity", DEFAULT_MIN_SEVERITY
        ),
        min_breaking_severity=item.get(
            "min_breaking_severity", DEFAULT_MIN_SEVERITY
        ),
        modified_date=convert_to_iso_str(last_entry_policies["date"])
        if last_entry_policies.get("date")
        else get_iso_date(),
        modified_by=last_entry_policies.get("user") or "unknown",
        vulnerability_grace_period=int(item["vulnerability_grace_period"])
        if item.get("vulnerability_grace_period") is not None
        else None,
    )


def format_organization_state(item: Item) -> OrganizationState:
    historic_state = item.get("historic_state", [])
    last_entry_state = historic_state[-1] if historic_state else {}
    pending_deletion_date = (
        convert_to_iso_str(item["pending_deletion_date"])
        if item.get("pending_deletion_date")
        else None
    )
    state_status = OrganizationStateStatus[
        last_entry_state.get("status") or "ACTIVE"
    ]

    return OrganizationState(
        status=state_status,
        modified_by=last_entry_state.get("modified_by"),
        modified_date=convert_to_iso_str(last_entry_state["modified_date"])
        if last_entry_state.get("modified_date")
        else None,
        pending_deletion_date=pending_deletion_date,
    )


def format_organization(item: Item) -> Organization:
    return Organization(
        billing_customer=item.get("billing_customer"),
        id=item["id"],
        name=item["name"],
        state=format_organization_state(item),
        policies=format_organization_policies(item),
    )


def format_organization_item(organization: Organization) -> Item:
    organization_id = remove_org_id_prefix(organization.id)
    return {
        "pk": f"ORG#{organization_id}",
        "sk": f"INFO#{organization.name.lower().strip()}",
        "historic_state": [
            {
                "modified_by": organization.state.modified_by,
                "modified_date": convert_from_iso_str(
                    organization.state.modified_date
                )
                if organization.state.modified_date
                else None,
                "status": organization.state.status.value,
            }
        ],
    }


def format_org_policies_item(
    historic: list[Item],
    modified_by: str,
    modified_date: str,
    policies: OrganizationPoliciesToUpdate,
) -> Item:
    if policies.max_number_acceptances is not None:
        historic.append(
            {
                "date": convert_from_iso_str(modified_date),
                "max_number_acceptations": policies.max_number_acceptances,
                "user": modified_by,
            }
        )
    item = {
        "max_acceptance_days": policies.max_acceptance_days,
        "max_acceptance_severity": policies.max_acceptance_severity,
        "min_acceptance_severity": policies.min_acceptance_severity,
        "min_breaking_severity": policies.min_breaking_severity,
        "vulnerability_grace_period": policies.vulnerability_grace_period,
        "historic_max_number_acceptances": historic,
        "max_number_acceptances": policies.max_number_acceptances,
    }

    return {
        key: None if not value else value
        for key, value in item.items()
        if value is not None
    }
