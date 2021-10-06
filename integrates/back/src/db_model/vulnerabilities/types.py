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
    modified_by: str
    modified_date: str
    source: Source
    status: VulnerabilityStateStatus
    approval_status: Optional[VulnerabilityApprovalStatus] = None
    justification: Optional[VulnerabilityDeletionJustification] = None


class VulnerabilityTreatment(NamedTuple):
    modified_date: str
    status: VulnerabilityTreatmentStatus
    accepted_until: Optional[str] = None
    acceptance_status: Optional[VulnerabilityAcceptanceStatus] = None
    justification: Optional[str] = None
    manager: Optional[str] = None
    modified_by: Optional[str] = None


class VulnerabilityVerification(NamedTuple):
    modified_date: str
    status: VulnerabilityVerificationStatus
    modified_by: Optional[str] = None


class VulnerabilityZeroRisk(NamedTuple):
    comment_id: str
    modified_by: str
    modified_date: str
    status: VulnerabilityZeroRiskStatus


class Vulnerability(NamedTuple):
    finding_id: str
    specific: str
    uuid: str
    where: str
    type: VulnerabilityType
    bug_tracking_system_url: Optional[str] = None
    commit: Optional[str] = None
    custom_severity: Optional[int] = None
    hash: Optional[int] = None
    repo: Optional[str] = None
    state: Optional[VulnerabilityState] = None
    stream: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    treatment: Optional[VulnerabilityTreatment] = None
    verification: Optional[VulnerabilityVerification] = None
    zero_risk: Optional[VulnerabilityZeroRisk] = None


class VulnerabilityMetadataToUpdate(NamedTuple):
    bug_tracking_system_url: Optional[str]
    commit: Optional[str]
    custom_severity: Optional[int]
    hash: Optional[int]
    repo: Optional[str]
    specific: Optional[str]
    stream: Optional[List[str]]
    tags: Optional[List[str]]
    type: Optional[VulnerabilityType]
    where: Optional[str]
