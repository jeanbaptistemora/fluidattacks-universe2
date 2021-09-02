from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("stakeholder")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customeradmin@gmail.com"],
        ["reviewer@gmail.com"],
        ["system_owner@gmail.com"],
    ],
)
async def test_get_stakeholder(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        stakeholder=email,
        group=group_name,
    )
    assert "errors" not in result
    assert result["data"]["stakeholder"]["email"] == email
    assert result["data"]["stakeholder"]["role"] == email.split("@")[0]
    assert result["data"]["stakeholder"]["responsibility"] == ""
    assert result["data"]["stakeholder"]["phoneNumber"] == "-"
    assert result["data"]["stakeholder"]["firstLogin"] == ""
    assert result["data"]["stakeholder"]["lastLogin"] == ""


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("stakeholder")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
    ],
)
async def test_get_stakeholder_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        stakeholder=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
