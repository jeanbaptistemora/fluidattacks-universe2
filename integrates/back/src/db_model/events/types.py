from .enums import (
    EventSolutionReason,
    EventStateStatus,
    EventType,
)
from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
    Optional,
)


class EventEvidence(NamedTuple):
    file_name: str
    modified_date: datetime


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
    modified_date: datetime
    status: EventStateStatus
    comment_id: Optional[str] = None
    other: Optional[str] = None
    reason: Optional[EventSolutionReason] = None


class EventUnreliableIndicators(NamedTuple):
    unreliable_solving_date: Optional[datetime] = None


class Event(NamedTuple):
    client: str
    created_by: str
    created_date: datetime
    description: str
    event_date: datetime
    evidences: EventEvidences
    group_name: str
    hacker: str
    id: str
    state: EventState
    type: EventType
    root_id: Optional[str] = None
    unreliable_indicators: EventUnreliableIndicators = (
        EventUnreliableIndicators()
    )


class EventMetadataToUpdate(NamedTuple):
    client: Optional[str] = None
    description: Optional[str] = None
    root_id: Optional[str] = None
    type: Optional[EventType] = None


class EventUnreliableIndicatorsToUpdate(NamedTuple):
    unreliable_solving_date: Optional[datetime] = None
    clean_unreliable_solving_date: bool = False


class GroupEventsRequest(NamedTuple):
    group_name: str
    is_solved: Optional[bool] = None
