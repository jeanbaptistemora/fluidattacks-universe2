# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from authz import (
    get_group_level_role,
    get_group_service_policies,
    get_user_level_role,
    grant_group_level_role,
    grant_user_level_role,
    revoke_group_level_role,
    revoke_user_level_role,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
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

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["table", "length"],
    [
        ["fi_authz", 7],
        ["integrates_vms", 13],
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
async def test_get_user_level_role(
    email: str, result: str, dynamo_resource: ServiceResource
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    loaders: Dataloaders = get_new_context()
    with mock.patch(
        "dynamodb.operations.get_resource", new_callable=mock.AsyncMock
    ) as mock_resource:
        mock_resource.return_value.batch_get_item.side_effect = (
            mock_batch_get_item
        )
        user_level_role = await get_user_level_role(loaders, email)
    assert mock_resource.called is True
    assert user_level_role == result


@pytest.mark.parametrize(
    ["group", "result"],
    [
        ["oneshottest", ["asm", "report_vulnerabilities", "service_black"]],
        [
            "unittesting",
            [
                "asm",
                "continuous",
                "forces",
                "report_vulnerabilities",
                "service_white",
                "squad",
            ],
        ],
    ],
)
async def test_get_group_service_policies(
    group: str,
    result: list,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    loaders: Dataloaders = get_new_context()
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        group_policies = get_group_service_policies(
            await loaders.group.load(group)
        )
    assert mock_table_resource
    assert sorted(group_policies) == result


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
    dynamo_resource: ServiceResource,
    email: str,
    group: str,
    result: str,
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    loaders: Dataloaders = get_new_context()
    with mock.patch(
        "dynamodb.operations.get_resource", new_callable=mock.AsyncMock
    ) as mock_resource:
        mock_resource.return_value.batch_get_item.side_effect = (
            mock_batch_get_item
        )
        test_role = await get_group_level_role(loaders, email, group)
        assert mock_resource.called is True
        assert test_role == result
        test_role_other_group = await get_group_level_role(
            loaders, email, "other-group"
        )
        if await get_user_level_role(loaders, email) == "admin":
            assert test_role_other_group == result
        else:
            assert not test_role_other_group


@pytest.mark.parametrize(
    ["email", "formatted_email", "role"],
    [
        ["TEST_EMAIL@TEST.COM", "test_email@test.com", "user"],
        ["TEST_EmAiL@tEsT.com", "test_email@test.com", "admin"],
    ],
)
async def test_grant_user_level_role(
    dynamo_resource: ServiceResource,
    email: str,
    formatted_email: str,
    role: str,
) -> None:
    def mock_update_item(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).update_item(**kwargs)

    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.update_item.side_effect = (
            mock_update_item
        )
        await grant_user_level_role(email, role)

    with mock.patch(
        "dynamodb.operations.get_resource", new_callable=mock.AsyncMock
    ) as mock_resource:
        mock_resource.return_value.batch_get_item.side_effect = (
            mock_batch_get_item
        )
        assert (
            await get_user_level_role(get_new_context(), formatted_email)
            == role
        )
    assert mock_table_resource.called is True
    with pytest.raises(ValueError) as test_raised_err:
        await grant_user_level_role(email, "breakall")
    assert str(test_raised_err.value) == "Invalid role value: breakall"


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
async def test_grant_group_level_role(
    email: str,
    group: str,
    group_role: str,
    expected_user_role: str,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_update_item(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).update_item(**kwargs)

    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.update_item.side_effect = (
            mock_update_item
        )
        with mock.patch(
            "dynamodb.operations.get_resource", new_callable=mock.AsyncMock
        ) as mock_resource:
            mock_resource.return_value.batch_get_item.side_effect = (
                mock_batch_get_item
            )
            await grant_group_level_role(
                get_new_context(), email, group, group_role
            )
    assert mock_table_resource.called is True
    assert mock_resource.called is True
    with mock.patch(
        "dynamodb.operations.get_resource", new_callable=mock.AsyncMock
    ) as mock_resource:
        mock_resource.return_value.batch_get_item.side_effect = (
            mock_batch_get_item
        )

        assert (
            await get_user_level_role(get_new_context(), email)
            == expected_user_role
        )
    with mock.patch(
        "dynamodb.operations.get_resource", new_callable=mock.AsyncMock
    ) as mock_resource:
        mock_resource.return_value.batch_get_item.side_effect = (
            mock_batch_get_item
        )
        assert (
            await get_group_level_role(get_new_context(), email, group)
            == group_role
        )

    with pytest.raises(ValueError) as test_raised_err:
        await grant_group_level_role(
            get_new_context(), email, group, "breakall"
        )
    assert str(test_raised_err.value) == "Invalid role value: breakall"


@pytest.mark.parametrize(
    ["email", "group", "group_role", "expected_group_role"],
    [
        ["revoke_group_level_role@gmail.com", "group", "user", "user"],
    ],
)
async def test_revoke_group_level_role(
    email: str,
    group: str,
    group_role: str,
    expected_group_role: str,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_update_item(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).update_item(**kwargs)

    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.update_item.side_effect = (
            mock_update_item
        )
        with mock.patch(
            "dynamodb.operations.get_resource", new_callable=mock.AsyncMock
        ) as mock_resource:
            mock_resource.return_value.batch_get_item.side_effect = (
                mock_batch_get_item
            )
            await grant_group_level_role(
                get_new_context(), email, group, group_role
            )
            group_level_role = await get_group_level_role(
                get_new_context(), email, group
            )
            assert group_level_role == expected_group_role
            await revoke_group_level_role(get_new_context(), email, group)
            assert not await get_group_level_role(
                get_new_context(), email, group
            )
    assert mock_resource.called is True
    assert mock_table_resource.called is True


async def test_revoke_user_level_role(
    dynamo_resource: ServiceResource,
) -> None:
    def mock_update_item(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).update_item(**kwargs)

    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    email = "revoke_user_level_role@gmail.com"
    role = "user"
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.update_item.side_effect = (
            mock_update_item
        )
        await grant_user_level_role(email, role)
        with mock.patch(
            "dynamodb.operations.get_resource", new_callable=mock.AsyncMock
        ) as mock_resource:
            mock_resource.return_value.batch_get_item.side_effect = (
                mock_batch_get_item
            )
            loaders: Dataloaders = get_new_context()
            user_level_role = await get_user_level_role(loaders, email)
            assert user_level_role == role
            await revoke_user_level_role(loaders, email)

            assert not await get_user_level_role(get_new_context(), email)
    assert mock_resource.called is True
    assert mock_table_resource.called is True
