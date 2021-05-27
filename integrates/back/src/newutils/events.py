from datetime import datetime
from typing import (
    Dict,
    List,
    cast,
)

from custom_types import Event as EventType
from newutils import datetime as datetime_utils


def format_data(event: EventType) -> EventType:
    historic_state = cast(
        List[Dict[str, str]], event.get("historic_state", [{}, {}])
    )
    event["closing_date"] = "-"
    if historic_state[-1].get("state") == "SOLVED":
        event["closing_date"] = historic_state[-2].get("date", "")

    return event


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
