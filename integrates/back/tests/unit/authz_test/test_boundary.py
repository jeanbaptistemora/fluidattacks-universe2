import authz
import pytest

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["email"],
    [
        ["continuoushacking@gmail.com"],
        ["integratescustomer@gmail.com"],
        ["integrateshacker@fluidattacks.com"],
    ],
)
async def test_get_user_level_actions_model(email: str) -> None:
    user_level_role = await authz.get_user_level_role(email)

    assert await authz.get_user_level_actions(
        email
    ) == authz.get_user_level_roles_model(email).get(user_level_role, {}).get(
        "actions"
    )


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
    group_level_role = await authz.get_group_level_role(email, group)

    assert await authz.get_group_level_actions(
        email, group
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
    organization_level_role = await authz.get_organization_level_role(
        email, organization_id
    )

    assert await authz.get_organization_level_actions(
        email, organization_id
    ) == authz.get_organization_level_roles_model(email).get(
        organization_level_role, {}
    ).get(
        "actions"
    )
