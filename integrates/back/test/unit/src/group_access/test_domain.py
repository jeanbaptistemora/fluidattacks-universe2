from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_mocked_path,
    set_mocks_return_values,
    set_mocks_side_effects,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
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
from newutils import (
    datetime as datetime_utils,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]

MODULE_AT_TEST = "group_access.domain."


@pytest.mark.parametrize(
    ["email", "group_name", "role"],
    [
        ["unittest@fluidattacks.com", "unittesting", "user"],
    ],
)
@patch(MODULE_AT_TEST + "authz.grant_group_level_role", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "update", new_callable=AsyncMock)
async def test_add_access(
    mock_update: AsyncMock,
    mock_authz_grant_group_level_role: AsyncMock,
    email: str,
    group_name: str,
    role: str,
) -> None:
    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_update,
            mock_authz_grant_group_level_role,
        ],
        [
            "update",
            "authz.grant_group_level_role",
        ],
        [
            [email, group_name],
            [email, group_name, role],
        ],
    ]
    assert set_mocks_return_values(
        mocks_args=mocks_args,
        mocked_objects=mocked_objects,
        module_at_test=MODULE_AT_TEST,
        paths_list=mocked_paths,
    )
    loaders: Dataloaders = get_new_context()
    await add_access(
        loaders=loaders, email=email, group_name=group_name, role=role
    )
    assert all(mock_object.called is True for mock_object in mocked_objects)


@pytest.mark.parametrize(
    ["email", "group_name"],
    [
        ["unittest@fluidattacks.com", "unittesting"],
    ],
)
@patch(MODULE_AT_TEST + "Dataloaders.group_access", new_callable=AsyncMock)
async def test_exists(
    mock_dataloaders_group_access: AsyncMock,
    email: str,
    group_name: str,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[group_name, email]],
        mocked_objects=[mock_dataloaders_group_access.load],
        module_at_test=MODULE_AT_TEST,
        paths_list=["Dataloaders.group_access"],
    )
    loaders: Dataloaders = get_new_context()
    assert await exists(loaders, group_name, email)
    assert mock_dataloaders_group_access.load.called is True
    mock_dataloaders_group_access.load.assert_called_with(
        GroupAccessRequest(group_name=group_name, email=email)
    )


