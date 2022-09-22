# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from newutils import (
    organizations as orgs_utils,
)
from organizations import (
    domain as orgs_domain,
)
from schedulers.common import (
    info,
)


async def update_organization_compliance(
    loaders: Dataloaders, organization: Organization
) -> None:
    info(f"Working on organization {organization.name}")
    org_groups: tuple[Group, ...] = await loaders.organization_groups.load(
        organization.id
    )
    info(f"Groups {len(org_groups)}")


async def update_compliance() -> None:
    loaders: Dataloaders = get_new_context()
    async for organization in orgs_domain.iterate_organizations():
        if orgs_utils.is_deleted(organization):
            continue

        await update_organization_compliance(
            loaders=loaders, organization=organization
        )


async def main() -> None:
    await update_compliance()
