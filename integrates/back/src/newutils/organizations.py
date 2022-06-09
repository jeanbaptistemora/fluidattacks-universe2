from db_model.organizations.constants import (
    ORGANIZATION_ID_PREFIX,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
)


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
