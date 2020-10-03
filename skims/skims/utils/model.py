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


class Platform(Enum):
    NPM: str = 'NPM'
    MAVEN: str = 'MAVEN'


class Grammar(Enum):
    CSHARP: str = 'CSharp'
    JAVA9: str = 'Java9'
    SCALA: str = 'Scala'


class LocalesEnum(Enum):
    EN: str = 'EN'
    ES: str = 'ES'


class FindingTypeEnum(Enum):
    HYGIENE: str = 'HYGIENE'
    SECURITY: str = 'SECURITY'


class FindingMetadata(NamedTuple):
    auto_approve: bool
    cwe: str
    description: str
    impact: str
    recommendation: str
    requirements: str
    severity: Dict[str, float]
    threat: str
    title: str
    type: FindingTypeEnum


class FindingEnum(Enum):
    F001_JPA: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='89',
        description='utils.model.finding.enum.F001_JPA.description',
        impact='utils.model.finding.enum.F001_JPA.impact',
        recommendation='utils.model.finding.enum.F001_JPA.recommendation',
        requirements='utils.model.finding.enum.F001_JPA.requirements',
        severity={
            'attackComplexity': 0.77,
            'attackVector': 0.85,
            'availabilityImpact': 0.0,
            'confidentialityImpact': 0.56,
            'exploitability': 0.94,
            'integrityImpact': 0.0,
            'privilegesRequired': 0.62,
            'remediationLevel': 1.0,
            'reportConfidence': 0.96,
            'severityScope': 0.0,
            'userInteraction': 0.85,
        },
        threat='utils.model.finding.enum.F001_JPA.threat',
        title='utils.model.finding.enum.F001_JPA.title',
        type=FindingTypeEnum.SECURITY,
    )
    F009: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='798',
        description='utils.model.finding.enum.f009.description',
        impact='utils.model.finding.enum.f009.impact',
        recommendation='utils.model.finding.enum.f009.recommendation',
        requirements='utils.model.finding.enum.f009.requirements',
        severity={
            'attackComplexity': 0.77,
            'attackVector': 0.85,
            'availabilityImpact': 0.0,
            'confidentialityImpact': 0.22,
            'exploitability': 0.94,
            'integrityImpact': 0.0,
            'privilegesRequired': 0.62,
            'remediationLevel': 1.0,
            'reportConfidence': 1.0,
            'severityScope': 0.0,
            'userInteraction': 0.85,
        },
        threat='utils.model.finding.enum.f009.threat',
        title='utils.model.finding.enum.f009.title',
        type=FindingTypeEnum.SECURITY,
    )
    F011: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='937',
        description='utils.model.finding.enum.f011.description',
        impact='utils.model.finding.enum.f011.impact',
        recommendation='utils.model.finding.enum.f011.recommendation',
        requirements='utils.model.finding.enum.f011.requirements',
        severity={
            'attackComplexity': 0.44,
            'attackVector': 0.85,
            'availabilityImpact': 0.22,
            'confidentialityImpact': 0.22,
            'exploitability': 0.94,
            'integrityImpact': 0.22,
            'privilegesRequired': 0.62,
            'remediationLevel': 0.95,
            'reportConfidence': 1.0,
            'severityScope': 0.0,
            'userInteraction': 0.85,
        },
        threat='utils.model.finding.enum.f011.threat',
        title='utils.model.finding.enum.f011.title',
        type=FindingTypeEnum.SECURITY,
    )
    F022: FindingMetadata = FindingMetadata(
        auto_approve=False,
        cwe='319',
        description='utils.model.finding.enum.F022.description',
        impact='utils.model.finding.enum.F022.impact',
        recommendation='utils.model.finding.enum.F022.recommendation',
        requirements='utils.model.finding.enum.F022.requirements',
        severity={
            'attackComplexity': 0.77,
            'attackVector': 0.62,
            'availabilityImpact': 0.0,
            'confidentialityImpact': 0.22,
            'exploitability': 0.94,
            'integrityImpact': 0.22,
            'privilegesRequired': 0.85,
            'remediationLevel': 0.95,
            'reportConfidence': 1.0,
            'severityScope': 0.0,
            'userInteraction': 0.62,
        },
        threat='utils.model.finding.enum.F022.threat',
        title='utils.model.finding.enum.F022.title',
        type=FindingTypeEnum.SECURITY,
    )
    F031_AWS: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='250',
        description='utils.model.finding.enum.F031_AWS.description',
        impact='utils.model.finding.enum.F031_AWS.impact',
        recommendation='utils.model.finding.enum.F031_AWS.recommendation',
        requirements='utils.model.finding.enum.F031_AWS.requirements',
        severity={
            'attackComplexity': 0.77,
            'attackVector': 0.85,
            'availabilityImpact': 0.22,
            'confidentialityImpact': 0.22,
            'exploitability': 0.94,
            'integrityImpact': 0.22,
            'privilegesRequired': 0.62,
            'remediationLevel': 1.0,
            'reportConfidence': 1.0,
            'severityScope': 0.0,
            'userInteraction': 0.85,
        },
        threat='utils.model.finding.enum.F031_AWS.threat',
        title='utils.model.finding.enum.F031_AWS.title',
        type=FindingTypeEnum.SECURITY,
    )
    F031_CWE378: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='378',
        description='utils.model.finding.enum.F031_CWE378.description',
        impact='utils.model.finding.enum.F031_CWE378.impact',
        recommendation='utils.model.finding.enum.F031_CWE378.recommendation',
        requirements='utils.model.finding.enum.F031_CWE378.requirements',
        severity={
            'attackComplexity': 0.77,
            'attackVector': 0.55,
            'availabilityImpact': 0.0,
            'confidentialityImpact': 0.22,
            'exploitability': 0.94,
            'integrityImpact': 0.22,
            'privilegesRequired': 0.85,
            'remediationLevel': 1.0,
            'reportConfidence': 1.0,
            'severityScope': 0.0,
            'userInteraction': 0.62,
        },
        threat='utils.model.finding.enum.F031_CWE378.threat',
        title='utils.model.finding.enum.F031_CWE378.title',
        type=FindingTypeEnum.SECURITY,
    )
    F034: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='330',
        description='utils.model.finding.enum.f034.description',
        impact='utils.model.finding.enum.f034.impact',
        recommendation='utils.model.finding.enum.f034.recommendation',
        requirements='utils.model.finding.enum.f034.requirements',
        severity={
            'attackComplexity': 0.44,
            'attackVector': 0.85,
            'availabilityImpact': 0.0,
            'confidentialityImpact': 0.22,
            'exploitability': 0.94,
            'integrityImpact': 0.0,
            'privilegesRequired': 0.62,
            'remediationLevel': 0.95,
            'reportConfidence': 1.0,
            'severityScope': 0.0,
            'userInteraction': 0.85,
        },
        threat='utils.model.finding.enum.f034.threat',
        title='utils.model.finding.enum.f034.title',
        type=FindingTypeEnum.SECURITY,
    )
    F052: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='310',
        description='utils.model.finding.enum.F052.description',
        impact='utils.model.finding.enum.F052.impact',
        recommendation='utils.model.finding.enum.F052.recommendation',
        requirements='utils.model.finding.enum.F052.requirements',
        severity={
            'attackComplexity': 0.44,
            'attackVector': 0.62,
            'availabilityImpact': 0.0,
            'confidentialityImpact': 0.22,
            'exploitability': 0.94,
            'integrityImpact': 0.22,
            'privilegesRequired': 0.85,
            'remediationLevel': 0.95,
            'reportConfidence': 1.0,
            'severityScope': 0.0,
            'userInteraction': 0.62,
        },
        threat='utils.model.finding.enum.F052.threat',
        title='utils.model.finding.enum.F052.title',
        type=FindingTypeEnum.SECURITY,
    )
    F060: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='396',
        description='utils.model.finding.enum.f060.description',
        impact='utils.model.finding.enum.f060.impact',
        recommendation='utils.model.finding.enum.f060.recommendation',
        requirements='utils.model.finding.enum.f060.requirements',
        severity={
            'attackComplexity': 0.77,
            'attackVector': 0.85,
            'availabilityImpact': 0.0,
            'confidentialityImpact': 0.0,
            'exploitability': 0.94,
            'integrityImpact': 0.22,
            'privilegesRequired': 0.62,
            'remediationLevel': 0.95,
            'reportConfidence': 1.0,
            'severityScope': 0.0,
            'userInteraction': 0.85,
        },
        threat='utils.model.finding.enum.f060.threat',
        title='utils.model.finding.enum.f060.title',
        type=FindingTypeEnum.HYGIENE,
    )
    F061: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='390',
        description='utils.model.finding.enum.f061.description',
        impact='utils.model.finding.enum.f061.impact',
        recommendation='utils.model.finding.enum.f061.recommendation',
        requirements='utils.model.finding.enum.f061.requirements',
        severity={
            'attackComplexity': 0.77,
            'attackVector': 0.85,
            'availabilityImpact': 0.0,
            'confidentialityImpact': 0.0,
            'exploitability': 0.94,
            'integrityImpact': 0.22,
            'privilegesRequired': 0.62,
            'remediationLevel': 1.0,
            'reportConfidence': 1.0,
            'severityScope': 0.0,
            'userInteraction': 0.85,
        },
        threat='utils.model.finding.enum.f061.threat',
        title='utils.model.finding.enum.f061.title',
        type=FindingTypeEnum.SECURITY,
    )
    F073: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='478',
        description='utils.model.finding.enum.F073.description',
        impact='utils.model.finding.enum.F073.impact',
        recommendation='utils.model.finding.enum.F073.recommendation',
        requirements='utils.model.finding.enum.F073.requirements',
        severity={
            "attackComplexity": 0.44,
            "attackVector": 0.85,
            "availabilityImpact": 0.0,
            "confidentialityImpact": 0.0,
            "exploitability": 0.91,
            "integrityImpact": 0.22,
            "privilegesRequired": 0.62,
            "remediationLevel": 1.0,
            "reportConfidence": 1.0,
            "severityScope": 0.0,
            "userInteraction": 0.85
        },
        threat='utils.model.finding.enum.F073.threat',
        title='utils.model.finding.enum.F073.title',
        type=FindingTypeEnum.HYGIENE,
    )
    F085: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='922',
        description='utils.model.finding.enum.f085.description',
        impact='utils.model.finding.enum.f085.impact',
        recommendation='utils.model.finding.enum.f085.recommendation',
        requirements='utils.model.finding.enum.f085.requirements',
        severity={
            'attackComplexity': 0.44,
            'attackVector': 0.85,
            'availabilityImpact': 0.0,
            'confidentialityImpact': 0.22,
            'exploitability': 0.97,
            'integrityImpact': 0.0,
            'privilegesRequired': 0.85,
            'remediationLevel': 0.95,
            'reportConfidence': 1.0,
            'severityScope': 0.0,
            'userInteraction': 0.62,
        },
        threat='utils.model.finding.enum.f085.threat',
        title='utils.model.finding.enum.f085.title',
        type=FindingTypeEnum.SECURITY,
    )
    F117: FindingMetadata = FindingMetadata(
        auto_approve=True,
        cwe='377',
        description='utils.model.finding.enum.f117.description',
        impact='utils.model.finding.enum.f117.impact',
        recommendation='utils.model.finding.enum.f117.recommendation',
        requirements='utils.model.finding.enum.f117.requirements',
        severity={
            'attackComplexity': 0.44,
            'attackVector': 0.85,
            'availabilityImpact': 0.0,
            'confidentialityImpact': 0.0,
            'exploitability': 0.91,
            'integrityImpact': 0.22,
            'privilegesRequired': 0.62,
            'remediationLevel': 1,
            'reportConfidence': 1,
            'severityScope': 0.0,
            'userInteraction': 0.85,
        },
        title='utils.model.finding.enum.f117.title',
        threat='utils.model.finding.enum.f117.threat',
        type=FindingTypeEnum.HYGIENE,
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
    start_column: int
    start_line: int


class IntegratesVulnerabilityMetadata(NamedTuple):
    approval_status: Optional[VulnerabilityApprovalStatusEnum] = None
    source: Optional[VulnerabilitySourceEnum] = None
    uuid: Optional[str] = None


class NVDVulnerability(NamedTuple):
    code: str
    cvss: str
    description: str
    product: str
    url: str
    version: str


class SkimsPathConfig(NamedTuple):
    exclude: Tuple[str, ...]
    include: Tuple[str, ...]


class SkimsConfig(NamedTuple):
    chdir: Optional[str]
    console_snippets: bool
    group: Optional[str]
    path: Optional[SkimsPathConfig]
    timeout: Optional[float]
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


def get_vulnerability_hash(vulnerability: Vulnerability) -> int:
    """Compute the hash of a Vulnerability according to Integrates rules.

    :param vulnerability: Vulnerability object to hash
    :type vulnerability: Vulnerability
    :return: A unique identifier under this runtime, not guaranteed to
        be the same across executions
    :rtype: int
    """
    return hash((
        vulnerability.finding,
        vulnerability.kind,
        vulnerability.what,
        vulnerability.where,
    ))


def _fill_finding_enum() -> None:
    for finding in FindingEnum:
        for modified, base in [
            ('modifiedAttackComplexity', 'attackComplexity'),
            ('modifiedAttackVector', 'attackVector'),
            ('modifiedAvailabilityImpact', 'availabilityImpact'),
            ('modifiedConfidentialityImpact', 'confidentialityImpact'),
            ('modifiedIntegrityImpact', 'integrityImpact'),
            ('modifiedPrivilegesRequired', 'privilegesRequired'),
            ('modifiedUserInteraction', 'userInteraction'),
            ('modifiedSeverityScope', 'severityScope'),
        ]:
            finding.value.severity[modified] = finding.value.severity[base]

        for environmental in [
            'availabilityRequirement',
            'confidentialityRequirement',
            'integrityRequirement',
        ]:
            finding.value.severity[environmental] = 0.0


_fill_finding_enum()
