from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customeradmin@gmail.com"],
        ["hacker@gmail.com"],
        ["system_owner@gmail.com"],
    ],
)
async def test_get_report(populate: bool, email: str) -> None:
    assert populate
    group: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name=group,
    )
    assert "success" in result["data"]["report"]
    assert result["data"]["report"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
        ["executive@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
    ],
)
async def test_get_report_fail(populate: bool, email: str) -> None:
    assert populate
    group: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name=group,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
