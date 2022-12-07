from authz.boundary import (
    get_group_level_actions,
    get_organization_level_actions,
    get_user_level_actions,
)
from authz.model import (
    get_group_level_roles_model,
    get_organization_level_roles_model,
    get_user_level_roles_model,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
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


@mock.patch(
    "dynamodb.operations.get_resource",
    new_callable=AsyncMock,
)
@pytest.mark.parametrize(
    ["email", "role"],
    [
        ["continuoushacking@gmail.com", "hacker"],
        ["integratesuser2@gmail.com", "user"],
        ["integrateshacker@fluidattacks.com", "hacker"],
    ],
)
async def test_get_user_level_actions(
    mock_resource: AsyncMock,
    dynamo_resource: ServiceResource,
    email: str,
    role: str,
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    loaders: Dataloaders = get_new_context()
    mock_resource.return_value.batch_get_item.side_effect = mock_batch_get_item
    assert await get_user_level_actions(
        loaders, email
    ) == get_user_level_roles_model(email).get(role, {}).get("actions")
    assert mock_resource.called is True


@mock.patch(
    "dynamodb.operations.get_table_resource",
    new_callable=AsyncMock,
)
@mock.patch(
    "dynamodb.operations.get_resource",
    new_callable=AsyncMock,
)
@pytest.mark.parametrize(
    ["email", "group", "role"],
    [
        ["continuoushacking@gmail.com", "UnItTeStInG", "user_manager"],
        ["continuoushacking@gmail.com", "unittesting", "user_manager"],
        ["continuoushacking@gmail.com", "oneshottest", "user_manager"],
        ["integrateshacker@fluidattacks.com", "unittesting", "hacker"],
        ["integrateshacker@fluidattacks.com", "oneshottest", "reattacker"],
        ["integratesuser@gmail.com", "unittesting", "user_manager"],
        ["integratesuser@gmail.com", "oneshottest", "user"],
    ],
)
async def test_get_group_level_actions(  # pylint: disable=too-many-arguments
    mock_resource: AsyncMock,
    mock_table_resource: AsyncMock,
    email: str,
    group: str,
    role: str,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    def mock_query(**kwargs: Any) -> Any:
        return dynamo_resource.Table(TABLE_NAME).query(**kwargs)

    loaders: Dataloaders = get_new_context()
    mock_table_resource.return_value.query.side_effect = mock_query
    mock_resource.return_value.batch_get_item.side_effect = mock_batch_get_item
    group_level_actions = await get_group_level_actions(loaders, email, group)
    expected_actions = (
        get_group_level_roles_model(email).get(role, {}).get("actions")
    )
    assert group_level_actions == expected_actions
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
@pytest.mark.parametrize(
    ["email", "organization_id", "organization_level_role"],
    [
        [
            "org_testgroupmanager1@gmail.com",
            "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            "customer_manager",
        ],
        [
            "unittest2@fluidattacks.com",
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            "customer_manager",
        ],
    ],
)
async def test_get_organization_level(  # pylint: disable=too-many-arguments
    mock_resource: AsyncMock,
    mock_table_resource: AsyncMock,
    email: str,
    organization_id: str,
    organization_level_role: str,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    def mock_query(**kwargs: Any) -> Any:
        return dynamo_resource.Table(TABLE_NAME).query(**kwargs)

    loaders: Dataloaders = get_new_context()
    mock_table_resource.return_value.query.side_effect = mock_query
    mock_resource.return_value.batch_get_item.side_effect = mock_batch_get_item
    organization_level_actions = await get_organization_level_actions(
        loaders, email, organization_id
    )

    expected_actions = (
        get_organization_level_roles_model(email)
        .get(organization_level_role, {})
        .get("actions")
    )
    assert organization_level_actions == expected_actions
    assert mock_table_resource.called is True
    assert mock_resource.called is True
