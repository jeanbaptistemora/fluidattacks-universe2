# pylint: disable=import-error
from authz import (
    get_group_level_role,
    get_group_service_policies,
    get_user_level_role,
    grant_group_level_role,
    grant_user_level_role,
    revoke_group_level_role,
    revoke_user_level_role,
)
from back.test.unit.src.utils import (
    get_mock_response,
    get_mocked_path,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
from db_model.types import (
    Policies,
)
from decimal import (
    Decimal,
)
import json
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["email", "result"],
    [
        ["continuoushacking@gmail.com", "hacker"],
        ["integrateshacker@fluidattacks.com", "hacker"],
        ["integratesuser@gmail.com", "user"],
        ["unittest@fluidattacks.com", "admin"],
        ["asdfasdfasdfasdf@gmail.com", ""],
    ],
)
@patch(get_mocked_path("loaders.stakeholder.load"), new_callable=AsyncMock)
async def test_get_user_level_role(
    mock_stakeholder_loader: AsyncMock,
    email: str,
    result: str,
) -> None:
    loaders: Dataloaders = get_new_context()
    if result:
        mock_stakeholder_loader.return_value = get_mock_response(
            get_mocked_path("loaders.stakeholder.load"),
            json.dumps([email]),
        )
    else:
        mock_stakeholder_loader.return_value.role = None
    user_level_role = await get_user_level_role(loaders, email)
    assert user_level_role == result
    assert mock_stakeholder_loader.called is True


@pytest.mark.parametrize(
    ["group", "result"],
    [
        [
            Group(
                business_name="Testing Company and Sons",
                policies=Policies(
                    max_number_acceptances=3,
                    min_acceptance_severity=Decimal("0"),
                    vulnerability_grace_period=10,
                    modified_by="integratesmanager@gmail.com",
                    min_breaking_severity=Decimal("3.9"),
                    max_acceptance_days=90,
                    modified_date=datetime.fromisoformat(
                        "2021-11-22T20:07:57+00:00"
                    ),
                    max_acceptance_severity=Decimal("3.9"),
                ),
                context="Group context test",
                disambiguation="Disambiguation test",
                description="Integrates unit test group",
                language=GroupLanguage.EN,
                created_by="integratesmanager@gmail.com",
                organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                name="unittesting",
                created_date=datetime.fromisoformat(
                    "2018-03-08T00:43:18+00:00"
                ),
                state=GroupState(
                    has_machine=True,
                    has_squad=True,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-03-08T00:43:18+00:00"
                    ),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.MACHINE,
                    type=GroupSubscriptionType.CONTINUOUS,
                    tags=set(("test-groups", "test-updates", "test-tag")),
                    service=GroupService.WHITE,
                ),
                business_id="14441323",
                sprint_duration=2,
            ),
            [
                "asm",
                "continuous",
                "forces",
                "report_vulnerabilities",
                "service_white",
                "squad",
            ],
        ],
        [
            Group(
                business_name="Testing Company and Sons",
                policies=Policies(
                    max_number_acceptances=3,
                    min_acceptance_severity=Decimal("0"),
                    vulnerability_grace_period=10,
                    modified_by="integratesmanager@gmail.com",
                    min_breaking_severity=Decimal("3.9"),
                    max_acceptance_days=90,
                    modified_date=datetime.fromisoformat(
                        "2021-11-22T20:07:57+00:00"
                    ),
                    max_acceptance_severity=Decimal("3.9"),
                ),
                context="Group context test",
                disambiguation="Disambiguation test",
                description="Oneshottest test group",
                language=GroupLanguage.EN,
                created_by="integratesmanager@gmail.com",
                organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                name="oneshottest",
                created_date=datetime.fromisoformat(
                    "2019-01-20T22:00:00+00:00"
                ),
                state=GroupState(
                    has_machine=True,
                    has_squad=False,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2019-01-20T22:00:00+00:00"
                    ),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.ONESHOT,
                    type=GroupSubscriptionType.ONESHOT,
                    tags=set(("test-tag")),
                    service=GroupService.BLACK,
                ),
                business_id="14441323",
                sprint_duration=2,
            ),
            [
                "asm",
                "report_vulnerabilities",
                "service_black",
            ],
        ],
    ],
)
async def test_get_group_service_policies(
    group: Group,
    result: list,
) -> None:

    group_policies = get_group_service_policies(group)
    assert sorted(group_policies) == result


@pytest.mark.parametrize(
    ["email", "group", "result"],
    [
        ["integrateshacker@fluidattacks.com", "unittesting", "hacker"],
        ["integratesuser@gmail.com", "unittesting", "user_manager"],
        ["unittest@fluidattacks.com", "unittesting", "admin"],
        ["test_admin@gmail.com", "unittesting", "admin"],
        ["test_email@gmail.com", "unittesting", ""],
    ],
)
@patch(get_mocked_path("loaders.group_access.load"), new_callable=AsyncMock)
@patch(get_mocked_path("get_user_level_role"), new_callable=AsyncMock)
async def test_get_group_level_role(
    mock_get_user_level_role: AsyncMock,
    mock_group_access_loader: AsyncMock,
    email: str,
    group: str,
    result: str,
) -> None:

    loaders: Dataloaders = get_new_context()
    mock_group_access_loader.return_value = get_mock_response(
        get_mocked_path("loaders.group_access.load"),
        json.dumps([email, group, result]),
    )
    mock_get_user_level_role.return_value = get_mock_response(
        get_mocked_path("get_user_level_role"),
        json.dumps([email]),
    )
    test_role = await get_group_level_role(loaders, email, group)
    assert test_role == result
    assert mock_group_access_loader.called is True
    if result == "":
        assert mock_get_user_level_role.called is True


