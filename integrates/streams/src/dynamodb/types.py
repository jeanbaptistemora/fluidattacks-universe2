from enum import (
    Enum,
)
from typing import (
    Any,
    NamedTuple,
    Optional,
)


class EventName(str, Enum):
    INSERT = "INSERT"
    MODIFY = "MODIFY"
    REMOVE = "REMOVE"


class Record(NamedTuple):
    event_name: EventName
    item: Optional[dict[str, Any]]
    pk: str
    sk: str
