from db_model.events.enums import (
    EventSolutionReason,
    EventType,
)
from typing import (
    NamedTuple,
)


class EventAttributesToUpdate(NamedTuple):
    event_type: EventType | None = None
    other_solving_reason: str | None = None
    solving_reason: EventSolutionReason | None = None
