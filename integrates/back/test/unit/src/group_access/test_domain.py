# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
    GroupAccessRequest,
    GroupAccessState,
)
from group_access.domain import (
    add_access,
    exists,
    get_group_stakeholders_emails,
    get_managers,
    get_reattackers,
    remove_access,
    update,
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
@pytest.mark.skip(reason="The feature it relies on has not been implemented")
async def test_update_group_access_metadata() -> None:
    loaders: Dataloaders = get_new_context()
    email = "another_user@gmail.com"
    group_name = "unittesting"
    modification_date: str = "2022-11-01T06:07:57+00:00"
    assert not await exists(loaders, group_name, email)

    await add_access(
        loaders=loaders, email=email, group_name=group_name, role="user"
    )
    assert await exists(loaders, group_name, email)

    access: GroupAccess = await loaders.group_access.load(
        GroupAccessRequest(email=email, group_name=group_name)
    )
    historic_access: tuple[
        GroupAccess, ...
    ] = await loaders.group_historic_access.load(
        GroupAccessRequest(email=email, group_name=group_name)
    )
    assert len(historic_access) == 2
    assert access.email == historic_access[1].email == email
    assert access.group_name == historic_access[1].group_name == group_name
    assert access.state == historic_access[1].state
    assert access.role == historic_access[1].role == "user"
    assert access.has_access == historic_access[1].has_access

    await update(
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(
            state=GroupAccessState(modified_date=modification_date),
            responsibility="Responsible for testing the historic facet",
        ),
    )

    loaders.group_access.clear_all()
    loaders.group_historic_access.clear_all()
    access = await loaders.group_access.load(
        GroupAccessRequest(email=email, group_name=group_name)
    )
    historic_access = await loaders.group_historic_access.load(
        GroupAccessRequest(email=email, group_name=group_name)
    )
    assert len(historic_access) == 3
    assert access == historic_access[-1]

    expected_history: tuple[GroupAccess, ...] = (
        GroupAccess(
            email=email,
            group_name=group_name,
            state=GroupAccessState(modified_date=modification_date),
            role=None,
            has_access=True,
        ),
        GroupAccess(
            email=email,
            group_name=group_name,
            state=GroupAccessState(modified_date=modification_date),
            role="user",
            has_access=True,
        ),
        GroupAccess(
            email=email,
            group_name=group_name,
            responsibility="Responsible for testing the historic facet",
            state=GroupAccessState(modified_date=modification_date),
            role="user",
            has_access=True,
        ),
    )
    assert historic_access == expected_history


@pytest.mark.changes_db
async def test_remove_access() -> None:
    loaders: Dataloaders = get_new_context()
    email = "unittest@fluidattacks.com"
    group_name = "unittesting"
    assert await exists(loaders, group_name, email)
    await remove_access(loaders, email, group_name)

    loaders = get_new_context()
    assert not await exists(loaders, group_name, email)
