# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.enums import (
    EventSolutionReason,
    EventStateStatus,
)
from db_model.events.types import (
    Event,
)
import pytest
from typing import (
    Any,
    Optional,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event_solving_reason")
@pytest.mark.parametrize(
    ["email", "event_id", "reason", "other"],
    [
        ["admin@gmail.com", "418900971", "PROBLEM_SOLVED", None],
        ["hacker@gmail.com", "418900972", "PERMISSION_DENIED", None],
        ["reattacker@gmail.com", "418900973", "SUPPLIES_WERE_GIVEN", None],
        ["resourcer@gmail.com", "418900974", "TOE_CHANGE_APPROVED", None],
        [
            "customer_manager@fluidattacks.com",
            "418900975",
            "OTHER",
            "Reason test",
        ],
    ],
)
async def test_update_event_solving_reason(
    populate: bool,
    email: str,
    event_id: str,
    reason: str,
    other: Optional[str],
) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    event: Event = await loaders.event.load(event_id)
    assert event.state.status == EventStateStatus.SOLVED

    result: dict[str, Any] = await get_result(
        user=email, event_id=event_id, reason=reason, other=other
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateEventSolvingReason"]

    loaders = get_new_context()
    event = await loaders.event.load(event_id)
    assert event.state.reason == EventSolutionReason[reason]
    assert event.state.other == other


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_event_solving_reason")
@pytest.mark.parametrize(
    ["email", "event_id", "reason", "other"],
    [
        ["user@gmail.com", "418900971", "PROBLEM_SOLVED", None],
        ["user_manager@gmail.com", "418900972", "PERMISSION_DENIED", None],
        [
            "vulnerability_manager@gmail.com",
            "418900973",
            "SUPPLIES_WERE_GIVEN",
            None,
        ],
        ["reviewer@gmail.com", "418900974", "TOE_CHANGE_APPROVED", None],
    ],
)
async def test_update_event_solving_reason_fail(
    populate: bool,
    email: str,
    event_id: str,
    reason: str,
    other: Optional[str],
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, event_id=event_id, reason=reason, other=other
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
