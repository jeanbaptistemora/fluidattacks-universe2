# Standard library
from enum import (
    Enum,
)
from typing import (
    Dict,
    NamedTuple,
    Optional,
    Tuple,
)


class LocalesEnum(Enum):
    EN: str = 'EN'
    ES: str = 'ES'


class FindingTypeEnum(Enum):
    HYGIENE: str = 'HYGIENE'
    SECURITY: str = 'SECURITY'


class FindingMetadata(NamedTuple):
    cwe: str
    description: str
    impact: str
    recommendation: str
    requirements: str
    risk: str
    severity: Dict[str, float]
    threat: str
    title: str
    type: FindingTypeEnum


class FindingEnum(Enum):
    F0034: FindingMetadata = FindingMetadata(
        cwe='330',
        description='utils.model.finding.enum.f0034.description',
        impact='utils.model.finding.enum.f0034.impact',
        recommendation='utils.model.finding.enum.f0034.recommendation',
        requirements='utils.model.finding.enum.f0034.requirements',
        risk='utils.model.finding.enum.f0034.risk',
        threat='utils.model.finding.enum.f0034.threat',
        severity={
            'attackComplexity': 0.44,
            'attackVector': 0.85,
            'availabilityImpact': 0.0,
            'availabilityRequirement': 0.5,
            'confidentialityImpact': 0.22,
            'confidentialityRequirement': 0.5,
            'exploitability': 0.94,
            'integrityImpact': 0.0,
            'integrityRequirement': 0.5,
            'modifiedAttackComplexity': 0.44,
            'modifiedAttackVector': 0.85,
            'modifiedAvailabilityImpact': 0.0,
            'modifiedConfidentialityImpact': 0.22,
            'modifiedIntegrityImpact': 0.0,
            'modifiedPrivilegesRequired': 0.62,
            'modifiedUserInteraction': 0.85,
            'modifiedSeverityScope': 0.0,
            'privilegesRequired': 0.62,
            'remediationLevel': 0.95,
            'reportConfidence': 1.0,
            'severityScope': 0.0,
            'userInteraction': 0.85,
        },
        title='utils.model.finding.enum.f0034.title',
        type=FindingTypeEnum.SECURITY,
    )


class FindingEvidenceIDEnum(Enum):
    ANIMATION: str = 'ANIMATION'
    EVIDENCE1: str = 'EVIDENCE1'
    EVIDENCE2: str = 'EVIDENCE2'
    EVIDENCE3: str = 'EVIDENCE3'
    EVIDENCE4: str = 'EVIDENCE4'
    EVIDENCE5: str = 'EVIDENCE5'
    EXPLOIT: str = 'EXPLOIT'
    EXPLOITATION: str = 'EXPLOITATION'
    RECORDS: str = 'RECORDS'


class FindingEvidenceDescriptionIDEnum(Enum):
    EVIDENCE1: str = 'EVIDENCE1'
    EVIDENCE2: str = 'EVIDENCE2'
    EVIDENCE3: str = 'EVIDENCE3'
    EVIDENCE4: str = 'EVIDENCE4'
    EVIDENCE5: str = 'EVIDENCE5'


class FindingReleaseStatusEnum(Enum):
    APPROVED: str = 'APPROVED'
    CREATED: str = 'CREATED'
    REJECTED: str = 'REJECTED'
    SUBMITTED: str = 'SUBMITTED'


class VulnerabilityApprovalStatusEnum(Enum):
    APPROVED: str = 'APPROVED'
    PENDING: str = 'PENDING'


class VulnerabilityStateEnum(Enum):
    OPEN: str = 'open'
    CLOSED: str = 'closed'


class VulnerabilityKindEnum(Enum):
    INPUTS: str = 'inputs'
    LINES: str = 'lines'
    PORTS: str = 'ports'


class VulnerabilitySourceEnum(Enum):
    INTEGRATES: str = 'integrates'
    SKIMS: str = 'skims'


class GrammarMatch(NamedTuple):
    start_char: int
    start_column: int
    start_line: int
    end_char: int
    end_column: int
    end_line: int


class IntegratesVulnerabilityMetadata(NamedTuple):
    approval_status: Optional[VulnerabilityApprovalStatusEnum] = None
    source: Optional[VulnerabilitySourceEnum] = None
    uuid: Optional[str] = None


class SkimsPathConfig(NamedTuple):
    exclude: Tuple[str, ...]
    include: Tuple[str, ...]


class SkimsConfig(NamedTuple):
    group: Optional[str]
    path: Optional[SkimsPathConfig]
    language: LocalesEnum


class SkimsVulnerabilityMetadata(NamedTuple):
    description: str
    snippet: str


class IntegratesVulnerabilitiesLines(NamedTuple):
    line: str
    path: str
    source: VulnerabilitySourceEnum
    state: VulnerabilityStateEnum


class Vulnerability(NamedTuple):
    finding: FindingEnum
    kind: VulnerabilityKindEnum
    state: VulnerabilityStateEnum
    what: str
    where: str

    integrates_metadata: Optional[IntegratesVulnerabilityMetadata] = None
    skims_metadata: Optional[SkimsVulnerabilityMetadata] = None
