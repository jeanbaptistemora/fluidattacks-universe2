from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.enums import (
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidences,
    GroupEventsRequest,
)
from newutils import (
    datetime as datetime_utils,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_event")
@pytest.mark.parametrize(
    ["email", "events_in_db"],
    [
        ["admin@gmail.com", 0],
        ["hacker@gmail.com", 1],
        ["reattacker@gmail.com", 2],
        ["resourcer@gmail.com", 3],
        ["customer_manager@fluidattacks.com", 4],
    ],
)
async def test_add_event(
    populate: bool, email: str, events_in_db: int
) -> None:
    assert populate
    group_name: str = "group1"
    loaders: Dataloaders = get_new_context()
    group_events = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    assert len(group_events) == events_in_db

    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addEvent"]
    assert result["data"]["addEvent"]

    loaders = get_new_context()
    group_events = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    assert len(group_events) == events_in_db + 1
    event: Event = next(
        event for event in group_events if event.hacker == email
    )
    assert event.client == "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    assert event.description == "hacker create new event"
    assert (
        datetime_utils.get_as_utc_iso_format(event.event_date)
        == "2020-02-01T00:00:00+00:00"
    )
    assert event.evidences == EventEvidences()
    assert event.group_name == group_name
    assert event.hacker == email
    assert event.state.status == EventStateStatus.CREATED
    assert event.type == EventType.MISSING_SUPPLIES
    assert event.root_id == "63298a73-9dff-46cf-b42d-9b2f01a56690"


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
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