@pytest.mark.parametrize(
    ["email", "role"],
    [
        ["test_email@test.com", "user"],
        ["test_email@test.com", "admin"],
    ],
)
@patch(
    get_mocked_path("stakeholders_model.update_metadata"),
    new_callable=AsyncMock,
)
async def test_grant_user_level_role(
    mock_stakeholder_update_metadata: AsyncMock,
    email: str,
    role: str,
) -> None:
    mock_stakeholder_update_metadata.return_value = get_mock_response(
        get_mocked_path("stakeholders_model.update_metadata"),
        json.dumps([email, role]),
    )

    await grant_user_level_role(email, role)

    with pytest.raises(ValueError) as test_raised_err:
        await grant_user_level_role(email, "bad_role")
    assert str(test_raised_err.value) == "Invalid role value: bad_role"
    assert mock_stakeholder_update_metadata.called is True


@pytest.mark.parametrize(
    ["email", "group", "group_role"],
    [
        ["test@test.com", "unittesting", "user"],
        ["test2@test.com", "oneshottest", "user_manager"],
    ],
)
@patch(get_mocked_path("grant_user_level_role"), new_callable=AsyncMock)
@patch(get_mocked_path("get_user_level_role"), new_callable=AsyncMock)
@patch(
    get_mocked_path("group_access_model.update_metadata"),
    new_callable=AsyncMock,
)
@patch(get_mocked_path("loaders.group_access.load"), new_callable=AsyncMock)
async def test_grant_group_level_role(  # pylint: disable=too-many-arguments
    mock_group_access_loader: AsyncMock,
    mock_group_access_update_metadata: AsyncMock,
    mock_get_user_level_role: AsyncMock,
    mock_grant_user_level_role: AsyncMock,
    email: str,
    group: str,
    group_role: str,
) -> None:
    mock_group_access_loader.return_value = get_mock_response(
        get_mocked_path("loaders.group_access.load"),
        json.dumps([email, group]),
    )
    mock_group_access_update_metadata.return_value = get_mock_response(
        get_mocked_path("group_access_model.update_metadata"),
        json.dumps([email, group, group_role]),
    )
    mock_get_user_level_role.return_value = get_mock_response(
        get_mocked_path("get_user_level_role"),
        json.dumps([email]),
    )
    mock_grant_user_level_role.return_value = get_mock_response(
        get_mocked_path("grant_user_level_role"),
        json.dumps([email, group_role]),
    )
    await grant_group_level_role(get_new_context(), email, group, group_role)

    assert mock_group_access_loader.called is True
    assert mock_group_access_update_metadata.called is True
    assert mock_get_user_level_role.called is True

    with pytest.raises(ValueError) as test_raised_err:
        await grant_group_level_role(
            get_new_context(), email, group, "breakall"
        )
    assert str(test_raised_err.value) == "Invalid role value: breakall"


@pytest.mark.parametrize(
    [
        "email",
        "group",
        "group_role",
    ],
    [
        ["integrateshacker@fluidattacks.com", "unittesting", "hacker"],
        ["integratesuser@gmail.com", "unittesting", "user_manager"],
    ],
)
@patch(get_mocked_path("loaders.group_access.load"), new_callable=AsyncMock)
@patch(
    get_mocked_path("group_access_model.update_metadata"),
    new_callable=AsyncMock,
)
async def test_revoke_group_level_role(
    mock_group_access_update_metadata: AsyncMock,
    mock_group_access_loader: AsyncMock,
    email: str,
    group: str,
    group_role: str,
) -> None:
    mock_group_access_loader.return_value = get_mock_response(
        get_mocked_path("loaders.group_access.load"),
        json.dumps([email, group, group_role]),
    )
    mock_group_access_update_metadata.return_value = get_mock_response(
        get_mocked_path("group_access_model.update_metadata"),
        json.dumps([email, group]),
    )

    await revoke_group_level_role(get_new_context(), email, group)
    assert mock_group_access_loader.called is True
    assert mock_group_access_update_metadata.called is True


@pytest.mark.parametrize(
    ["email"],
    [
        ["integrateshacker@fluidattacks.com"],
        ["integratesuser@gmail.com"],
    ],
)
@patch(
    get_mocked_path("stakeholders_model.update_metadata"),
    new_callable=AsyncMock,
)
async def test_revoke_user_level_role(
    mock_stakeholder_update_metadata: AsyncMock,
    email: str,
) -> None:

    loaders: Dataloaders = get_new_context()
    mock_stakeholder_update_metadata.return_value = get_mock_response(
        get_mocked_path("stakeholders_model.update_metadata"),
        json.dumps([email]),
    )
    await revoke_user_level_role(loaders, email)

    assert mock_stakeholder_update_metadata.called is True
