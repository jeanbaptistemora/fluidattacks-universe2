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
@pytest.mark.resolver_test_group("update_group_disambiguation")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["resourcer@gmail.com"],
    ],
)
async def test_update_group_info(
    populate: bool,
    email: str,
) -> None:
    assert populate
    group_name: str = "group1"
    disambiguation = f"disambiguation text modified by {email}"
    result: dict[str, Any] = await get_result(
        user=email,
        disambiguation=disambiguation,
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupDisambiguation"]
    assert result["data"]["updateGroupDisambiguation"]["success"]

    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group_typed.load(group_name)
    assert group.disambiguation == disambiguation


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_disambiguation")
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
    assert group.disambiguation is not None

    result: dict[str, Any] = await get_result(
        user=email,
        disambiguation="",
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupDisambiguation"]
    assert result["data"]["updateGroupDisambiguation"]["success"]

    loaders.group_typed.clear(group_name)
    group = await loaders.group_typed.load(group_name)
    assert group.disambiguation is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_disambiguation")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["user@gmail.com"],
        ["reattacker@gmail.com"],
        ["reviewer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_update_group_info_fail(
    populate: bool,
    email: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        disambiguation="Disambiguation test",
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
