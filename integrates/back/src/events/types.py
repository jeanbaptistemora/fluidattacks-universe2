from db_model.events.enums import (
    EventType,
)
from typing import (
    NamedTuple,
    Optional,
)


class EventAttributesToUpdate(NamedTuple):
    event_type: Optional[EventType] = None
