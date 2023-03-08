from . import (
    put_mutation,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupManaged,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_managed")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_update_group_managed(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    loaders: Dataloaders = get_new_context()
    group = await loaders.group.load(group_name)
    assert group
    assert group.state.has_squad is True
    assert group.state.managed is GroupManaged["MANAGED"]

    result: dict[str, Any] = await put_mutation(
        user=email,
        group=group_name,
        managed=GroupManaged["UNDER_REVIEW"],
        comments="Change to under review",
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupManaged"]
    assert result["data"]["updateGroupManaged"]["success"]

    loaders.group.clear(group_name)
    group_updated = await loaders.group.load(group_name)
    assert group_updated
    assert group_updated.state.has_squad is True
    assert group_updated.state.managed is GroupManaged["UNDER_REVIEW"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_managed")
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
    ],
)
async def test_update_group_managed_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await put_mutation(
        user=email,
        group=group_name,
        managed=GroupManaged["UNDER_REVIEW"],
        comments="",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
