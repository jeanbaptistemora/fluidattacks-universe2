from .enums import (
    EventStateStatus,
)
from typing import (
    NamedTuple,
    Optional,
)


class EventState(NamedTuple):
    modified_by: str
    modified_date: str
    status: EventStateStatus


class Event(NamedTuple):
    accessibility: str
    affected_components: str
    client: str
    description: str
    group_name: str
    hacker: str
    id: str
    state: EventState
    type: str
    action_after_blocking: Optional[str] = None  # Deprecated
    action_before_blocking: Optional[str] = None  # Deprecated
    context: Optional[str] = None  # Deprecated
    evidence: Optional[str] = None
    evidence_date: Optional[str] = None
    evidence_file: Optional[str] = None
    evidence_file_date: Optional[str] = None
