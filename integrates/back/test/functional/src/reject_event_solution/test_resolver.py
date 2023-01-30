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
@pytest.mark.resolver_test_group("reject_event_solution")
@pytest.mark.parametrize(
    ["email", "event_id", "comments"],
    [
        ["admin@gmail.com", "418900971", "comment test"],
    ],
)
async def test_reject_event_solution(
    populate: bool,
    email: str,
    event_id: str,
    comments: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, event_id=event_id, comments=comments
    )
    assert "errors" not in result
    assert result["data"]["rejectEventSolution"]["success"]

    loaders: Dataloaders = get_new_context()
    event: Event = await loaders.event.load(event_id)
    assert event.state.status == EventStateStatus.CREATED
    event_comments = await loaders.event_comments.load(event_id)
    assert event.state.comment_id in {comment.id for comment in event_comments}


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_event_solution")
@pytest.mark.parametrize(
    ["email", "event_id", "comments"],
    [
        ["user@gmail.com", "418900971", "comment test"],
        ["user_manager@gmail.com", "418900972", "comment test"],
        ["vulnerability_manager@gmail.com", "418900973", "comment test"],
        ["reviewer@gmail.com", "418900974", "comment test"],
    ],
)
async def test_reject_event_solution_access_denied(
    populate: bool,
    email: str,
    event_id: str,
    comments: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, event_id=event_id, comments=comments
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_event_solution")
@pytest.mark.parametrize(
    ["email", "event_id", "comments"],
    [
        ["admin@gmail.com", "418900974", "comment test"],
        ["admin@gmail.com", "418900975", "comment test"],
    ],
)
async def test_reject_event_solution_non_requested(
    populate: bool,
    email: str,
    event_id: str,
    comments: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, event_id=event_id, comments=comments
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The event verification has not been requested"
    )
