# Standard library
from __future__ import (
    annotations,
)
from enum import (
    Enum,
)
from typing import (
    Dict,
    NamedTuple,
    Optional,
    Set,
    Tuple,
)

# Local libraries
from model.cvss3_model import (
    AttackComplexity,
    AttackVector,
    AvailabilityImpact,
    ConfidentialityImpact,
    Exploitability,
    IntegrityImpact,
    PrivilegesRequired,
    RemediationLevel,
    ReportConfidence,
    SeverityScope,
    UserInteraction,
)


class Platform(Enum):
    NPM: str = "NPM"
    MAVEN: str = "MAVEN"


class Grammar(Enum):
    CSHARP: str = "CSharp"
    JAVA9: str = "Java9"
    SCALA: str = "Scala"


class LocalesEnum(Enum):
    EN: str = "EN"
    ES: str = "ES"


class FindingTypeEnum(Enum):
    HYGIENE: str = "HYGIENE"
    SECURITY: str = "SECURITY"


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

    @classmethod
    def new(
        cls,
        *,
        code: str,
        cwe: str,
        auto_approve: bool = True,
        attack_complexity: AttackComplexity,
        attack_vector: AttackVector,
        availability_impact: AvailabilityImpact,
        confidentiality_impact: ConfidentialityImpact,
        exploitability: Exploitability,
        integrity_impact: IntegrityImpact,
        privileges_required: PrivilegesRequired,
        remediation_level: RemediationLevel,
        report_confidence: ReportConfidence,
        severity_scope: SeverityScope,
        user_interaction: UserInteraction,
    ) -> FindingMetadata:
        return FindingMetadata(
            auto_approve=auto_approve,
            cwe=cwe,
            description=f"{code}.description",
            impact=f"{code}.impact",
            recommendation=f"{code}.recommendation",
            requirements=f"{code}.requirements",
            severity={
                "attackComplexity": attack_complexity.value,
                "attackVector": attack_vector.value,
                "availabilityImpact": availability_impact.value,
                "confidentialityImpact": confidentiality_impact.value,
                "exploitability": exploitability.value,
                "integrityImpact": integrity_impact.value,
                "privilegesRequired": privileges_required.value,
                "remediationLevel": remediation_level.value,
                "reportConfidence": report_confidence.value,
                "severityScope": severity_scope.value,
                "userInteraction": user_interaction.value,
            },
            threat=f"{code}.threat",
            title=f"{code}.title",
            type=FindingTypeEnum.SECURITY,
        )


