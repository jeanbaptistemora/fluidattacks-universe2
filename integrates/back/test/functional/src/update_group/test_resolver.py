from . import (
    get_query_group,
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupSubscriptionType,
    GroupTier,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_update_group(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    loaders: Dataloaders = get_new_context()
    group = await loaders.group.load(group_name)
    assert group
    assert group.state.type == GroupSubscriptionType.CONTINUOUS
    assert group.state.has_machine is False
    assert group.state.has_squad is True
    assert group.state.justification is None
    assert group.state.tier == GroupTier.OTHER

    result: dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" not in result
    assert "success" in result["data"]["updateGroup"]
    assert result["data"]["updateGroup"]["success"]

    query_result = await get_query_group(email=email, group_name=group_name)
    assert "errors" in query_result
    assert (
        query_result["errors"][0]["message"]
        == "Access denied or group not found"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_update_group_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
