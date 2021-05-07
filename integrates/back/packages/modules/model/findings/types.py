# Standard
from decimal import Decimal
from typing import Tuple, NamedTuple, Union, Optional


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
    description: str = ''
    modified_date: str = ''
    url: str = ''


class FindingEvidences(NamedTuple):
    animation: FindingEvidence = FindingEvidence()
    evidence1: FindingEvidence = FindingEvidence()
    evidence2: FindingEvidence = FindingEvidence()
    evidence3: FindingEvidence = FindingEvidence()
    evidence4: FindingEvidence = FindingEvidence()
    evidence5: FindingEvidence = FindingEvidence()
    exploitation: FindingEvidence = FindingEvidence()


class FindingRecords(NamedTuple):
    description: str = ''
    modified_date: str = ''
    url: str = ''


class Finding20Severity(NamedTuple):
    access_complexity: Decimal = Decimal('0.0')
    access_vector: Decimal = Decimal('0.0')
    authentication: Decimal = Decimal('0.0')
    availability_impact: Decimal = Decimal('0.0')
    availability_requirement: Decimal = Decimal('0.0')
    collateral_damage_potential: Decimal = Decimal('0.0')
    confidence_level: Decimal = Decimal('0.0')
    confidentiality_impact: Decimal = Decimal('0.0')
    confidentiality_requirement: Decimal = Decimal('0.0')
    exploitability: Decimal = Decimal('0.0')
    finding_distribution: Decimal = Decimal('0.0')
    integrity_impact: Decimal = Decimal('0.0')
    integrity_requirement: Decimal = Decimal('0.0')
    resolution_level: Decimal = Decimal('0.0')


class Finding31Severity(NamedTuple):
    attack_complexity: Decimal = Decimal('0.0')
    attack_vector: Decimal = Decimal('0.0')
    availability_impact: Decimal = Decimal('0.0')
    availability_requirement: Decimal = Decimal('0.0')
    confidentiality_impact: Decimal = Decimal('0.0')
    confidentiality_requirement: Decimal = Decimal('0.0')
    exploitability: Decimal = Decimal('0.0')
    integrity_impact: Decimal = Decimal('0.0')
    integrity_requirement: Decimal = Decimal('0.0')
    modified_attack_complexity: Decimal = Decimal('0.0')
    modified_attack_vector: Decimal = Decimal('0.0')
    modified_availability_impact: Decimal = Decimal('0.0')
    modified_confidentiality_impact: Decimal = Decimal('0.0')
    modified_integrity_impact: Decimal = Decimal('0.0')
    modified_privileges_required: Decimal = Decimal('0.0')
    modified_user_interaction: Decimal = Decimal('0.0')
    modified_severity_scope: Decimal = Decimal('0.0')
    privileges_required: Decimal = Decimal('0.0')
    remediation_level: Decimal = Decimal('0.0')
    report_confidence: Decimal = Decimal('0.0')
    severity_scope: Decimal = Decimal('0.0')
    user_interaction: Decimal = Decimal('0.0')


class Finding(NamedTuple):
    analyst_email: str
    group_name: str
    id: str
    state: FindingState
    title: str
    actor: str = ''
    affected_systems: str = ''
    attack_vector_desc: str = ''
    bts_url: str = ''
    compromised_attributes: str = ''
    compromised_records: int = 0
    cvss_version: str = '3.1'
    cwe: str = ''
    description: str = ''
    evidences: FindingEvidences = FindingEvidences()
    scenario: str = ''
    severity: Union[Finding20Severity, Finding31Severity] = \
        Finding31Severity()
    sorts: str = 'NO'
    records: FindingRecords = FindingRecords()
    recommendation: str = ''
    requirements: str = ''
    risk: str = ''
    threat: str = ''
    type: str = ''
    verification: Optional[FindingVerification] = None
