# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
    get_new_context,
)
from group_access.domain import (
    exists,
    get_group_stakeholders_emails,
    get_managers,
    get_reattackers,
    remove_access,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_exists() -> None:
    loaders: Dataloaders = get_new_context()
    email = "unittest@fluidattacks.com"
    group_name = "unittesting"
    assert await exists(loaders, group_name, email)


async def test_get_group_stakeholders_emails() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    users = await get_group_stakeholders_emails(loaders, group_name)
    expected = [
        "continuoushack2@gmail.com",
        "continuoushacking@gmail.com",
        "customer_manager@fluidattacks.com",
        "forces.unittesting@fluidattacks.com",
        "integrateshacker@fluidattacks.com",
        "integratesmanager@fluidattacks.com",
        "integratesmanager@gmail.com",
        "integratesreattacker@fluidattacks.com",
        "integratesresourcer@fluidattacks.com",
        "integratesreviewer@fluidattacks.com",
        "integratesserviceforces@fluidattacks.com",
        "integratesuser2@fluidattacks.com",
        "integratesuser2@gmail.com",
        "integratesuser@gmail.com",
        "unittest2@fluidattacks.com",
        "unittest@fluidattacks.com",
        "vulnmanager@gmail.com",
    ]
    for user in expected:
        assert user in users


async def test_get_managers() -> None:
    group_name = "unittesting"
    expected_output = [
        "continuoushack2@gmail.com",
        "continuoushacking@gmail.com",
        "integratesuser@gmail.com",
        "vulnmanager@gmail.com",
    ]
    assert expected_output == sorted(
        await get_managers(get_new_context(), group_name)
    )


async def test_get_reattackers() -> None:
    reattackers = await get_reattackers(get_new_context(), "oneshottest")
    assert reattackers == ["integrateshacker@fluidattacks.com"]


@pytest.mark.changes_db
async def test_remove_access() -> None:
    loaders: Dataloaders = get_new_context()
    email = "unittest@fluidattacks.com"
    group_name = "unittesting"
    assert await exists(loaders, group_name, email)
    await remove_access(loaders, email, group_name)

    loaders = get_new_context()
    assert not await exists(loaders, group_name, email)
