from .enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityApprovalStatus,
    VulnerabilityDeletionJustification,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.enums import (
    Source,
)
from typing import (
    List,
    NamedTuple,
    Optional,
)


class VulnerabilityState(NamedTuple):
    approval_status: Optional[VulnerabilityApprovalStatus]
    justification: Optional[VulnerabilityDeletionJustification]
    modified_by: str
    modified_date: str
    source: Source
    status: VulnerabilityStateStatus


class VulnerabilityTreatment(NamedTuple):
    accepted_until: Optional[str]
    acceptance_status: Optional[VulnerabilityAcceptanceStatus]
    justification: Optional[str]
    manager: Optional[str]
    modified_by: str
    modified_date: str
    status: VulnerabilityTreatmentStatus


class VulnerabilityVerification(NamedTuple):
    modified_by: str
    modified_date: str
    status: VulnerabilityVerificationStatus


class VulnerabilityZeroRisk(NamedTuple):
    comment_id: str
    modified_by: str
    modified_date: str
    status: VulnerabilityZeroRiskStatus


class Vulnerability(NamedTuple):
    bts_url: Optional[str]
    commit: Optional[str]
    custom_severity: Optional[int]
    finding_id: str
    hash: Optional[int]
    repo: Optional[str]
    specific: str
    state: VulnerabilityState
    stream: Optional[List[str]]
    uuid: str
    tags: Optional[List[str]]
    treatment: Optional[VulnerabilityTreatment]
    type: VulnerabilityType
    verification: Optional[VulnerabilityVerification]
    where: str
    zero_risk: Optional[VulnerabilityZeroRisk]


class VulnerabilityMetadataToUpdate(NamedTuple):
    bts_url: Optional[str]
    commit: Optional[str]
    custom_severity: Optional[int]
    hash: Optional[int]
    repo: Optional[str]
    specific: Optional[str]
    stream: Optional[List[str]]
    tags: Optional[List[str]]
    type: Optional[VulnerabilityType]
    where: Optional[str]
