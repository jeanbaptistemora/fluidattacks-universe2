# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
)


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
