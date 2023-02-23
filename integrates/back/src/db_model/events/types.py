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
)


class EventEvidence(NamedTuple):
    file_name: str
    modified_date: datetime


class EventEvidences(NamedTuple):
    file_1: EventEvidence | None = None
    image_1: EventEvidence | None = None
    image_2: EventEvidence | None = None
    image_3: EventEvidence | None = None
    image_4: EventEvidence | None = None
    image_5: EventEvidence | None = None
    image_6: EventEvidence | None = None


class EventState(NamedTuple):
    modified_by: str
    modified_date: datetime
    status: EventStateStatus
    comment_id: str | None = None
    other: str | None = None
    reason: EventSolutionReason | None = None


class EventUnreliableIndicators(NamedTuple):
    unreliable_solving_date: datetime | None = None


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
    root_id: str | None = None
    unreliable_indicators: EventUnreliableIndicators = (
        EventUnreliableIndicators()
    )


class EventMetadataToUpdate(NamedTuple):
    client: str | None = None
    description: str | None = None
    root_id: str | None = None
    type: EventType | None = None


class EventUnreliableIndicatorsToUpdate(NamedTuple):
    unreliable_solving_date: datetime | None = None
    clean_unreliable_solving_date: bool = False


class GroupEventsRequest(NamedTuple):
    group_name: str
    is_solved: bool | None = None
