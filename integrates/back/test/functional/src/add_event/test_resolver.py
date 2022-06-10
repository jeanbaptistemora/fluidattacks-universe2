from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_event")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_add_event(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert result["data"]["addEvent"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_event")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["reviewer@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_add_event_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
