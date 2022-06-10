from datetime import (
    datetime,
)
from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.types import (
    Event,
    EventState,
)
from dynamodb.types import (
    Item,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    cast,
)


async def filter_events_date(
    events: list[dict[str, Any]],
    min_date: datetime,
) -> list[dict[str, Any]]:
    return [
        event
        for event in events
        if min_date
        and datetime_utils.get_from_str(event["historic_state"][-1]["date"])
        >= min_date
    ]


def format_data(event: dict[str, Any]) -> dict[str, Any]:
    historic_state = cast(
        list[dict[str, str]], event.get("historic_state", [{}, {}])
    )
    event["closing_date"] = "-"
    if historic_state[-1].get("state") == "SOLVED":
        event["closing_date"] = historic_state[-2].get("date", "")

    return event


def format_state(item: Item) -> EventState:
    historic_state = item["historic_state"]
    last_state = historic_state[-1]
    return EventState(
        modified_by=last_state["analyst"],
        modified_date=last_state["date"],
        status=EventStateStatus[last_state["state"]],
    )


def format_event(item: Item) -> Event:
    return Event(
        action_after_blocking=item.get("action_after_blocking", None),
        action_before_blocking=item.get("action_before_blocking", None),
        accessibility=item.get("accessibility", ""),
        affected_components=item.get("affected_components", ""),
        client=item.get("client", ""),
        context=item.get("context", ""),
        description=item["detail"],
        evidence=item.get("event_id", ""),
        evidence_date=item.get("evidence_date", None),
        evidence_file=item.get("event_id", ""),
        evidence_file_date=item.get("evidence_file_date", None),
        group_name=item["project_name"],
        hacker=item["analyst"],
        id=item["event_id"],
        state=format_state(item),
        type=item["event_type"],
    )
