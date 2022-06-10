from organizations import (
    dal as orgs_dal,
)
import pytest

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_add_user() -> None:
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    users = await orgs_dal.get_users(org_id)

    email = "org_testuser1@gmail.com"
    await orgs_dal.add_user(org_id, email)
    updated_users = await orgs_dal.get_users(org_id)
    assert len(updated_users) == len(users) + 1
    assert sorted(updated_users) == sorted(users + [email])


@pytest.mark.changes_db
async def test_remove_user() -> None:
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    user = "org_testuser2@gmail.com"
    users = await orgs_dal.get_users(org_id)
    assert len(users) > 0
    assert user in users

    await orgs_dal.remove_user(org_id, user)
    updated_users = await orgs_dal.get_users(org_id)
    assert len(updated_users) == len(users) - 1
    assert user not in updated_users


async def test_get_ids_for_user() -> None:
    existing_user = "integratesmanager@gmail.com"
    non_existent_user = "madeupuser@gmail.com"
    org_ids_1 = await orgs_dal.get_ids_for_user(existing_user)
    org_ids_2 = await orgs_dal.get_ids_for_user(non_existent_user)
    assert sorted(org_ids_1) == [
        "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        "ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac",
        "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
        "ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1",
    ]
    assert org_ids_2 == []


async def test_get_users() -> None:
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    users = await orgs_dal.get_users(org_id)
    expected = [
        "continuoushack2@gmail.com",
        "continuoushacking@gmail.com",
        "customer_manager@fluidattacks.com",
        "forces.unittesting@fluidattacks.com",
        "integratesuser2@fluidattacks.com",
        "integratesuser2@gmail.com",
        "integrateshacker@fluidattacks.com",
        "integratesmanager@fluidattacks.com",
        "integratesmanager@gmail.com",
        "integratesreattacker@fluidattacks.com",
        "integratesresourcer@fluidattacks.com",
        "integratesreviewer@fluidattacks.com",
        "integratesserviceforces@gmail.com",
        "integratesuser@gmail.com",
        "unittest2@fluidattacks.com",
        "vulnmanager@gmail.com",
    ]
    assert len(users) == 18
    for user in expected:
        assert user in users


async def test_has_user_access() -> None:
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    existing_user = "integratesmanager@gmail.com"
    non_existent_user = "madeupuser@gmail.com"
    assert await orgs_dal.has_user_access(org_id, existing_user)
    assert not await orgs_dal.has_user_access(org_id, non_existent_user)
