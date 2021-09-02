from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("solve_event")
@pytest.mark.parametrize(
    ["email", "event_id"],
    [
        ["admin@gmail.com", "418900971"],
        ["hacker@gmail.com", "418900972"],
        ["reattacker@gmail.com", "418900973"],
        ["resourcer@gmail.com", "418900974"],
        ["system_owner@gmail.com", "418900975"],
    ],
)
async def test_solve_event(populate: bool, email: str, event_id: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" not in result
    assert "success" in result["data"]["solveEvent"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("solve_event")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_solve_event_fail(populate: bool, email: str) -> None:
    assert populate
    event_id: str = "418900971"
    result: Dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
