# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    InvalidUserProvided,
)
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


@pytest.mark.changes_db
async def test_add_customer_manager_fail() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    user = "org_testgroupmanager2@gmail.com"
    assert not await orgs_domain.has_access(loaders, org_id, user)

    try:
        await orgs_domain.add_stakeholder(
            loaders, org_id, user, "customer_manager"
        )
    except InvalidUserProvided as ex:
        assert (
            str(ex)
            == "Exception - This role can only be granted to Fluid Attacks "
            "users"
        )

    loaders = get_new_context()
    group_names = await orgs_domain.get_group_names(loaders, org_id)
    groups_users = await collect(
        group_access_domain.get_group_stakeholders_emails(loaders, group)
        for group in group_names
    )
    assert all(user not in group_users for group_users in groups_users)
