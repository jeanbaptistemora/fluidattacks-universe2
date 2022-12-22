from db_model.findings.enums import (
    FindingSorts,
)
from db_model.findings.types import (
    Finding31Severity,
)
from typing import (
    NamedTuple,
    Optional,
)


class FindingDescriptionToUpdate(NamedTuple):
    attack_vector_description: Optional[str] = None
    description: Optional[str] = None
    recommendation: Optional[str] = None
    sorts: Optional[FindingSorts] = None
    threat: Optional[str] = None
    title: Optional[str] = None


class FindingDraftToAdd(NamedTuple):
    attack_vector_description: str
    description: str
    hacker_email: str
    min_time_to_remediate: Optional[int]
    recommendation: str
    requirements: str
    severity: Finding31Severity
    threat: str
    title: str


class Tracking(NamedTuple):
    cycle: int
    open: int
    closed: int
    date: str
    accepted: int
    accepted_undefined: int
    assigned: str
    justification: str
    safe: int
    vulnerable: int
    effectiveness: Optional[int] = None
    new: Optional[int] = None
    in_progress: Optional[int] = None
