from .enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateJustification,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from datetime import (
    datetime,
)
from db_model.types import (
    CodeLanguage,
    Policies,
)
from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
    Optional,
    Union,
)

RegisterByTime = list[list[dict[str, Union[str, Decimal]]]]


class GroupState(NamedTuple):
    has_machine: bool
    has_squad: bool
    managed: GroupManaged
    modified_by: str
    modified_date: datetime
    status: GroupStateStatus
    tier: GroupTier
    type: GroupSubscriptionType
    tags: Optional[set[str]] = None
    comments: Optional[str] = None
    justification: Optional[GroupStateJustification] = None
    payment_id: Optional[str] = None
    pending_deletion_date: Optional[datetime] = None
    service: Optional[GroupService] = None


class GroupTreatmentSummary(NamedTuple):
    accepted: int = 0
    accepted_undefined: int = 0
    in_progress: int = 0
    untreated: int = 0


class UnfulfilledStandard(NamedTuple):
    name: str
    unfulfilled_requirements: list[str]


class GroupUnreliableIndicators(NamedTuple):
    closed_vulnerabilities: Optional[int] = None
    code_languages: Optional[list[CodeLanguage]] = None
    exposed_over_time_cvssf: Optional[RegisterByTime] = None
    exposed_over_time_month_cvssf: Optional[RegisterByTime] = None
    exposed_over_time_year_cvssf: Optional[RegisterByTime] = None
    last_closed_vulnerability_days: Optional[int] = None
    last_closed_vulnerability_finding: Optional[str] = None
    max_open_severity: Optional[Decimal] = None
    max_open_severity_finding: Optional[str] = None
    max_severity: Optional[Decimal] = None
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
    unfulfilled_standards: Optional[list[UnfulfilledStandard]] = None


class GroupFile(NamedTuple):
    description: str
    file_name: str
    modified_by: str
    modified_date: Optional[datetime] = None


class Group(NamedTuple):
    created_by: str
    created_date: datetime
    description: str
    language: GroupLanguage
    name: str
    organization_id: str
    state: GroupState
    agent_token: Optional[str] = None
    business_id: Optional[str] = None
    business_name: Optional[str] = None
    context: Optional[str] = None
    disambiguation: Optional[str] = None
    files: Optional[list[GroupFile]] = None
    policies: Optional[Policies] = None
    sprint_duration: int = 1
    sprint_start_date: Optional[datetime] = None


class GroupMetadataToUpdate(NamedTuple):
    agent_token: Optional[str] = None
    business_id: Optional[str] = None
    business_name: Optional[str] = None
    context: Optional[str] = None
    description: Optional[str] = None
    disambiguation: Optional[str] = None
    files: Optional[list[GroupFile]] = None
    language: Optional[GroupLanguage] = None
    sprint_duration: Optional[int] = None
    sprint_start_date: Optional[datetime] = None
    clean_sprint_start_date: bool = False
