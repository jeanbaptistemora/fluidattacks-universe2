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
)

RegisterByTime = list[list[dict[str, str | Decimal]]]


class GroupState(NamedTuple):
    has_machine: bool
    has_squad: bool
    managed: GroupManaged
    modified_by: str
    modified_date: datetime
    status: GroupStateStatus
    tier: GroupTier
    type: GroupSubscriptionType
    tags: set[str] | None = None
    comments: str | None = None
    justification: GroupStateJustification | None = None
    payment_id: str | None = None
    pending_deletion_date: datetime | None = None
    service: GroupService | None = None


class GroupTreatmentSummary(NamedTuple):
    accepted: int = 0
    accepted_undefined: int = 0
    in_progress: int = 0
    untreated: int = 0


class UnfulfilledStandard(NamedTuple):
    name: str
    unfulfilled_requirements: list[str]


class GroupUnreliableIndicators(NamedTuple):
    closed_vulnerabilities: int | None = None
    code_languages: list[CodeLanguage] | None = None
    exposed_over_time_cvssf: RegisterByTime | None = None
    exposed_over_time_month_cvssf: RegisterByTime | None = None
    exposed_over_time_year_cvssf: RegisterByTime | None = None
    last_closed_vulnerability_days: int | None = None
    last_closed_vulnerability_finding: str | None = None
    max_open_severity: Decimal | None = None
    max_open_severity_finding: str | None = None
    max_severity: Decimal | None = None
    mean_remediate: Decimal | None = None
    mean_remediate_critical_severity: Decimal | None = None
    mean_remediate_high_severity: Decimal | None = None
    mean_remediate_low_severity: Decimal | None = None
    mean_remediate_medium_severity: Decimal | None = None
    open_findings: int | None = None
    open_vulnerabilities: int | None = None
    remediated_over_time: RegisterByTime | None = None
    remediated_over_time_30: RegisterByTime | None = None
    remediated_over_time_90: RegisterByTime | None = None
    remediated_over_time_cvssf: RegisterByTime | None = None
    remediated_over_time_cvssf_30: RegisterByTime | None = None
    remediated_over_time_cvssf_90: RegisterByTime | None = None
    remediated_over_time_month: RegisterByTime | None = None
    remediated_over_time_month_cvssf: RegisterByTime | None = None
    remediated_over_time_year: RegisterByTime | None = None
    remediated_over_time_year_cvssf: RegisterByTime | None = None
    treatment_summary: GroupTreatmentSummary | None = None
    unfulfilled_standards: list[UnfulfilledStandard] | None = None


class GroupFile(NamedTuple):
    description: str
    file_name: str
    modified_by: str
    modified_date: datetime | None = None


class Group(NamedTuple):
    created_by: str
    created_date: datetime
    description: str
    language: GroupLanguage
    name: str
    organization_id: str
    state: GroupState
    agent_token: str | None = None
    business_id: str | None = None
    business_name: str | None = None
    context: str | None = None
    disambiguation: str | None = None
    files: list[GroupFile] | None = None
    policies: Policies | None = None
    sprint_duration: int = 1
    sprint_start_date: datetime | None = None


class GroupMetadataToUpdate(NamedTuple):
    agent_token: str | None = None
    business_id: str | None = None
    business_name: str | None = None
    context: str | None = None
    description: str | None = None
    disambiguation: str | None = None
    files: list[GroupFile] | None = None
    language: GroupLanguage | None = None
    sprint_duration: int | None = None
    sprint_start_date: datetime | None = None
    clean_sprint_start_date: bool = False
