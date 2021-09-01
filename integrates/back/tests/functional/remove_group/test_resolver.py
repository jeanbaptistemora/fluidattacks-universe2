from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_remove_group(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, group=group_name, reason="NO_SYSTEM"
    )
    assert "errors" not in result
    assert result["data"]["removeGroup"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["closer@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["resourcer@gmail.com"],
        ["executive@gmail.com"],
        ["reviewer@gmail.com"],
        ["group_manager@gmail.com"],
    ],
)
async def test_remove_group_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group2"
    result: Dict[str, Any] = await get_result(
        user=email, group=group_name, reason="NO_SYSTEM"
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
