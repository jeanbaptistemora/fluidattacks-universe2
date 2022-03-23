from typing import (
    NamedTuple,
    Optional,
)


class EventHistory(NamedTuple):
    affectation: str
    date: str
    state: str


class Event(NamedTuple):
    type: str
    accessibility: str
    affected_components: str
    analyst: str
    client: str
    closing_date: str
    context: str
    detail: str
    evidence_file: str
    evidence: str
    historic_state: EventHistory
    id: str
    subscription: str
    action_after_blocking: Optional[str] = None
    action_before_blocking: Optional[str] = None
    evidence_date: Optional[str] = None
    evidence_file_date: Optional[str] = None
