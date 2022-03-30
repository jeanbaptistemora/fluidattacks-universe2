from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupStateUpdationJustification,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
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
    group: Group = await loaders.group_typed.load(group_name)
    assert group.state.type == GroupSubscriptionType.CONTINUOUS
    assert group.state.has_machine is False
    assert group.state.has_squad is True
    assert group.state.justification is None
    assert group.state.tier == GroupTier.OTHER

    result: dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" not in result
    assert "success" in result["data"]["updateGroup"]
    assert result["data"]["updateGroup"]["success"]

    loaders.group_typed.clear(group_name)
    group_updated: Group = await loaders.group_typed.load(group_name)
    assert group_updated.state.type == GroupSubscriptionType.ONESHOT
    assert group_updated.state.has_machine is False
    assert group_updated.state.has_squad is False
    assert (
        group_updated.state.justification
        == GroupStateUpdationJustification.NONE
    )
    assert group_updated.state.tier == GroupTier.ONESHOT
    assert group_updated.state.modified_by == email


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
        ["executive@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_update_group_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
