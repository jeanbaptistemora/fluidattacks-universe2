from db_model.events.enums import (
    EventSolutionReason,
    EventType,
)
from typing import (
    NamedTuple,
    Optional,
)


class EventAttributesToUpdate(NamedTuple):
    event_type: Optional[EventType] = None
    other_solving_reason: Optional[str] = None
    solving_reason: Optional[EventSolutionReason] = None
