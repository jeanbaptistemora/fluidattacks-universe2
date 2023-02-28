from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingSorts,
)
from db_model.findings.types import (
    Finding31Severity,
)
from typing import (
    NamedTuple,
)


class FindingDescriptionToUpdate(NamedTuple):
    attack_vector_description: str | None = None
    description: str | None = None
    recommendation: str | None = None
    sorts: FindingSorts | None = None
    threat: str | None = None
    title: str | None = None
    unfulfilled_requirements: list[str] | None = None


class FindingDraftToAdd(NamedTuple):
    attack_vector_description: str
    description: str
    hacker_email: str
    min_time_to_remediate: int | None
    recommendation: str
    requirements: str
    severity: Finding31Severity
    threat: str
    title: str


class FindingAttributesToAdd(NamedTuple):
    attack_vector_description: str
    description: str
    min_time_to_remediate: int | None
    recommendation: str
    severity: Finding31Severity
    source: Source
    threat: str
    title: str
    unfulfilled_requirements: list[str]


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
