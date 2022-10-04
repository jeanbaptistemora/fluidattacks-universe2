# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import authz
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import pytest
from unittest import (
    mock,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["email", "role"],
    [
        ["continuoushacking@gmail.com", "hacker"],
        ["integratesuser2@gmail.com", "user"],
        ["integrateshacker@fluidattacks.com", "hacker"],
    ],
)
async def test_get_user_level_actions_model(email: str, role: str) -> None:
    loaders: Dataloaders = get_new_context()
    with mock.patch(
        "authz.enforcer.get_user_level_role", new_callable=mock.AsyncMock
    ) as mock_get_user_level_role:
        mock_get_user_level_role.return_value = role
        assert await authz.get_user_level_actions(
            loaders, email
        ) == authz.get_user_level_roles_model(email).get(role, {}).get(
            "actions"
        )
    assert mock_get_user_level_role.called is True


@pytest.mark.parametrize(
    ["email", "group"],
    [
        ["continuoushacking@gmail.com", "UnItTeStInG"],
        ["continuoushacking@gmail.com", "unittesting"],
        ["continuoushacking@gmail.com", "oneshottest"],
        ["integrateshacker@fluidattacks.com", "unittesting"],
        ["integrateshacker@fluidattacks.com", "oneshottest"],
        ["integratesuser@gmail.com", "unittesting"],
        ["integratesuser@gmail.com", "oneshottest"],
    ],
)
async def test_get_group_level_actions_model(email: str, group: str) -> None:
    loaders: Dataloaders = get_new_context()
    group_level_role = await authz.get_group_level_role(loaders, email, group)

    assert await authz.get_group_level_actions(
        loaders, email, group
    ) == authz.get_group_level_roles_model(email).get(
        group_level_role, {}
    ).get(
        "actions"
    )


@pytest.mark.parametrize(
    ["email", "organization_id"],
    [
        [
            "org_testgroupmanager1@gmail.com",
            "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
        ],
        [
            "unittest2@fluidattacks.com",
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        ],
    ],
)
async def test_get_organization_level_actions_model(
    email: str, organization_id: str
) -> None:
    loaders: Dataloaders = get_new_context()
    organization_level_role = await authz.get_organization_level_role(
        loaders, email, organization_id
    )

    assert await authz.get_organization_level_actions(
        loaders, email, organization_id
    ) == authz.get_organization_level_roles_model(email).get(
        organization_level_role, {}
    ).get(
        "actions"
    )
