from .constants import (
    ORGANIZATION_ID_PREFIX,
)
from .types import (
    Organization,
    OrganizationPolicies,
    OrganizationState,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from dynamodb.types import (
    Item,
)


def add_org_id_prefix(organization_id: str) -> str:
    no_prefix_id = remove_org_id_prefix(organization_id)
    return f"{ORGANIZATION_ID_PREFIX}{no_prefix_id}"


def remove_org_id_prefix(organization_id: str) -> str:
    return organization_id.lstrip(ORGANIZATION_ID_PREFIX)


def format_organization(item: Item) -> Organization:
    return Organization(
        billing_customer=item.get("billing_customer"),
        id=add_org_id_prefix(item["id"]),
        name=item["name"],
        policies=format_policies(item["policies"]),
        state=format_state(item["state"]),
    )


def format_policies(policies: Item) -> OrganizationPolicies:
    return OrganizationPolicies(
        max_acceptance_days=int(policies["max_acceptance_days"]),
        max_acceptance_severity=policies["max_acceptance_severity"],
        max_number_acceptances=int(policies["max_number_acceptances"]),
        min_acceptance_severity=policies["min_acceptance_severity"],
        min_breaking_severity=policies["min_breaking_severity"],
        modified_date=policies["modified_date"],
        modified_by=policies["modified_by"],
        vulnerability_grace_period=int(policies["vulnerability_grace_period"]),
    )


def format_state(state: Item) -> OrganizationState:
    return OrganizationState(
        status=OrganizationStateStatus[state["status"]],
        modified_by=state["modified_by"],
        modified_date=state["modified_date"],
        pending_deletion_date=state.get("pending_deletion_date"),
    )
