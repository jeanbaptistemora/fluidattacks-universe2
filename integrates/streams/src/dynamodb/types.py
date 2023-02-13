from collections.abc import (
    Callable,
)
from enum import (
    Enum,
)
from typing import (
    Any,
    NamedTuple,
)

Item = dict[str, Any]


class HookEvent(str, Enum):
    DELETED_VULNERABILITY = "Vulnerability was deleted"
    EDITED_VULNERABILITY = "Vulnerability was edited"
    REPORTED_VULNERABILITY = "Vulnerability was reported"


class StreamEvent(str, Enum):
    INSERT = "INSERT"
    MODIFY = "MODIFY"
    REMOVE = "REMOVE"


class Record(NamedTuple):
    event_name: StreamEvent
    new_image: Item | None
    old_image: Item | None
    pk: str
    sequence_number: str
    sk: str


class Trigger(NamedTuple):
    records_filter: Callable[[Record], bool]
    records_processor: Callable[[tuple[Record, ...]], None]
