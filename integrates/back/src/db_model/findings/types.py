from .enums import (
    FindingSorts,
    FindingStateStatus,
    FindingStatus,
    FindingVerificationStatus,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
    Optional,
    Set,
    Union,
)


class FindingState(NamedTuple):
    modified_by: str
    modified_date: str
    source: Source
    status: FindingStateStatus
    justification: StateRemovalJustification = (
        StateRemovalJustification.NO_JUSTIFICATION
    )


class FindingVerification(NamedTuple):
    comment_id: str
    modified_by: str
    modified_date: str
    status: FindingVerificationStatus
    vulnerability_ids: Optional[Set[str]] = None


class FindingEvidence(NamedTuple):
    description: str
    modified_date: str
    url: str


class FindingEvidences(NamedTuple):
    animation: Optional[FindingEvidence] = None
    evidence1: Optional[FindingEvidence] = None
    evidence2: Optional[FindingEvidence] = None
    evidence3: Optional[FindingEvidence] = None
    evidence4: Optional[FindingEvidence] = None
    evidence5: Optional[FindingEvidence] = None
    exploitation: Optional[FindingEvidence] = None
    records: Optional[FindingEvidence] = None


class Finding20Severity(NamedTuple):
    access_complexity: Decimal = Decimal("0.0")
    access_vector: Decimal = Decimal("0.0")
    authentication: Decimal = Decimal("0.0")
    availability_impact: Decimal = Decimal("0.0")
    availability_requirement: Decimal = Decimal("0.0")
    collateral_damage_potential: Decimal = Decimal("0.0")
    confidence_level: Decimal = Decimal("0.0")
    confidentiality_impact: Decimal = Decimal("0.0")
    confidentiality_requirement: Decimal = Decimal("0.0")
    exploitability: Decimal = Decimal("0.0")
    finding_distribution: Decimal = Decimal("0.0")
    integrity_impact: Decimal = Decimal("0.0")
    integrity_requirement: Decimal = Decimal("0.0")
    resolution_level: Decimal = Decimal("0.0")


class Finding20CvssParameters(NamedTuple):
    bs_factor_1: Decimal
    bs_factor_2: Decimal
    bs_factor_3: Decimal
    impact_factor: Decimal
    exploitability_factor: Decimal


class Finding31Severity(NamedTuple):
    attack_complexity: Decimal = Decimal("0.0")
    attack_vector: Decimal = Decimal("0.0")
    availability_impact: Decimal = Decimal("0.0")
    availability_requirement: Decimal = Decimal("0.0")
    confidentiality_impact: Decimal = Decimal("0.0")
    confidentiality_requirement: Decimal = Decimal("0.0")
    exploitability: Decimal = Decimal("0.0")
    integrity_impact: Decimal = Decimal("0.0")
    integrity_requirement: Decimal = Decimal("0.0")
    modified_attack_complexity: Decimal = Decimal("0.0")
    modified_attack_vector: Decimal = Decimal("0.0")
    modified_availability_impact: Decimal = Decimal("0.0")
    modified_confidentiality_impact: Decimal = Decimal("0.0")
    modified_integrity_impact: Decimal = Decimal("0.0")
    modified_privileges_required: Decimal = Decimal("0.0")
    modified_user_interaction: Decimal = Decimal("0.0")
    modified_severity_scope: Decimal = Decimal("0.0")
    privileges_required: Decimal = Decimal("0.0")
    remediation_level: Decimal = Decimal("0.0")
    report_confidence: Decimal = Decimal("0.0")
    severity_scope: Decimal = Decimal("0.0")
    user_interaction: Decimal = Decimal("0.0")


class Finding31CvssParameters(NamedTuple):
    basescore_factor: Decimal
    exploitability_factor_1: Decimal
    impact_factor_1: Decimal
    impact_factor_2: Decimal
    impact_factor_3: Decimal
    impact_factor_4: Decimal
    impact_factor_5: Decimal
    impact_factor_6: Decimal
    mod_impact_factor_1: Decimal
    mod_impact_factor_2: Decimal
    mod_impact_factor_3: Decimal
    mod_impact_factor_4: Decimal
    mod_impact_factor_5: Decimal
    mod_impact_factor_6: Decimal
    mod_impact_factor_7: Decimal
    mod_impact_factor_8: Decimal


class FindingTreatmentSummary(NamedTuple):
    accepted: int = 0
    accepted_undefined: int = 0
    in_progress: int = 0
    new: int = 0


class FindingUnreliableIndicators(NamedTuple):
    unreliable_closed_vulnerabilities: int = 0
    unreliable_is_verified: bool = True
    unreliable_newest_vulnerability_report_date: str = ""
    unreliable_oldest_open_vulnerability_report_date: str = ""
    unreliable_oldest_vulnerability_report_date: str = ""
    unreliable_open_vulnerabilities: int = 0
    unreliable_status: FindingStatus = FindingStatus.CLOSED
    unreliable_treatment_summary: FindingTreatmentSummary = (
        FindingTreatmentSummary()
    )
    unreliable_where: str = ""


class Finding(NamedTuple):
    hacker_email: str
    group_name: str
    id: str
    state: FindingState
    title: str
    approval: Optional[FindingState] = None
    attack_vector_description: str = ""
    creation: Optional[FindingState] = None
    description: str = ""
    evidences: FindingEvidences = FindingEvidences()
    min_time_to_remediate: Optional[int] = None
    recommendation: str = ""
    requirements: str = ""
    severity: Union[Finding20Severity, Finding31Severity] = Finding31Severity()
    sorts: FindingSorts = FindingSorts.NO
    submission: Optional[FindingState] = None
    threat: str = ""
    unreliable_indicators: FindingUnreliableIndicators = (
        FindingUnreliableIndicators()
    )
    verification: Optional[FindingVerification] = None


class FindingEvidenceToUpdate(NamedTuple):
    description: Optional[str] = None
    modified_date: Optional[str] = None
    url: Optional[str] = None


class FindingMetadataToUpdate(NamedTuple):
    attack_vector_description: Optional[str] = None
    description: Optional[str] = None
    evidences: Optional[FindingEvidences] = None
    recommendation: Optional[str] = None
    severity: Optional[Union[Finding20Severity, Finding31Severity]] = None
    sorts: Optional[FindingSorts] = None
    threat: Optional[str] = None
    title: Optional[str] = None


class FindingUnreliableIndicatorsToUpdate(NamedTuple):
    unreliable_closed_vulnerabilities: Optional[int] = None
    unreliable_is_verified: Optional[bool] = None
    unreliable_newest_vulnerability_report_date: Optional[str] = None
    unreliable_oldest_open_vulnerability_report_date: Optional[str] = None
    unreliable_oldest_vulnerability_report_date: Optional[str] = None
    unreliable_open_vulnerabilities: Optional[int] = None
    unreliable_status: Optional[FindingStatus] = None
    unreliable_treatment_summary: Optional[FindingTreatmentSummary] = None
    unreliable_where: Optional[str] = None
