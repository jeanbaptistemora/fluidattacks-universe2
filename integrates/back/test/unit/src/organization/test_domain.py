import authz
from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_mock_response,
    get_mocked_path,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from group_access import (
    domain as group_access_domain,
)
import json
from organizations.domain import (
    add_group_access,
    add_stakeholder,
    get_group_names,
    get_stakeholders,
    get_stakeholders_emails,
    has_access,
    has_group,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["organization_id", "email", "role"],
    [
        [
            "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            "org_testgroupmanager2@fluidattacks.com",
            "customer_manager",
        ],
    ],
)
@patch(
    get_mocked_path("group_access_domain.add_access"), new_callable=AsyncMock
)
@patch(get_mocked_path("get_group_names"), new_callable=AsyncMock)
@patch(
    get_mocked_path("authz.grant_organization_level_role"),
    new_callable=AsyncMock,
)
@patch(
    get_mocked_path("org_access_model.update_metadata"), new_callable=AsyncMock
)
async def test_add_customer_manager(  # pylint: disable=too-many-arguments
    mock_org_access_model_update_metadata: AsyncMock,
    mock_authz_grant_organization_level_role: AsyncMock,
    mock_get_group_names: AsyncMock,
    mock_group_access_domain_add_access: AsyncMock,
    organization_id: str,
    email: str,
    role: str,
) -> None:
    mock_org_access_model_update_metadata.return_value = get_mock_response(
        get_mocked_path("org_access_model.update_metadata"),
        json.dumps([organization_id, email]),
    )
    mock_authz_grant_organization_level_role.return_value = get_mock_response(
        get_mocked_path("authz.grant_organization_level_role"),
        json.dumps([email, organization_id, role]),
    )
    mock_get_group_names.return_value = get_mock_response(
        get_mocked_path("get_group_names"),
        json.dumps([organization_id]),
    )
    mock_group_access_domain_add_access.return_value = get_mock_response(
        get_mocked_path("group_access_domain.add_access"),
        json.dumps([email, organization_id, role]),
    )
    loaders: Dataloaders = get_new_context()

    await add_stakeholder(
        loaders=loaders,
        organization_id=organization_id,
        email=email,
        role=role,
    )
    assert mock_org_access_model_update_metadata.called is True
    assert mock_authz_grant_organization_level_role.called is True
    assert mock_get_group_names.called is True
    assert mock_group_access_domain_add_access.called is True


async def test_add_group_access() -> None:
    loaders: Dataloaders = get_new_context()
    group_name = "kurome"
    group_users = await group_access_domain.get_group_stakeholders_emails(
        loaders, group_name
    )
    assert len(group_users) == 0

    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"  # NOSONAR
    org_group_names = await get_group_names(loaders, org_id)
    assert group_name in org_group_names
    await add_group_access(loaders, org_id, group_name)

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


async def test_get_group_names() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"  # NOSONAR
    groups = await get_group_names(loaders, org_id)
    assert len(groups) == 3
    assert sorted(groups) == [
        "continuoustesting",
        "oneshottest",
        "unittesting",
    ]


async def test_get_stakeholders() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    org_stakeholders = await get_stakeholders(loaders, org_id)
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
        await get_stakeholders_emails(loaders, org_id)
    )
    assert len(second_stakeholders_emails) == 17
    for email in expected_emails:
        assert email in second_stakeholders_emails


async def test_has_group() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    existing_group = "unittesting"
    non_existent_group = "madeupgroup"
    assert await has_group(loaders, org_id, existing_group)
    assert not await has_group(loaders, org_id, non_existent_group)


async def test_has_user_access() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    existing_user = "integratesmanager@gmail.com"
    non_existent_user = "madeupuser@gmail.com"
    assert await has_access(loaders, org_id, existing_user)
    assert not await has_access(loaders, org_id, non_existent_user)
