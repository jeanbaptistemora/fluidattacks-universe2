from db_model.findings.enums import (
    FindingSorts,
)
from typing import (
    NamedTuple,
    Optional,
)


class FindingDescriptionToUpdate(NamedTuple):
    affected_systems: Optional[str] = None
    attack_vector_description: Optional[str] = None
    compromised_attributes: Optional[str] = None
    compromised_records: Optional[int] = None
    description: Optional[str] = None
    recommendation: Optional[str] = None
    requirements: Optional[str] = None
    risk: Optional[str] = None
    scenario: Optional[str] = None
    sorts: Optional[FindingSorts] = None
    threat: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None


class FindingDraftToAdd(NamedTuple):
    affected_systems: Optional[str] = None
    analyst_email: Optional[str] = None
    attack_vector_description: Optional[str] = None
    description: Optional[str] = None
    risk: Optional[str] = None
    recommendation: Optional[str] = None
    requirements: Optional[str] = None
    title: Optional[str] = None
    threat: Optional[str] = None
    type: Optional[str] = None
