from datetime import (
    datetime,
)
from db_model.events.types import (
    Event,
)
from newutils import (
    datetime as datetime_utils,
)


async def filter_events_date(
    events: list[Event],
    min_date: datetime,
) -> list[Event]:
    return [
        event
        for event in events
        if min_date
        and datetime_utils.get_datetime_from_iso_str(event.state.modified_date)
        >= min_date
    ]
