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
    IntegrityImpact,
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
        auto_approve: bool,
        attack_complexity: AttackComplexity,
        attack_vector: AttackVector,
        availability_impact: AvailabilityImpact,
        confidentiality_impact: ConfidentialityImpact,
        exploitability: float,
        integrity_impact: IntegrityImpact,
        privileges_required: float,
        remediation_level: float,
        report_confidence: float,
        severity_scope: float,
        user_interaction: float,
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
                "exploitability": exploitability,
                "integrityImpact": integrity_impact.value,
                "privilegesRequired": privileges_required,
                "remediationLevel": remediation_level,
                "reportConfidence": report_confidence,
                "severityScope": severity_scope,
                "userInteraction": user_interaction,
            },
            threat=f"{code}.threat",
            title=f"{code}.title",
            type=FindingTypeEnum.SECURITY,
        )


class FindingEnum(Enum):
    F001_JAVA_SQL: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F001_JAVA_SQL",
        cwe="89",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.low,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=0.96,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F001_JPA: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F001_JPA",
        cwe="89",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.high,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=0.96,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F004: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F004",
        cwe="78",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.high,
        confidentiality_impact=ConfidentialityImpact.high,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=0.96,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F008: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F008",
        cwe="79",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.68,
        remediation_level=1.0,
        report_confidence=0.96,
        severity_scope=0.0,
        user_interaction=0.62,
    )
    F009: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F009",
        cwe="798",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F011: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F011",
        cwe="937",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.low,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.62,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F020: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F020",
        cwe="311",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F021: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F021",
        cwe="643",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F022: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F022",
        cwe="319",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.adjacent,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.85,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.62,
    )
    F024_AWS: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F024_AWS",
        cwe="16",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=1.0,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.85,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=1.0,
        user_interaction=0.85,
    )
    F031_AWS: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F031_AWS",
        cwe="250",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.low,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F031_CWE378: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F031_CWE378",
        cwe="378",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.local,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.85,
        remediation_level=1.0,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.62,
    )
    F034: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F034",
        cwe="330",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.62,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F037: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F037",
        cwe="200",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.91,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F042: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F042",
        cwe="614",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.27,
        remediation_level=0.95,
        report_confidence=0.96,
        severity_scope=0.0,
        user_interaction=0.62,
    )
    F043_DAST_CSP: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F043_DAST_CSP",
        cwe="644",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.85,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.62,
    )
    F043_DAST_RP: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F043_DAST_RP",
        cwe="644",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.85,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.62,
    )
    F043_DAST_STS: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F043_DAST_STS",
        cwe="644",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.adjacent,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.85,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.62,
    )
    F043_DAST_XCTO: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F043_DAST_XCTO",
        cwe="644",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.85,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.62,
    )
    F043_DAST_XFO: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F043_DAST_XFO",
        cwe="644",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.85,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.62,
    )
    F052: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F052",
        cwe="310",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.adjacent,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.85,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.62,
    )
    F055_AWS_MISSING_ENCRYPTION: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F055_AWS_MISSING_ENCRYPTION",
        cwe="311",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.local,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.high,
        exploitability=1.0,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.68,
        remediation_level=0.94,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F055_CORS: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F055_CORS",
        cwe="942",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.85,
        remediation_level=1.0,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F059: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F059",
        cwe="532",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.adjacent,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.high,
        exploitability=0.91,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.27,
        remediation_level=1.0,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F060: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F060",
        cwe="396",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.62,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F061: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F061",
        cwe="390",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F063_PATH_TRAVERSAL: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F063_PATH_TRAVERSAL",
        cwe="22",
        attack_complexity=AttackComplexity.high,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.62,
        remediation_level=0.95,
        report_confidence=0.96,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F063_TRUSTBOUND: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F063_TRUSTBOUND",
        cwe="501",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=0.91,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=0.92,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F073: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F073",
        cwe="478",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=0.91,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F085: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F085",
        cwe="922",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.97,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.85,
        remediation_level=0.95,
        report_confidence=1.0,
        severity_scope=0.0,
        user_interaction=0.62,
    )
    F107: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F107",
        cwe="90",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.low,
        exploitability=0.94,
        integrity_impact=IntegrityImpact.none,
        privileges_required=0.62,
        remediation_level=1.0,
        report_confidence=0.96,
        severity_scope=0.0,
        user_interaction=0.85,
    )
    F117: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F117",
        cwe="377",
        attack_complexity=AttackComplexity.low,
        attack_vector=AttackVector.network,
        availability_impact=AvailabilityImpact.none,
        confidentiality_impact=ConfidentialityImpact.none,
        exploitability=0.91,
        integrity_impact=IntegrityImpact.low,
        privileges_required=0.62,
        remediation_level=1,
        report_confidence=1,
        severity_scope=0.0,
        user_interaction=0.85,
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
