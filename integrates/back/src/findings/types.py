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
    affected_systems: Optional[str] = None
    attack_vector_description: Optional[str] = None
    compromised_attributes: Optional[str] = None
    description: Optional[str] = None
    recommendation: Optional[str] = None
    sorts: Optional[FindingSorts] = None
    threat: Optional[str] = None
    title: Optional[str] = None


class FindingDraftToAdd(NamedTuple):
    affected_systems: str
    attack_vector_description: str
    description: str
    hacker_email: str
    recommendation: str
    requirements: str
    severity: Finding31Severity
    threat: str
    title: str
