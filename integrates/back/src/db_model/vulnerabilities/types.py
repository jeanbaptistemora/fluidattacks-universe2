from .enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
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
    justification: Optional[StateRemovalJustification] = None


class VulnerabilityTreatment(NamedTuple):
    modified_date: str
    status: VulnerabilityTreatmentStatus
    acceptance_status: Optional[VulnerabilityAcceptanceStatus] = None
    accepted_until: Optional[str] = None
    justification: Optional[str] = None
    manager: Optional[str] = None
    modified_by: Optional[str] = None


class VulnerabilityVerification(NamedTuple):
    modified_date: str
    status: VulnerabilityVerificationStatus


class VulnerabilityZeroRisk(NamedTuple):
    comment_id: str
    modified_by: str
    modified_date: str
    status: VulnerabilityZeroRiskStatus


class Vulnerability(NamedTuple):
    finding_id: str
    id: str
    specific: str
    state: VulnerabilityState
    type: VulnerabilityType
    where: str
    bug_tracking_system_url: Optional[str] = None
    commit: Optional[str] = None
    custom_severity: Optional[int] = None
    hash: Optional[int] = None
    repo: Optional[str] = None
    skims_method: Optional[str] = None
    stream: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    treatment: Optional[VulnerabilityTreatment] = None
    verification: Optional[VulnerabilityVerification] = None
    zero_risk: Optional[VulnerabilityZeroRisk] = None


class VulnerabilityMetadataToUpdate(NamedTuple):
    bug_tracking_system_url: Optional[str] = None
    commit: Optional[str] = None
    custom_severity: Optional[int] = None
    hash: Optional[int] = None
    repo: Optional[str] = None
    skims_method: Optional[str] = None
    specific: Optional[str] = None
    stream: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    type: Optional[VulnerabilityType] = None
    where: Optional[str] = None
