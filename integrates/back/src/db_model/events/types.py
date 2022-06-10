from .enums import (
    EventAccessibility,
    EventAffectedComponents,
    EventStateStatus,
    EventType,
)
from typing import (
    NamedTuple,
    Optional,
)


class EventEvidence(NamedTuple):
    file_name: str
    modified_date: str


class EventEvidences(NamedTuple):
    file: Optional[EventEvidence] = None
    image: Optional[EventEvidence] = None


class EventState(NamedTuple):
    modified_by: str
    modified_date: str
    status: EventStateStatus


class Event(NamedTuple):
    accessibility: set[EventAccessibility]
    client: str
    description: str
    evidences: EventEvidences
    group_name: str
    hacker: str
    id: str
    state: EventState
    type: EventType
    action_after_blocking: Optional[str] = None  # Deprecated
    action_before_blocking: Optional[str] = None  # Deprecated
    affected_components: Optional[set[EventAffectedComponents]] = None
    context: Optional[str] = None  # Deprecated
    root_id: Optional[str] = None
