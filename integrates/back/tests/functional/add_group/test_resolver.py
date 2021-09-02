from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_group(populate: bool, email: str) -> None:
    assert populate
    org_name: str = "orgtest"
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, org=org_name, group=group_name
    )
    assert "errors" not in result
    assert "success" in result["data"]["addGroup"]
    assert result["data"]["addGroup"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["system_owner@gmail.com"],
    ],
)
async def test_add_group_fail(populate: bool, email: str) -> None:
    assert populate
    org_name: str = "orgtest"
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, org=org_name, group=group_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
