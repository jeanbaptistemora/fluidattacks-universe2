from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.events.enums import (
    EventStateStatus,
    EventType,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event")
@pytest.mark.parametrize(
    [
        "email",
        "event_id",
        "event_type",
        "solving_reason",
        "other_solving_reason",
    ],
    [
        [
            "admin@gmail.com",
            "418900971",
            "AUTHORIZATION_SPECIAL_ATTACK",
            "PERMISSION_DENIED",
            "",
        ],
        [
            "admin@gmail.com",
            "418900972",
            "DATA_UPDATE_REQUIRED",
            "DATA_UPDATED",
            "",
        ],
        ["admin@gmail.com", "418900974", "OTHER", "OTHER", "Reason"],
        [
            "admin@gmail.com",
            "418900974",
            "TOE_DIFFERS_APPROVED",
            "TOE_CHANGE_APPROVED",
            "",
        ],
        ["admin@gmail.com", "418900975", "OTHER", "OTHER", "Reason"],
    ],
)
async def test_update_event(  # pylint: disable=too-many-arguments
    populate: bool,
    email: str,
    event_id: str,
    event_type: str,
    solving_reason: str,
    other_solving_reason: str,
) -> None:
    assert populate
    loaders = get_new_context()
    event = await loaders.event.load(event_id)
    assert event
    assert event.state.status == EventStateStatus.SOLVED

    result: dict[str, Any] = await get_result(
        user=email,
        event_id=event_id,
        event_type=event_type,
        solving_reason=solving_reason,
        other_solving_reason=other_solving_reason,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateEvent"]

    loaders = get_new_context()
    event = await loaders.event.load(event_id)
    assert event
    assert event.type == EventType[event_type]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event")
@pytest.mark.parametrize(
    [
        "email",
        "event_id",
        "event_type",
        "solving_reason",
        "other_solving_reason",
    ],
    [
        [
            "user@gmail.com",
            "418900971",
            "AUTHORIZATION_SPECIAL_ATTACK",
            "PERMISSION_DENIED",
            "",
        ],
        [
            "reviewer@gmail.com",
            "418900972",
            "DATA_UPDATE_REQUIRED",
            "DATA_UPDATED",
            "",
        ],
    ],
)
async def test_update_event_fail(  # pylint: disable=too-many-arguments
    populate: bool,
    email: str,
    event_id: str,
    event_type: str,
    solving_reason: str,
    other_solving_reason: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        event_id=event_id,
        event_type=event_type,
        solving_reason=solving_reason,
        other_solving_reason=other_solving_reason,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
