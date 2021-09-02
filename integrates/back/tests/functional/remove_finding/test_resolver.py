from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_finding")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_remove_finding(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "475041513"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeFinding"]
    assert result["data"]["removeFinding"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_finding")
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
    ],
)
async def test_remove_finding_fail(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "475041513"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
