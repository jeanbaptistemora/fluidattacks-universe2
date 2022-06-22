from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.types import (
    Event,
)
import pytest
from typing import (
    Any,
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
        ["customer_manager@fluidattacks.com", "418900975"],
    ],
)
async def test_solve_event(populate: bool, email: str, event_id: str) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    event: Event = await loaders.event.load(event_id)
    assert event.state.status == EventStateStatus.CREATED

    result: dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" not in result
    assert "success" in result["data"]["solveEvent"]

    loaders = get_new_context()
    event = await loaders.event.load(event_id)
    assert event.state.status == EventStateStatus.SOLVED
    assert event.state.modified_by == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("solve_event")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_solve_event_fail(populate: bool, email: str) -> None:
    assert populate
    event_id: str = "418900971"
    result: dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
