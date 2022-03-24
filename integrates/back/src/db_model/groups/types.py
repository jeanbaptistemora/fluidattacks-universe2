from .enums import (
    GroupLanguage,
    GroupService,
    GroupStateRemovalJustification,
    GroupStateStatus,
    GroupStateUpdationJustification,
    GroupSubscriptionType,
    GroupTier,
)
from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
    Optional,
    Union,
)

GroupStatusJustification = Union[
    GroupStateRemovalJustification,
    GroupStateUpdationJustification,
]
RegisterByTime = list[list[dict[str, Union[str, Decimal]]]]


class GroupState(NamedTuple):
    has_machine: bool
    has_squad: bool
    modified_by: str
    modified_date: str
    status: GroupStateStatus
    tier: GroupTier
    type: GroupSubscriptionType
    comments: Optional[str] = None
    justification: Optional[GroupStatusJustification] = None
    pending_deletion_date: Optional[str] = None
    service: Optional[GroupService] = None


class GroupTreatmentSummary(NamedTuple):
    accepted: int = 0
    accepted_undefined: int = 0
    in_progress: int = 0
    new: int = 0


class GroupUnreliableIndicators(NamedTuple):
    closed_vulnerabilities: Optional[int] = None
    exposed_over_time_cvssf: Optional[RegisterByTime] = None
    exposed_over_time_month_cvssf: Optional[RegisterByTime] = None
    exposed_over_time_year_cvssf: Optional[RegisterByTime] = None
    last_closed_vulnerability_days: Optional[Decimal] = None
    last_closed_vulnerability_finding: Optional[str] = None
    max_open_severity: Optional[Decimal] = None
    max_open_severity_finding: Optional[str] = None
    mean_remediate: Optional[Decimal] = None
    mean_remediate_critical_severity: Optional[Decimal] = None
    mean_remediate_high_severity: Optional[Decimal] = None
    mean_remediate_low_severity: Optional[Decimal] = None
    mean_remediate_medium_severity: Optional[Decimal] = None
    open_findings: Optional[int] = None
    open_vulnerabilities: Optional[int] = None
    remediated_over_time: Optional[RegisterByTime] = None
    remediated_over_time_30: Optional[RegisterByTime] = None
    remediated_over_time_90: Optional[RegisterByTime] = None
    remediated_over_time_cvssf: Optional[RegisterByTime] = None
    remediated_over_time_cvssf_30: Optional[RegisterByTime] = None
    remediated_over_time_cvssf_90: Optional[RegisterByTime] = None
    remediated_over_time_month: Optional[RegisterByTime] = None
    remediated_over_time_month_cvssf: Optional[RegisterByTime] = None
    remediated_over_time_year: Optional[RegisterByTime] = None
    remediated_over_time_year_cvssf: Optional[RegisterByTime] = None
    treatment_summary: Optional[GroupTreatmentSummary] = None


class GroupFile(NamedTuple):
    description: str
    filename: str
    modified_by: str
    modified_date: Optional[str] = None


class Group(NamedTuple):
    business_id: Optional[str]
    business_name: Optional[str]
    description: str
    language: GroupLanguage
    name: str
    organization_name: str
    state: GroupState
    agent_token: Optional[str] = None
    context: Optional[str] = None
    disambiguation: Optional[str] = None
    files: Optional[list[GroupFile]] = None
    tags: Optional[set[str]] = None


class GroupMetadataToUpdate(NamedTuple):
    context: Optional[str] = None
    description: Optional[str] = None
    disambiguation: Optional[str] = None
    language: Optional[GroupLanguage] = None
    tags: Optional[set[str]] = None
