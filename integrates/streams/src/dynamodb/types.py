from enum import (
    Enum,
)
from typing import (
    Any,
    Callable,
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


class Trigger(NamedTuple):
    batch_size: int
    records_filter: Callable[[Record], bool]
    records_processor: Callable[[tuple[Record, ...]], None]
