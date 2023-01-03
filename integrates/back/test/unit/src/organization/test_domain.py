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
            loaders=loaders,
            organization_id=org_id,
            email=user,
            role="customer_manager",
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


async def test_get_group_names() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"  # NOSONAR
    groups = await orgs_domain.get_group_names(loaders, org_id)
    assert len(groups) == 3
    assert sorted(groups) == [
        "continuoustesting",
        "oneshottest",
        "unittesting",
    ]


async def test_get_stakeholders() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    org_stakeholders = await orgs_domain.get_stakeholders(loaders, org_id)
    org_stakeholders_emails = sorted(
        [stakeholder.email for stakeholder in org_stakeholders]
    )

    expected_emails = [
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
        "vulnmanager@gmail.com",
    ]
    assert len(org_stakeholders_emails) == 17
    for email in expected_emails:
        assert email in org_stakeholders_emails

    second_stakeholders_emails = sorted(
        await orgs_domain.get_stakeholders_emails(loaders, org_id)
    )
    assert len(second_stakeholders_emails) == 17
    for email in expected_emails:
        assert email in second_stakeholders_emails


async def test_has_group() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    existing_group = "unittesting"
    non_existent_group = "madeupgroup"
    assert await orgs_domain.has_group(loaders, org_id, existing_group)
    assert not await orgs_domain.has_group(loaders, org_id, non_existent_group)


async def test_has_user_access() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    existing_user = "integratesmanager@gmail.com"
    non_existent_user = "madeupuser@gmail.com"
    assert await orgs_domain.has_access(loaders, org_id, existing_user)
    assert not await orgs_domain.has_access(loaders, org_id, non_existent_user)
