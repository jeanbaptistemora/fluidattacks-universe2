from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from typing import (
    Optional,
)


@dataclass(frozen=True)
class MetadataTableRow:
    # pylint: disable=invalid-name
    id: str
    cvss_version: Optional[str]
    group_name: str
    hacker_email: str
    requirements: str
    sorts: str
    title: str


@dataclass(frozen=True)
class StateTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_date: datetime
    justification: str
    source: str
    status: str


@dataclass(frozen=True)
class SeverityCvss20TableRow:
    # pylint: disable=invalid-name,too-many-instance-attributes
    id: str
    access_complexity: Decimal
    access_vector: Decimal
    authentication: Decimal
    availability_impact: Decimal
    availability_requirement: Decimal
    collateral_damage_potential: Decimal
    confidence_level: Decimal
    confidentiality_impact: Decimal
    confidentiality_requirement: Decimal
    exploitability: Decimal
    finding_distribution: Decimal
    integrity_impact: Decimal
    integrity_requirement: Decimal
    resolution_level: Decimal


@dataclass(frozen=True)
class SeverityCvss31TableRow:
    # pylint: disable=invalid-name,too-many-instance-attributes
    id: str
    attack_complexity: Decimal
    attack_vector: Decimal
    availability_impact: Decimal
    availability_requirement: Decimal
    confidentiality_impact: Decimal
    confidentiality_requirement: Decimal
    exploitability: Decimal
    integrity_impact: Decimal
    integrity_requirement: Decimal
    modified_attack_complexity: Decimal
    modified_attack_vector: Decimal
    modified_availability_impact: Decimal
    modified_confidentiality_impact: Decimal
    modified_integrity_impact: Decimal
    modified_privileges_required: Decimal
    modified_user_interaction: Decimal
    modified_severity_scope: Decimal
    privileges_required: Decimal
    remediation_level: Decimal
    report_confidence: Decimal
    severity_scope: Decimal
    user_interaction: Decimal


@dataclass(frozen=True)
class VerificationTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_date: datetime
    status: str


@dataclass(frozen=True)
class VerificationVulnIdsTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_date: datetime
    vulnerability_id: str
