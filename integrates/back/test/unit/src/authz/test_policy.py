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
from moto.dynamodb2 import (
    dynamodb_backend2,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
import pytest
from typing import (
    Any,
)
from unittest import (
    mock,
)
from unittest.mock import (
    AsyncMock,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]

TABLE_NAME = "integrates_vms"


@pytest.mark.parametrize(
    ["table", "length"],
    [
        ["integrates_vms", 22],
    ],
)
def test_create_tables(
    dynamo_resource: ServiceResource, table: str, length: int
) -> None:
    assert table in dynamodb_backend2.tables
    assert len(dynamo_resource.Table(table).scan()["Items"]) == length


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
@mock.patch(
    get_mocked_path("loaders.stakeholder.load"), new_callable=mock.AsyncMock
)
async def test_get_user_level_role(
    mock_stakeholder_loader: mock.AsyncMock,
    email: str,
    result: str,
) -> None:
    loaders: Dataloaders = get_new_context()
    if result:
        mock_stakeholder_loader.return_value = get_mock_response(
            get_mocked_path("loaders.stakeholder.load"),
            json.dumps([email, result]),
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
                    modified_date="2021-11-22T20:07:57+00:00",
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
                    modified_date="2021-11-22T20:07:57+00:00",
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


@mock.patch(
    "dynamodb.operations.get_resource",
    new_callable=AsyncMock,
)
@pytest.mark.parametrize(
    ["email", "group", "result"],
    [
        ["integrateshacker@fluidattacks.com", "unittesting", "hacker"],
        ["integratesuser@gmail.com", "unittesting", "user_manager"],
        ["unittest@fluidattacks.com", "unittesting", "admin"],
        ["test_email@gmail.com", "unittesting", ""],
    ],
)
async def test_get_group_level_role(
    mock_resource: AsyncMock,
    dynamo_resource: ServiceResource,
    email: str,
    group: str,
    result: str,
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    loaders: Dataloaders = get_new_context()
    mock_resource.return_value.batch_get_item.side_effect = mock_batch_get_item
    test_role = await get_group_level_role(loaders, email, group)
    assert test_role == result
    test_role_other_group = await get_group_level_role(
        loaders, email, "other-group"
    )
    if await get_user_level_role(loaders, email) == "admin":
        assert test_role_other_group == result
    else:
        assert not test_role_other_group
    assert mock_resource.called is True


@pytest.mark.parametrize(
    ["email", "role"],
    [
        ["test_email@test.com", "user"],
        ["test_email@test.com", "admin"],
    ],
)
@mock.patch(
    get_mocked_path("stakeholders_model.update_metadata"),
    new_callable=mock.AsyncMock,
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


@mock.patch(
    "dynamodb.operations.get_table_resource",
    new_callable=AsyncMock,
)
@mock.patch(
    "dynamodb.operations.get_resource",
    new_callable=AsyncMock,
)
@pytest.mark.parametrize(
    ["email", "group", "group_role", "expected_user_role"],
    [
        ["test@test.com", "test_group", "user", "user"],
        [
            "test2@test.com",
            "test_group2",
            "user_manager",
            "user",
        ],
    ],
)
async def test_grant_group_level_role(  # pylint: disable=too-many-arguments
    mock_resource: AsyncMock,
    mock_table_resource: AsyncMock,
    email: str,
    group: str,
    group_role: str,
    expected_user_role: str,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    def mock_update_item(**kwargs: Any) -> Any:
        return dynamo_resource.Table(TABLE_NAME).update_item(**kwargs)

    mock_table_resource.return_value.update_item.side_effect = mock_update_item
    mock_resource.return_value.batch_get_item.side_effect = mock_batch_get_item
    await grant_group_level_role(get_new_context(), email, group, group_role)
    assert (
        await get_user_level_role(get_new_context(), email)
        == expected_user_role
    )
    mock_resource.return_value.batch_get_item.side_effect = mock_batch_get_item
    assert (
        await get_group_level_role(get_new_context(), email, group)
        == group_role
    )
    assert mock_table_resource.called is True
    assert mock_resource.called is True
    with pytest.raises(ValueError) as test_raised_err:
        await grant_group_level_role(
            get_new_context(), email, group, "breakall"
        )
    assert str(test_raised_err.value) == "Invalid role value: breakall"


@mock.patch(
    "dynamodb.operations.get_table_resource",
    new_callable=AsyncMock,
)
@mock.patch(
    "dynamodb.operations.get_resource",
    new_callable=AsyncMock,
)
@pytest.mark.parametrize(
    ["email", "group", "group_role", "expected_group_role"],
    [
        ["revoke_group_level_role@gmail.com", "group", "user", "user"],
    ],
)
async def test_revoke_group_level_role(  # pylint: disable=too-many-arguments
    mock_resource: AsyncMock,
    mock_table_resource: AsyncMock,
    email: str,
    group: str,
    group_role: str,
    expected_group_role: str,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    def mock_update_item(**kwargs: Any) -> Any:
        return dynamo_resource.Table(TABLE_NAME).update_item(**kwargs)

    mock_table_resource.return_value.update_item.side_effect = mock_update_item
    mock_resource.return_value.batch_get_item.side_effect = mock_batch_get_item
    await grant_group_level_role(get_new_context(), email, group, group_role)
    group_level_role = await get_group_level_role(
        get_new_context(), email, group
    )
    assert group_level_role == expected_group_role
    await revoke_group_level_role(get_new_context(), email, group)
    assert not await get_group_level_role(get_new_context(), email, group)
    assert mock_table_resource.called is True
    assert mock_resource.called is True


@mock.patch(
    "dynamodb.operations.get_table_resource",
    new_callable=AsyncMock,
)
@mock.patch(
    "dynamodb.operations.get_resource",
    new_callable=AsyncMock,
)
async def test_revoke_user_level_role(
    mock_resource: AsyncMock,
    mock_table_resource: AsyncMock,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    def mock_update_item(**kwargs: Any) -> Any:
        return dynamo_resource.Table(TABLE_NAME).update_item(**kwargs)

    email = "revoke_user_level_role@gmail.com"
    role = "user"
    mock_table_resource.return_value.update_item.side_effect = mock_update_item
    await grant_user_level_role(email, role)
    mock_resource.return_value.batch_get_item.side_effect = mock_batch_get_item
    loaders: Dataloaders = get_new_context()
    user_level_role = await get_user_level_role(loaders, email)
    assert user_level_role == role
    await revoke_user_level_role(loaders, email)

    assert not await get_user_level_role(get_new_context(), email)
    assert mock_table_resource.called is True
    assert mock_resource.called is True
