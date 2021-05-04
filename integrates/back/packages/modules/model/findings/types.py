# Standard
from typing import Tuple, NamedTuple, Union


class FindingState(NamedTuple):
    modified_by: str
    modified_date: str
    source: str
    status: str


class FindingVerification(NamedTuple):
    comment_id: str
    modified_by: str
    modified_date: str
    status: str
    vuln_uuids: Tuple[str, ...]


class FindingEvidence(NamedTuple):
    description: str
    modified_date: str
    url: str


class FindingEvidences(NamedTuple):
    animation: FindingEvidence
    evidence1: FindingEvidence
    evidence2: FindingEvidence
    evidence3: FindingEvidence
    evidence4: FindingEvidence
    evidence5: FindingEvidence
    exploitation: FindingEvidence


class FindingRecords(NamedTuple):
    description: str
    modified_date: str
    url: str


class Finding20Severity(NamedTuple):
    access_complexity: float
    access_vector: float
    authentication: float
    availability_impact: float
    availability_requirement: float
    collateral_damage_potential: float
    confidence_level: float
    confidentiality_impact: float
    confidentiality_requirement: float
    exploitability: float
    finding_distribution: float
    integrity_impact: float
    integrity_requirement: float
    resolution_level: float


class Finding31Severity(NamedTuple):
    attack_complexity: float
    attack_vector: float
    availability_impact: float
    availability_requirement: float
    confidentiality_impact: float
    confidentiality_requirement: float
    exploitability: float
    integrity_impact: float
    integrity_requirement: float
    modified_attack_complexity: float
    modified_attack_vector: float
    modified_availability_impact: float
    modified_confidentiality_impact: float
    modified_integrity_impact: float
    modified_privileges_required: float
    modified_user_interaction: float
    modified_severity_scope: float
    privileges_required: float
    remediation_level: float
    report_confidence: float
    severity_scope: float
    user_interaction: float


class Finding(NamedTuple):
    actor: str
    affected_systems: str
    analyst_email: str
    attack_vector_desc: str
    bts_url: str
    compromised_attributes: str
    compromised_records: int
    cvss_version: float
    cwe_url: str
    description: str
    evidences: FindingEvidences
    group_name: str
    id: str
    scenario: str
    severity: Union[Finding20Severity, Finding31Severity]
    sorts: str
    state: FindingState
    records: FindingRecords
    risk: str
    recommendation: str
    requirements: str
    title: str
    threat: str
    type: str
    verification: FindingVerification
