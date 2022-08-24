from .enums import (
    EventActionsAfterBlocking,
    EventActionsBeforeBlocking,
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
    file_1: Optional[EventEvidence] = None
    image_1: Optional[EventEvidence] = None
    image_2: Optional[EventEvidence] = None
    image_3: Optional[EventEvidence] = None
    image_4: Optional[EventEvidence] = None
    image_5: Optional[EventEvidence] = None
    image_6: Optional[EventEvidence] = None


class EventState(NamedTuple):
    modified_by: str
    modified_date: str
    status: EventStateStatus
    comment_id: Optional[str] = None
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
    action_after_blocking: Optional[
        EventActionsAfterBlocking
    ] = None  # Deprecated
    action_before_blocking: Optional[
        EventActionsBeforeBlocking
    ] = None  # Deprecated
    context: Optional[str] = None  # Deprecated
    root_id: Optional[str] = None
    unreliable_indicators: EventUnreliableIndicators = (
        EventUnreliableIndicators()
    )


class EventMetadataToUpdate(NamedTuple):
    client: Optional[str] = None
    description: Optional[str] = None
    type: Optional[EventType] = None


class EventUnreliableIndicatorsToUpdate(NamedTuple):
    unreliable_solving_date: Optional[str] = None


class GroupEventsRequest(NamedTuple):
    group_name: str
    is_solved: Optional[bool] = None