@pytest.mark.parametrize(
    ["group_name", "expected_result"],
    [
        [
            "unittesting",
            [
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
            ],
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.group_stakeholders_access",
    new_callable=AsyncMock,
)
async def test_get_group_stakeholders_emails(
    mock_dataloaders_group_stakeholders_access: AsyncMock,
    group_name: str,
    expected_result: list,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[group_name]],
        mocked_objects=[mock_dataloaders_group_stakeholders_access.load],
        module_at_test=MODULE_AT_TEST,
        paths_list=["Dataloaders.group_stakeholders_access"],
    )
    loaders = get_new_context()
    users = await get_group_stakeholders_emails(loaders, group_name)
    for user in expected_result:
        assert user in users
    assert mock_dataloaders_group_stakeholders_access.load.called is True
    mock_dataloaders_group_stakeholders_access.load.assert_called_with(
        group_name
    )


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


@pytest.mark.parametrize(
    ["group_name"],
    [
        ["oneshottest"],
    ],
)
@patch(
    MODULE_AT_TEST + "authz.get_group_level_role",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "get_group_stakeholders_emails",
    new_callable=AsyncMock,
)
async def test_get_reattackers(
    mock_get_group_stakeholders_emails: AsyncMock,
    mock_authz_get_group_level_role: AsyncMock,
    group_name: str,
) -> None:

    assert set_mocks_return_values(
        mocks_args=[[group_name]],
        mocked_objects=[mock_get_group_stakeholders_emails],
        module_at_test=MODULE_AT_TEST,
        paths_list=["get_group_stakeholders_emails"],
    )
    assert set_mocks_side_effects(
        mocks_args=[[group_name]],
        mocked_objects=[mock_authz_get_group_level_role],
        module_at_test=MODULE_AT_TEST,
        paths_list=["authz.get_group_level_role"],
    )
    loaders = get_new_context()
    reattackers = await get_reattackers(loaders=loaders, group_name=group_name)
    assert reattackers == ["integrateshacker@fluidattacks.com"]
    assert mock_get_group_stakeholders_emails.called is True
    assert mock_authz_get_group_level_role.call_count == 5


@pytest.mark.changes_db
async def test_group_access_changes() -> None:
    loaders: Dataloaders = get_new_context()
    email = "another_user@gmail.com"
    group_name = "unittesting"
    dummy_date = datetime.fromisoformat("2022-11-01T06:07:57+00:00")
    assert not await exists(loaders, group_name, email)

    await add_access(
        loaders=loaders, email=email, group_name=group_name, role="user"
    )
    assert await exists(loaders, group_name, email)

    # Adding a new user implies two trips to the db, one of which leaves a
    # cached GroupAccess
    access: GroupAccess = await loaders.group_access.clear_all().load(
        GroupAccessRequest(email=email, group_name=group_name)
    )
    historic_access: list[
        GroupAccess
    ] = await loaders.group_historic_access.load(
        GroupAccessRequest(email=email, group_name=group_name)
    )
    assert len(historic_access) == 2
    assert access == historic_access[-1]

    await update(
        loaders=loaders,
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(
            state=GroupAccessState(modified_date=datetime_utils.get_utc_now()),
            responsibility="Responsible for testing the historic facet",
        ),
    )

    access = await loaders.group_access.clear_all().load(
        GroupAccessRequest(email=email, group_name=group_name)
    )
    historic_access = await loaders.group_historic_access.clear_all().load(
        GroupAccessRequest(email=email, group_name=group_name)
    )
    assert len(historic_access) == 3
    assert access == historic_access[-1]

    expected_history = [
        GroupAccess(
            email=email,
            group_name=group_name,
            state=GroupAccessState(modified_date=dummy_date),
            role=None,
            has_access=True,
        ),
        GroupAccess(
            email=email,
            group_name=group_name,
            state=GroupAccessState(modified_date=dummy_date),
            role="user",
            has_access=True,
        ),
        GroupAccess(
            email=email,
            group_name=group_name,
            responsibility="Responsible for testing the historic facet",
            state=GroupAccessState(modified_date=dummy_date),
            role="user",
            has_access=True,
        ),
    ]
    for historic, expected in zip(historic_access, expected_history):
        assert historic.email == expected.email
        assert historic.group_name == expected.group_name
        assert historic.responsibility == expected.responsibility
        assert historic.state.modified_date
        assert historic.role == expected.role
        assert historic.has_access == expected.has_access

    await remove_access(loaders, email, group_name)
    loaders.group_access.clear_all()
    assert not await exists(loaders, group_name, email)
    historic_access = await loaders.group_historic_access.clear_all().load(
        GroupAccessRequest(email=email, group_name=group_name)
    )
    assert historic_access == []


@pytest.mark.parametrize(
    ["email", "group_name"],
    [
        ["unittest@fluidattacks.com", "unittesting"],
    ],
)
@patch(get_mocked_path("group_access_model.remove"), new_callable=AsyncMock)
@patch(get_mocked_path("update_me_draft_index"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.me_drafts.load"), new_callable=AsyncMock)
@patch(
    get_mocked_path("loaders.me_vulnerabilities.load"), new_callable=AsyncMock
)
@patch(
    get_mocked_path("loaders.group_drafts_and_findings.load"),
    new_callable=AsyncMock,
)
async def test_remove_access(  # pylint: disable=too-many-arguments
    mock_loaders_group_drafts_and_findings: AsyncMock,
    mock_loaders_me_vulnerabilities: AsyncMock,
    mock_loaders_me_drafts: AsyncMock,
    mock_update_me_draft_index: AsyncMock,
    mock_group_access_model_remove: AsyncMock,
    email: str,
    group_name: str,
) -> None:
    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_loaders_group_drafts_and_findings,
            mock_loaders_me_vulnerabilities,
            mock_loaders_me_drafts,
            mock_update_me_draft_index,
            mock_group_access_model_remove,
        ],
        [
            "loaders.group_drafts_and_findings.load",
            "loaders.me_vulnerabilities.load",
            "loaders.me_drafts.load",
            "update_me_draft_index",
            "group_access_model.remove",
        ],
        [
            [group_name],
            [email],
            [email],
            [email, group_name],
            [email, group_name],
        ],
    ]
    assert set_mocks_return_values(
        mocked_objects=mocked_objects,
        paths_list=mocked_paths,
        mocks_args=mocks_args,
    )
    loaders: Dataloaders = get_new_context()
    await remove_access(loaders, email, group_name)
    assert all(mock_object.called is True for mock_object in mocked_objects)
