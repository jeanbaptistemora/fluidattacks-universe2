from custom_types import (
    Event as EventType,
)
from datetime import (
    datetime,
)
from db_model.events.enums import (
    EventStatus,
)
from db_model.events.types import (
    Event,
    EventHistory,
)
from dynamodb.types import (
    Item,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    cast,
    Dict,
    List,
)


def format_data(event: EventType) -> EventType:
    historic_state = cast(
        List[Dict[str, str]], event.get("historic_state", [{}, {}])
    )
    event["closing_date"] = "-"
    if historic_state[-1].get("state") == "SOLVED":
        event["closing_date"] = historic_state[-2].get("date", "")

    return event


def event_history(item: Item, history_state: EventStatus) -> EventHistory:
    return EventHistory(
        affectation=item.get["affectation", ""],
        date=item.get["date", ""],
        state=history_state,
    )


def format_event(item: Item) -> Event:
    return Event(
        type=item.get("event_id", ""),
        accessibility=item.get("accessibility", ""),
        affected_components=item.get("affected_components", ""),
        analyst=item.get("analyst", ""),
        client=item.get("client", ""),
        closing_date=item.get("closing_date", ""),
        context=item.get("context", ""),
        detail=item.get("detail", ""),
        evidence_file=item.get("event_id", ""),
        evidence=item.get("event_id", ""),
        historic_state=EventHistory,
        id=item.get("event_id", ""),
        subscription=item.get("event_id", ""),
        action_after_blocking=item.get("action_after_blocking", None),
        action_before_blocking=item.get("action_before_blocking", None),
        evidence_date=item.get("evidence_date", None),
        evidence_file_date=item.get("evidence_file_date", None),
    )


async def filter_events_date(
    events: List[EventType],
    min_date: datetime,
) -> List[EventType]:
    return [
        event
        for event in events
        if min_date
        and datetime_utils.get_from_str(event["historic_state"][-1]["date"])
        >= min_date
    ]