class FindingEnum(Enum):
    F001_JAVA_SQL: FindingMetadata = FindingMetadata.new(
        code="F001_JAVA_SQL",
        cwe="89",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.low,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.reasonable,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F001_JPA: FindingMetadata = FindingMetadata.new(
        code="F001_JPA",
        cwe="89",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.high,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.reasonable,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F004: FindingMetadata = FindingMetadata.new(
        code="F004",
        cwe="78",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.high,
        confidentiality_impact=ConfidentialityImpact.high,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.reasonable,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F008: FindingMetadata = FindingMetadata.new(
        code="F008",
        cwe="79",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.reasonable,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.required,
    )
    F009: FindingMetadata = FindingMetadata.new(
        code="F009",
        cwe="798",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F011: FindingMetadata = FindingMetadata.new(
        code="F011",
        cwe="937",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.low,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F015_DAST_BASIC: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F015_DAST_BASIC",
        cwe="287",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.adjacent,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.high,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.none,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.changed,
        user_interaction=UserInteraction.required,
    )
    F020: FindingMetadata = FindingMetadata.new(
        code="F020",
        cwe="311",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F021: FindingMetadata = FindingMetadata.new(
        code="F021",
        cwe="643",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F022: FindingMetadata = FindingMetadata.new(
        code="F022",
        cwe="319",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.adjacent,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.high,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.required,
    )
    F024_AWS: FindingMetadata = FindingMetadata.new(
        code="F024_AWS",
        cwe="16",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=Exploitability.high,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.high,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.changed,
        user_interaction=UserInteraction.none,
    )
    F031_AWS: FindingMetadata = FindingMetadata.new(
        code="F031_AWS",
        cwe="250",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.low,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F031_CWE378: FindingMetadata = FindingMetadata.new(
        code="F031_CWE378",
        cwe="378",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.local,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.high,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.required,
    )
    F034: FindingMetadata = FindingMetadata.new(
        code="F034",
        cwe="330",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F037: FindingMetadata = FindingMetadata.new(
        code="F037",
        cwe="200",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.unproven,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F042: FindingMetadata = FindingMetadata.new(
        code="F042",
        cwe="614",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.none,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.reasonable,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.required,
    )
    F043_DAST_CSP: FindingMetadata = FindingMetadata.new(
        code="F043_DAST_CSP",
        cwe="644",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.high,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.required,
    )
    F043_DAST_RP: FindingMetadata = FindingMetadata.new(
        code="F043_DAST_RP",
        cwe="644",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.high,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.required,
    )
    F043_DAST_STS: FindingMetadata = FindingMetadata.new(
        code="F043_DAST_STS",
        cwe="644",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.adjacent,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.high,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.required,
    )
    F043_DAST_XCTO: FindingMetadata = FindingMetadata.new(
        code="F043_DAST_XCTO",
        cwe="644",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.high,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.required,
    )
    F052: FindingMetadata = FindingMetadata.new(
        code="F052",
        cwe="310",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.adjacent,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.high,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.required,
    )
    F055_AWS_MISSING_ENCRYPTION: FindingMetadata = FindingMetadata.new(
        code="F055_AWS_MISSING_ENCRYPTION",
        cwe="311",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.local,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.high,
        exploitability=Exploitability.high,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F055_CORS: FindingMetadata = FindingMetadata.new(
        code="F055_CORS",
        cwe="942",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.high,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F059: FindingMetadata = FindingMetadata.new(
        code="F059",
        cwe="532",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.adjacent,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.high,
        exploitability=Exploitability.unproven,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.none,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F060: FindingMetadata = FindingMetadata.new(
        code="F060",
        cwe="396",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F061: FindingMetadata = FindingMetadata.new(
        code="F061",
        cwe="390",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F063_PATH_TRAVERSAL: FindingMetadata = FindingMetadata.new(
        code="F063_PATH_TRAVERSAL",
        cwe="22",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.reasonable,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F063_TRUSTBOUND: FindingMetadata = FindingMetadata.new(
        code="F063_TRUSTBOUND",
        cwe="501",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=Exploitability.unproven,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.unknown,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F073: FindingMetadata = FindingMetadata.new(
        code="F073",
        cwe="478",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=Exploitability.unproven,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F085: FindingMetadata = FindingMetadata.new(
        code="F085",
        cwe="922",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.functional,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.high,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.required,
    )
    F086: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F086",
        cwe="353",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=Exploitability.unproven,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.none,
        remediation_level=RemediationLevel.official_fix,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.required,
    )
    F107: FindingMetadata = FindingMetadata.new(
        code="F107",
        cwe="90",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=Exploitability.poc,
        integrity_impact=IntegrityImpact.none,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.reasonable,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )
    F117: FindingMetadata = FindingMetadata.new(
        code="F117",
        cwe="377",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=Exploitability.unproven,
        integrity_impact=IntegrityImpact.low,
        privileges_required=PrivilegesRequired.low,
        remediation_level=RemediationLevel.unavailable,
        report_confidence=ReportConfidence.confirmed,
        severity_scope=SeverityScope.unchanged,
        user_interaction=UserInteraction.none,
    )


FINDING_ENUM_FROM_STR: Dict[str, FindingEnum] = {
    __finding.name: __finding for __finding in FindingEnum
}


class FindingEvidenceIDEnum(Enum):
    ANIMATION: str = "ANIMATION"
    EVIDENCE1: str = "EVIDENCE1"
    EVIDENCE2: str = "EVIDENCE2"
    EVIDENCE3: str = "EVIDENCE3"
    EVIDENCE4: str = "EVIDENCE4"
    EVIDENCE5: str = "EVIDENCE5"
    EXPLOIT: str = "EXPLOIT"
    EXPLOITATION: str = "EXPLOITATION"
    RECORDS: str = "RECORDS"


class FindingEvidenceDescriptionIDEnum(Enum):
    EVIDENCE1: str = "EVIDENCE1"
    EVIDENCE2: str = "EVIDENCE2"
    EVIDENCE3: str = "EVIDENCE3"
    EVIDENCE4: str = "EVIDENCE4"
    EVIDENCE5: str = "EVIDENCE5"


class FindingReleaseStatusEnum(Enum):
    APPROVED: str = "APPROVED"
    CREATED: str = "CREATED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"


class VulnerabilityApprovalStatusEnum(Enum):
    APPROVED: str = "APPROVED"
    PENDING: str = "PENDING"


class VulnerabilityStateEnum(Enum):
    OPEN: str = "open"
    CLOSED: str = "closed"


class VulnerabilityKindEnum(Enum):
    INPUTS: str = "inputs"
    LINES: str = "lines"
    PORTS: str = "ports"


class VulnerabilitySourceEnum(Enum):
    INTEGRATES: str = "integrates"
    SKIMS: str = "skims"


class GrammarMatch(NamedTuple):
    start_column: int
    start_line: int


class IntegratesVulnerabilityMetadata(NamedTuple):
    approval_status: Optional[VulnerabilityApprovalStatusEnum] = None
    namespace: Optional[str] = None
    source: Optional[VulnerabilitySourceEnum] = None
    uuid: Optional[str] = None


class NVDVulnerability(NamedTuple):
    code: str
    cvss: str
    description: str
    product: str
    url: str
    version: str


class SkimsHttpConfig(NamedTuple):
    include: Tuple[str, ...]


class SkimsPathConfig(NamedTuple):
    exclude: Tuple[str, ...]
    include: Tuple[str, ...]
    lib_path: bool
    lib_root: bool


class SkimsConfig(NamedTuple):
    checks: Set[FindingEnum]
    group: Optional[str]
    http: SkimsHttpConfig
    language: LocalesEnum
    namespace: str
    output: Optional[str]
    path: SkimsPathConfig
    start_dir: str
    timeout: Optional[float]
    working_dir: str


class SkimsVulnerabilityMetadata(NamedTuple):
    cwe: Tuple[str, ...]
    description: str
    snippet: str


class IntegratesVulnerabilitiesLines(NamedTuple):
    commit_hash: str
    line: str
    path: str
    repo_nickname: str
    state: VulnerabilityStateEnum


class IntegratesVulnerabilitiesInputs(NamedTuple):
    field: str
    state: VulnerabilityStateEnum
    stream: str
    url: str


class Vulnerability(NamedTuple):
    finding: FindingEnum
    kind: VulnerabilityKindEnum
    state: VulnerabilityStateEnum
    what: str
    where: str
    stream: str = "skims"

    integrates_metadata: Optional[IntegratesVulnerabilityMetadata] = None
    skims_metadata: Optional[SkimsVulnerabilityMetadata] = None

    @property
    def digest(self) -> int:
        """Hash a Vulnerability according to Integrates rules."""
        return hash(
            (
                self.finding,
                self.kind,
                self.what,
                self.where,
            )
        )


Vulnerabilities = Tuple[Vulnerability, ...]


def _fill_finding_enum() -> None:
    for finding in FindingEnum:
        for modified, base in [
            ("modifiedAttackComplexity", "attackComplexity"),
            ("modifiedAttackVector", "attackVector"),
            ("modifiedAvailabilityImpact", "availabilityImpact"),
            ("modifiedConfidentialityImpact", "confidentialityImpact"),
            ("modifiedIntegrityImpact", "integrityImpact"),
            ("modifiedPrivilegesRequired", "privilegesRequired"),
            ("modifiedUserInteraction", "userInteraction"),
            ("modifiedSeverityScope", "severityScope"),
        ]:
            finding.value.severity[modified] = finding.value.severity[base]

        for environmental in [
            "availabilityRequirement",
            "confidentialityRequirement",
            "integrityRequirement",
        ]:
            finding.value.severity[environmental] = 0.0


# Import hooks
_fill_finding_enum()
