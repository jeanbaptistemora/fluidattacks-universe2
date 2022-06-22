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
from decimal import (
    Decimal,
)
from dynamodb.types import (
    PageInfo,
)
from typing import (
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union,
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
    assigned: Optional[str] = None
    modified_by: Optional[str] = None


class VulnerabilityUnreliableIndicators(NamedTuple):
    unreliable_report_date: str = ""
    unreliable_source: Source = Source.ASM
    unreliable_efficacy: Optional[Decimal] = None
    unreliable_last_reattack_date: Optional[str] = None
    unreliable_last_reattack_requester: Optional[str] = None
    unreliable_last_requested_reattack_date: Optional[str] = None
    unreliable_reattack_cycles: Optional[int] = None
    unreliable_treatment_changes: Optional[int] = None


class VulnerabilityVerification(NamedTuple):
    modified_date: str
    status: VulnerabilityVerificationStatus
    event_id: Optional[str] = None


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
    developer: Optional[str] = None
    event_id: Optional[str] = None
    group_name: Optional[str] = None
    hash: Optional[int] = None
    root_id: Optional[str] = None
    skims_method: Optional[str] = None
    skims_technique: Optional[str] = None
    stream: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    treatment: Optional[VulnerabilityTreatment] = None
    unreliable_indicators: VulnerabilityUnreliableIndicators = (
        VulnerabilityUnreliableIndicators()
    )
    verification: Optional[VulnerabilityVerification] = None
    zero_risk: Optional[VulnerabilityZeroRisk] = None


class VulnerabilityEdge(NamedTuple):
    node: Vulnerability
    cursor: str


class VulnerabilitiesConnection(NamedTuple):
    edges: Tuple[VulnerabilityEdge, ...]
    page_info: PageInfo


class VulnerabilityMetadataToUpdate(NamedTuple):
    bug_tracking_system_url: Optional[str] = None
    commit: Optional[str] = None
    custom_severity: Optional[str] = None
    hash: Optional[int] = None
    skims_method: Optional[str] = None
    skims_technique: Optional[str] = None
    developer: Optional[str] = None
    root_id: Optional[str] = None
    specific: Optional[str] = None
    stream: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    type: Optional[VulnerabilityType] = None
    where: Optional[str] = None


VulnerabilityHistoric = Union[
    Tuple[VulnerabilityState, ...],
    Tuple[VulnerabilityTreatment, ...],
    Tuple[VulnerabilityVerification, ...],
    Tuple[VulnerabilityZeroRisk, ...],
]

VulnerabilityHistoricEntry = Union[
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
]


class VulnerabilityUnreliableIndicatorsToUpdate(NamedTuple):
    unreliable_efficacy: Optional[Decimal] = None
    unreliable_last_reattack_date: Optional[str] = None
    unreliable_last_reattack_requester: Optional[str] = None
    unreliable_last_requested_reattack_date: Optional[str] = None
    unreliable_reattack_cycles: Optional[int] = None
    unreliable_report_date: Optional[str] = None
    unreliable_source: Optional[Source] = None
    unreliable_treatment_changes: Optional[int] = None


class VulnerabilityFilters(NamedTuple):
    treatment_status: Optional[str] = None
    verification_status: Optional[str] = None
    where: Optional[str] = None


class FindingVulnerabilitiesZrRequest(NamedTuple):
    finding_id: str
    after: Optional[str] = None
    filters: VulnerabilityFilters = VulnerabilityFilters()
    first: Optional[int] = None
    paginate: bool = False
    state_status: Optional[VulnerabilityStateStatus] = None
    verification_status: Optional[VulnerabilityVerificationStatus] = None


class FindingVulnerabilitiesToReattackRequest(NamedTuple):
    finding_id: str
    after: Optional[str] = None
    first: Optional[int] = None
    paginate: bool = False
