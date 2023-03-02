from collections.abc import (
    Iterable,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
)


def is_deleted(organization: Organization) -> bool:
    return organization.state.status == OrganizationStateStatus.DELETED


def filter_active_organizations(
    organizations: Iterable[Organization],
) -> list[Organization]:
    return [
        organization
        for organization in organizations
        if not is_deleted(organization)
    ]
