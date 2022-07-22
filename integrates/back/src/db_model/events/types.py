from .enums import (
    EventAccessibility,
    EventActionsAfterBlocking,
    EventActionsBeforeBlocking,
    EventAffectedComponents,
    EventSolutionReason,
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
    other: Optional[str] = None
    reason: Optional[EventSolutionReason] = None


class EventUnreliableIndicators(NamedTuple):
    unreliable_solving_date: Optional[str] = None


class Event(NamedTuple):
    client: str
    description: str
    event_date: str
    evidences: EventEvidences
    group_name: str
    hacker: str
    id: str
    state: EventState
    type: EventType
    accessibility: Optional[set[EventAccessibility]] = None
    action_after_blocking: Optional[
        EventActionsAfterBlocking
    ] = None  # Deprecated
    action_before_blocking: Optional[
        EventActionsBeforeBlocking
    ] = None  # Deprecated
    affected_components: Optional[set[EventAffectedComponents]] = None
    context: Optional[str] = None  # Deprecated
    root_id: Optional[str] = None
    unreliable_indicators: EventUnreliableIndicators = (
        EventUnreliableIndicators()
    )


class EventMetadataToUpdate(NamedTuple):
    affected_components: Optional[set[EventAffectedComponents]] = None
    client: Optional[str] = None
    description: Optional[str] = None
    type: Optional[EventType] = None
    clean_affected_components: bool = False


class EventUnreliableIndicatorsToUpdate(NamedTuple):
    unreliable_solving_date: Optional[str] = None
