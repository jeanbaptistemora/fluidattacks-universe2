# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import authz
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from group_access import (
    domain as group_access_domain,
)
from organizations import (
    domain as orgs_domain,
)
import pytest

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


async def test_add_group_access() -> None:
    loaders: Dataloaders = get_new_context()
    group_name = "kurome"
    group_users = await group_access_domain.get_group_stakeholders_emails(
        loaders, group_name
    )
    assert len(group_users) == 0

    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"  # NOSONAR
    org_group_names = await orgs_domain.get_group_names(loaders, org_id)
    assert group_name in org_group_names
    await orgs_domain.add_group_access(loaders, org_id, group_name)

    loaders = get_new_context()
    group_users = await group_access_domain.get_group_stakeholders_emails(
        loaders, group_name
    )
    assert len(group_users) == 1
    assert (
        await authz.get_organization_level_role(
            loaders, group_users[0], org_id
        )
        == "customer_manager"
    )
