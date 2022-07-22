from db_model.events.enums import (
    EventAffectedComponents,
    EventType,
)
from typing import (
    NamedTuple,
    Optional,
)


class EventAttributesToUpdate(NamedTuple):
    event_type: Optional[EventType] = None
    affected_components: Optional[set[EventAffectedComponents]] = None
