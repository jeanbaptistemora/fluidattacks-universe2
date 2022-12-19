from .enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from datetime import (
    datetime,
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
from serializers import (
    Snippet,
)
from typing import (
    NamedTuple,
    Optional,
    Union,
)


class VulnerabilityTool(NamedTuple):
    name: str
    impact: VulnerabilityToolImpact


class VulnerabilityState(NamedTuple):
    modified_by: str
    modified_date: datetime
    source: Source
    specific: str
    status: VulnerabilityStateStatus
    where: str
    commit: Optional[str] = None
    justification: Optional[StateRemovalJustification] = None
    tool: Optional[VulnerabilityTool] = None
    snippet: Optional[Snippet] = None


class VulnerabilityTreatment(NamedTuple):
    modified_date: datetime
    status: VulnerabilityTreatmentStatus
    acceptance_status: Optional[VulnerabilityAcceptanceStatus] = None
    accepted_until: Optional[datetime] = None
    justification: Optional[str] = None
    assigned: Optional[str] = None
    modified_by: Optional[str] = None


class VulnerabilityUnreliableIndicators(NamedTuple):
    unreliable_closing_date: Optional[datetime] = None
    unreliable_source: Source = Source.ASM
    unreliable_efficacy: Optional[Decimal] = None
    unreliable_last_reattack_date: Optional[datetime] = None
    unreliable_last_reattack_requester: Optional[str] = None
    unreliable_last_requested_reattack_date: Optional[datetime] = None
    unreliable_reattack_cycles: Optional[int] = None
    unreliable_treatment_changes: Optional[int] = None


class VulnerabilityVerification(NamedTuple):
    modified_date: datetime
    status: VulnerabilityVerificationStatus
    event_id: Optional[str] = None


class VulnerabilityZeroRisk(NamedTuple):
    comment_id: str
    modified_by: str
    modified_date: datetime
    status: VulnerabilityZeroRiskStatus


class Vulnerability(NamedTuple):
    created_by: str
    created_date: datetime
    finding_id: str
    group_name: str
    hacker_email: str
    id: str
    state: VulnerabilityState
    type: VulnerabilityType
    bug_tracking_system_url: Optional[str] = None
    custom_severity: Optional[int] = None
    developer: Optional[str] = None
    event_id: Optional[str] = None
    hash: Optional[int] = None
    root_id: Optional[str] = None
    skims_method: Optional[str] = None
    skims_technique: Optional[str] = None
    stream: Optional[list[str]] = None
    tags: Optional[list[str]] = None
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
    edges: tuple[VulnerabilityEdge, ...]
    page_info: PageInfo
    total: Optional[int] = None


class VulnerabilityMetadataToUpdate(NamedTuple):
    bug_tracking_system_url: Optional[str] = None
    created_by: Optional[str] = None
    created_date: Optional[datetime] = None
    custom_severity: Optional[str] = None
    hacker_email: Optional[str] = None
    hash: Optional[int] = None
    skims_method: Optional[str] = None
    skims_technique: Optional[str] = None
    developer: Optional[str] = None
    root_id: Optional[str] = None
    stream: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    type: Optional[VulnerabilityType] = None


VulnerabilityHistoric = Union[
    tuple[VulnerabilityState, ...],
    tuple[VulnerabilityTreatment, ...],
    tuple[VulnerabilityVerification, ...],
    tuple[VulnerabilityZeroRisk, ...],
]

VulnerabilityHistoricEntry = Union[
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
]


class VulnerabilityUnreliableIndicatorsToUpdate(NamedTuple):
    unreliable_closing_date: Optional[datetime] = None
    unreliable_efficacy: Optional[Decimal] = None
    unreliable_last_reattack_date: Optional[datetime] = None
    unreliable_last_reattack_requester: Optional[str] = None
    unreliable_last_requested_reattack_date: Optional[datetime] = None
    unreliable_reattack_cycles: Optional[int] = None
    unreliable_source: Optional[Source] = None
    unreliable_treatment_changes: Optional[int] = None
    clean_unreliable_closing_date: bool = False
    clean_unreliable_last_reattack_date: bool = False
    clean_unreliable_last_requested_reattack_date: bool = False


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
