from authz import (
    get_cached_group_service_policies,
    get_group_level_role,
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
    stakeholders as stakeholders_model,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
import pytest
from unittest import (
    mock,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_cached_group_service_attributes_policies() -> None:
    loaders: Dataloaders = get_new_context()
    function = get_cached_group_service_policies
    assert sorted(await function(await loaders.group.load("oneshottest"))) == [
        "asm",
        "report_vulnerabilities",
        "service_black",
    ]
    assert sorted(await function(await loaders.group.load("unittesting"))) == [
        "asm",
        "continuous",
        "forces",
        "report_vulnerabilities",
        "service_white",
        "squad",
    ]


async def test_get_group_level_role(dynamodb: ServiceResource) -> None:
    loaders: Dataloaders = get_new_context()

    def side_effect(table: str, query_attrs: dict) -> str:
        return dynamodb.Table(table).query(
            ConsistentRead=query_attrs["ConsistentRead"],
            KeyConditionExpression=query_attrs["KeyConditionExpression"],
        )["Items"]

    with mock.patch("authz.policy.dynamodb_ops.query") as mock_query:
        mock_query.side_effect = side_effect
        assert (
            await get_group_level_role(
                loaders, "integrateshacker@fluidattacks.com", "unittesting"
            )
            == "hacker"
        )
        assert (
            await get_group_level_role(
                loaders, "integratesuser@gmail.com", "unittesting"
            )
            == "user_manager"
        )
        assert (
            await get_group_level_role(
                loaders, "unittest@fluidattacks.com", "unittesting"
            )
            == "admin"
        )
        assert not await get_group_level_role(
            loaders, "asdfasdfasdfasdf@gmail.com", "unittesting"
        )


async def test_get_user_level_role() -> None:
    loaders: Dataloaders = get_new_context()
    assert (
        await get_user_level_role(loaders, "continuoushacking@gmail.com")
        == "hacker"
    )
    assert (
        await get_user_level_role(loaders, "integrateshacker@fluidattacks.com")
        == "hacker"
    )
    assert (
        await get_user_level_role(loaders, "integratesuser@gmail.com")
        == "user"
    )
    assert (
        await get_user_level_role(loaders, "unittest@fluidattacks.com")
        == "admin"
    )
    assert not await get_user_level_role(loaders, "asdfasdfasdfasdf@gmail.com")


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
    assert await revoke_group_level_role(
        "revoke_GROUP_level_role@gmail.com", "other-group"
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
    assert await revoke_group_level_role(
        "revoke_GROUP_level_role@gmail.com", "group"
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
    loaders: Dataloaders = get_new_context()
    await grant_user_level_role("revoke_user_LEVEL_role@gmail.com", "user")

    assert (
        await get_user_level_role(loaders, "revoke_user_level_ROLE@gmail.com")
        == "user"
    )
    assert not await get_user_level_role(
        loaders, "REVOKE_user_level_role@gmail.net"
    )
    await stakeholders_model.remove(email="revoke_USER_LEVEL_ROLE@gmail.com")
    assert await revoke_user_level_role("revoke_USER_LEVEL_ROLE@gmail.com")
    assert not await get_user_level_role(
        get_new_context(), "revoke_user_level_ROLE@gmail.com"
    )
