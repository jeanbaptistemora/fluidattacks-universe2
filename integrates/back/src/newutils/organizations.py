from db_model.organizations.constants import (
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationMetadataToUpdate,
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
    get_now_as_str,
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


def is_deleted(organization: Organization) -> bool:
    return organization.state.status == OrganizationStateStatus.DELETED


def filter_active_organizations(
    organizations: tuple[Organization, ...]
) -> tuple[Organization, ...]:
    return tuple(
        organization
        for organization in organizations
        if not is_deleted(organization)
    )


def format_historic_acceptances(
    item: Item,
) -> tuple[OrganizationPolicies, ...]:
    historic_acceptances: list[dict[str, Any]] = get_key_or_fallback(
        item,
        "historic_max_number_acceptances",
        "historic_max_number_acceptations",
        fallback=[],
    )
    return tuple(
        OrganizationPolicies(
            modified_date=convert_to_iso_str(entry["date"])
            if entry.get("date")
            else convert_to_iso_str(get_now_as_str()),
            modified_by=entry.get("user") or "unknown",
            max_number_acceptances=int(
                get_key_or_fallback(
                    entry, "max_number_acceptances", "max_number_acceptations"
                )
            )
            if get_key_or_fallback(
                entry, "max_number_acceptances", "max_number_acceptations"
            )
            is not None
            else None,
            max_acceptance_severity=None,
            min_acceptance_severity=None,
            min_breaking_severity=None,
        )
        for entry in historic_acceptances
    )


def format_historic_policies(item: Item) -> tuple[OrganizationPolicies, ...]:
    historic_acceptances = get_key_or_fallback(
        item,
        "historic_max_number_acceptances",
        "historic_max_number_acceptations",
        fallback=[],
    )
    last_entry_acceptances = (
        historic_acceptances[-1] if historic_acceptances else {}
    )
    max_number_acceptances = get_key_or_fallback(
        item,
        "max_number_acceptances",
        "max_number_acceptations",
    )

    last_policies_entry = OrganizationPolicies(
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
        modified_date=convert_to_iso_str(last_entry_acceptances["date"])
        if last_entry_acceptances.get("date")
        else convert_to_iso_str(get_now_as_str()),
        modified_by=last_entry_acceptances.get("user") or "unknown",
        vulnerability_grace_period=int(item["vulnerability_grace_period"])
        if item.get("vulnerability_grace_period") is not None
        else None,
    )

    formatted_acceptances = format_historic_acceptances(item)
    return (
        *formatted_acceptances[:-1],
        last_policies_entry,
    )


def format_historic_state(item: Item) -> tuple[OrganizationState, ...]:
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

    historic_state_formatted = [
        OrganizationState(
            modified_by=entry["modified_by"],
            modified_date=convert_to_iso_str(entry["modified_date"]),
            status=OrganizationStateStatus[entry["status"]],
        )
        for entry in historic_state
    ]
    last_state_formatted = OrganizationState(
        status=state_status,
        modified_by=last_entry_state.get("modified_by") or "unknown",
        modified_date=convert_to_iso_str(last_entry_state["modified_date"])
        if last_entry_state.get("modified_date")
        else convert_to_iso_str(get_now_as_str()),
        pending_deletion_date=pending_deletion_date,
    )

    return (
        *historic_state_formatted[:-1],
        last_state_formatted,
    )


def format_organization(item: Item) -> Organization:
    policies = format_historic_policies(item)
    states = format_historic_state(item)
    return Organization(
        billing_customer=item.get("billing_customer"),
        id=item["id"],
        name=item["name"],
        state=states[-1],
        policies=policies[-1],
    )


def format_organization_item(organization: Organization) -> Item:
    organization_id = remove_org_id_prefix(organization.id)
    policies = organization.policies
    return {
        "pk": f"ORG#{organization_id}",
        "sk": f"INFO#{organization.name.lower().strip()}",
        "historic_state": [
            {
                "modified_by": organization.state.modified_by,
                "modified_date": convert_from_iso_str(
                    organization.state.modified_date
                ),
                "status": organization.state.status.value,
            }
        ],
        "max_acceptance_days": policies.max_acceptance_days,
        "max_acceptance_severity": policies.max_acceptance_severity,
        "max_number_acceptances": policies.max_number_acceptances,
        "min_acceptance_severity": policies.min_acceptance_severity,
        "min_breaking_severity": policies.min_breaking_severity,
        "vulnerability_grace_period": policies.vulnerability_grace_period,
        "historic_max_number_acceptances": [
            {
                "date": convert_from_iso_str(policies.modified_date),
                "max_number_acceptations": policies.max_number_acceptances,
                "user": policies.modified_by,
            }
        ],
    }


def format_state_item(org_state: OrganizationState) -> Item:
    return {
        "modified_by": org_state.modified_by,
        "modified_date": convert_from_iso_str(org_state.modified_date),
        "status": org_state.status.value,
    }


def format_policies_item(
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


def format_metadata_item(
    metadata: OrganizationMetadataToUpdate,
) -> Item:
    item = {
        "billing_customer": metadata.billing_customer,
    }
    return {
        key: None if not value else value
        for key, value in item.items()
        if value is not None
    }
