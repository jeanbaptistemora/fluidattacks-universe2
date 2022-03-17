from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_access_info")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
        ["hacker@gmail.com"],
        ["user@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_update_group_info(
    populate: bool,
    email: str,
) -> None:
    assert populate
    group_name: str = "group1"
    group_context = f"Group context test modified by {email}"
    result: dict[str, Any] = await get_result(
        user=email,
        group_context=group_context,
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupAccessInfo"]
    assert result["data"]["updateGroupAccessInfo"]["success"]

    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group_typed.load(group_name)
    assert group.context == group_context


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_access_info")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_update_group_info_clear_field(
    populate: bool,
    email: str,
) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    group_name: str = "group1"
    group: Group = await loaders.group_typed.load(group_name)
    assert group.context is not None

    result: dict[str, Any] = await get_result(
        user=email,
        group_context="",
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupAccessInfo"]
    assert result["data"]["updateGroupAccessInfo"]["success"]

    loaders.group_typed.clear(group_name)
    group = await loaders.group_typed.load(group_name)
    assert group.context is None
