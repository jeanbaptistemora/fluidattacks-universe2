from . import (
    query,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("edit_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_edit_group(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await query(user=email, group=group_name)
    assert "errors" not in result
    assert "success" in result["data"]["editGroup"]
    assert result["data"]["editGroup"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("edit_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
        ["resourcer@gmail.com"],
    ],
)
async def test_edit_group_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await query(user=email, group=group_name)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
