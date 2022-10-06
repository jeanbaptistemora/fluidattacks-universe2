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
from db_model import (
    group_access as group_access_model,
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
        ["integrates_vms", 9],
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
    def side_effect(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    loaders: Dataloaders = get_new_context()
    with mock.patch(
        "dynamodb.operations.get_resource", new_callable=mock.AsyncMock
    ) as mock_resource:
        mock_resource.return_value.batch_get_item.side_effect = side_effect
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
    def side_effect(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    loaders: Dataloaders = get_new_context()
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = side_effect
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
    def side_effect(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    loaders: Dataloaders = get_new_context()
    with mock.patch(
        "dynamodb.operations.get_resource", new_callable=mock.AsyncMock
    ) as mock_resource:
        mock_resource.return_value.batch_get_item.side_effect = side_effect
        test_role = await get_group_level_role(loaders, email, group)
        assert mock_resource.called is True
        assert test_role == result


@pytest.mark.changes_db
async def test_grant_user_level_role() -> None:
    await grant_user_level_role("..TEST@gmail.com", "user")
    assert (
        await get_user_level_role(get_new_context(), "..test@gmail.com")
        == "user"
    )
    assert (
        await get_user_level_role(get_new_context(), "..tEst@gmail.com")
        == "user"
    )
    await grant_user_level_role("..TEST@gmail.com", "admin")
    assert (
        await get_user_level_role(get_new_context(), "..test@gmail.com")
        == "admin"
    )
    assert (
        await get_group_level_role(
            get_new_context(), "..tEst@gmail.com", "a-group"
        )
        == "admin"
    )
    with pytest.raises(ValueError) as test_raised_err:
        await grant_user_level_role("..TEST@gmail.com", "breakall")
    assert str(test_raised_err.value) == "Invalid role value: breakall"


@pytest.mark.changes_db
async def test_grant_group_level_role() -> None:
    await grant_group_level_role(
        get_new_context(), "..TEST2@gmail.com", "group", "user"
    )
    assert (
        await get_user_level_role(get_new_context(), "..test2@gmail.com")
        == "user"
    )
    assert (
        await get_user_level_role(get_new_context(), "..tESt2@gmail.com")
        == "user"
    )
    assert (
        await get_group_level_role(
            get_new_context(), "..test2@gmail.com", "GROUP"
        )
        == "user"
    )
    assert not await get_group_level_role(
        get_new_context(), "..test2@gmail.com", "other-group"
    )
    with pytest.raises(ValueError) as test_raised_err:
        await grant_group_level_role(
            get_new_context(), "..TEST2@gmail.com", "group", "breakall"
        )
    assert str(test_raised_err.value) == "Invalid role value: breakall"


@pytest.mark.changes_db
async def test_revoke_group_level_role() -> None:
    await grant_group_level_role(
        get_new_context(), "revoke_group_LEVEL_role@gmail.com", "group", "user"
    )
    await grant_group_level_role(
        get_new_context(),
        "REVOKE_group_level_role@gmail.com",
        "other-group",
        "user",
    )
    assert (
        await get_group_level_role(
            get_new_context(), "revoke_group_level_ROLE@gmail.com", "group"
        )
        == "user"
    )
    assert (
        await get_group_level_role(
            get_new_context(),
            "revoke_GROUP_level_role@gmail.com",
            "other-group",
        )
        == "user"
    )
    assert not await get_group_level_role(
        get_new_context(),
        "REVOKE_group_level_role@gmail.com",
        "yet-other-group",
    )
    await group_access_model.remove(
        email="revoke_GROUP_level_role@gmail.com", group_name="other-group"
    )
    await revoke_group_level_role(
        get_new_context(), "revoke_GROUP_level_role@gmail.com", "other-group"
    )
    assert (
        await get_group_level_role(
            get_new_context(), "revoke_group_level_role@gmail.com", "group"
        )
        == "user"
    )
    assert not await get_group_level_role(
        get_new_context(), "revoke_group_level_role@gmail.com", "other-group"
    )
    assert not await get_group_level_role(
        get_new_context(),
        "revoke_group_level_role@gmail.com",
        "yet-other-group",
    )
    await group_access_model.remove(
        email="revoke_GROUP_level_role@gmail.com", group_name="group"
    )
    await revoke_group_level_role(
        get_new_context(), "revoke_GROUP_level_role@gmail.com", "group"
    )
    assert not await get_group_level_role(
        get_new_context(), "revOke_group_level_role@gmail.com", "group"
    )
    assert not await get_group_level_role(
        get_new_context(), "revoKe_group_level_role@gmail.com", "other-group"
    )
    assert not await get_group_level_role(
        get_new_context(),
        "revokE_group_level_role@gmail.com",
        "yet-other-group",
    )


@pytest.mark.changes_db
async def test_revoke_user_level_role() -> None:
    await grant_user_level_role("revoke_user_LEVEL_role@gmail.com", "user")

    loaders: Dataloaders = get_new_context()
    assert (
        await get_user_level_role(loaders, "revoke_user_level_ROLE@gmail.com")
        == "user"
    )
    assert not await get_user_level_role(
        loaders, "REVOKE_user_level_role@gmail.net"
    )
    await revoke_user_level_role(loaders, "revoke_USER_LEVEL_ROLE@gmail.com")

    assert not await get_user_level_role(
        get_new_context(), "revoke_user_level_ROLE@gmail.com"
    )
