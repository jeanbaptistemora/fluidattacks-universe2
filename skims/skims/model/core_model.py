# pylint: disable=too-many-lines
# pylint: disable=invalid-name
from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
from enum import (
    Enum,
)
from model import (
    cvss3_model,
    time_model,
)
from typing import (
    Dict,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
)


class Platform(Enum):
    NPM: str = "NPM"
    MAVEN: str = "MAVEN"
    NUGET: str = "NUGET"


class Grammar(Enum):
    JAVA9: str = "Java9"
    SCALA: str = "Scala"


class LocalesEnum(Enum):
    EN: str = "EN"
    ES: str = "ES"


class AvailabilityEnum(Enum):
    ALWAYS = "ALWAYS"
    WORKING_HOURS = "WORKING_HOURS"
    NEVER = "NEVER"


class ExecutionQueueConfig(NamedTuple):
    availability: AvailabilityEnum
    name: str


class ExecutionQueue(Enum):
    apk = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="apk"
    )
    aws = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="aws"
    )
    control = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="control"
    )
    cookie = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="cookie"
    )
    crypto = ExecutionQueueConfig(
        availability=AvailabilityEnum.WORKING_HOURS, name="crypto"
    )
    f014 = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="f014"
    )
    f117 = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="f117"
    )
    http = ExecutionQueueConfig(
        availability=AvailabilityEnum.WORKING_HOURS, name="http"
    )
    injection = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="injection"
    )
    leak = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="leak"
    )
    none = ExecutionQueueConfig(
        availability=AvailabilityEnum.NEVER, name="none"
    )
    sca = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="sca"
    )
    sql = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="sql"
    )
    ssl = ExecutionQueueConfig(
        availability=AvailabilityEnum.WORKING_HOURS, name="ssl"
    )
    xss = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="xss"
    )


if len(ExecutionQueue) > 20:
    # We can have at most 20 items in this Enum
    # Each item in this Enum represents 2 queues:
    #   Soon (urgent): used for re-attacks
    #   Later (non-urgent): is used for periodic executions
    # Batch has a limit of 50 queues, 10 for other products
    # https://docs.aws.amazon.com/batch/latest/userguide/service_limits.html
    raise AssertionError("We can't allocate so many queues")


class FindingMetadata(NamedTuple):
    auto_approve: bool
    cwe: int
    description: str
    execution_queue: ExecutionQueue
    impact: str
    recommendation: str
    requirements: List[int]
    score: cvss3_model.Score
    threat: str
    title: str

    @classmethod
    def new(
        cls,
        *,
        code: str,
        cwe: int,
        execution_queue: ExecutionQueue,
        auto_approve: bool,
        requirements: List[int],
        score: cvss3_model.Score,
    ) -> FindingMetadata:
        return FindingMetadata(
            auto_approve=auto_approve,
            cwe=cwe,
            description=f"{code}.description",
            execution_queue=execution_queue,
            impact=f"{code}.impact",
            recommendation=f"{code}.recommendation",
            requirements=requirements,
            score=score,
            threat=f"{code}.threat",
            title=f"criteria.vulns.{code[1:]}.title",
        )


class FindingEnum(Enum):
    F001: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F001",
        cwe=89,
        execution_queue=ExecutionQueue.sql,
        requirements=[169],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F004: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F004",
        cwe=78,
        execution_queue=ExecutionQueue.injection,
        requirements=[173, 265],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.high,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.high,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F008: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F008",
        cwe=79,
        execution_queue=ExecutionQueue.xss,
        requirements=[173],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F009: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F009",
        cwe=798,
        execution_queue=ExecutionQueue.leak,
        requirements=[156],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F011: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F011",
        cwe=937,
        execution_queue=ExecutionQueue.sca,
        requirements=[262],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.low,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F012: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F012",
        cwe=89,
        execution_queue=ExecutionQueue.sql,
        requirements=[169],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.high,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F015: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F015",
        cwe=287,
        execution_queue=ExecutionQueue.http,
        requirements=[228, 319],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.high,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.changed,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F016: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F016",
        cwe=326,
        execution_queue=ExecutionQueue.ssl,
        requirements=[148, 149, 150, 181, 336],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F017: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F017",
        cwe=319,
        execution_queue=ExecutionQueue.http,
        requirements=[32, 181],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.high,
            exploitability=cvss3_model.Exploitability.high,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.changed,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F021: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F021",
        cwe=643,
        execution_queue=ExecutionQueue.injection,
        requirements=[173],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F022: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F022",
        cwe=319,
        execution_queue=ExecutionQueue.f014,
        requirements=[181],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F023: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F023",
        cwe=601,
        execution_queue=ExecutionQueue.http,
        requirements=[173, 324],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F024: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F024",
        cwe=16,
        execution_queue=ExecutionQueue.aws,
        requirements=[255, 266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.high,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.changed,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F031: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F031",
        cwe=250,
        execution_queue=ExecutionQueue.aws,
        requirements=[186],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.low,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F034: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F034",
        cwe=330,
        execution_queue=ExecutionQueue.crypto,
        requirements=[223, 224],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F035: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F035",
        cwe=521,
        execution_queue=ExecutionQueue.f014,
        requirements=[130, 132, 133, 139, 332],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F036: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F036",
        cwe=319,
        execution_queue=ExecutionQueue.http,
        requirements=[26],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.local,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F042: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F042",
        cwe=614,
        execution_queue=ExecutionQueue.cookie,
        requirements=[29],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F043: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F043",
        cwe=644,
        execution_queue=ExecutionQueue.http,
        requirements=[62],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F046: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F046",
        cwe=1269,
        execution_queue=ExecutionQueue.apk,
        requirements=[159],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F048: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F048",
        cwe=250,
        execution_queue=ExecutionQueue.apk,
        requirements=[326],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.local,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F052: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F052",
        cwe=310,
        execution_queue=ExecutionQueue.crypto,
        requirements=[158, 149, 150, 181, 336],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F055: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F055",
        cwe=530,
        execution_queue=ExecutionQueue.apk,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.local,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F058: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F058",
        cwe=489,
        execution_queue=ExecutionQueue.apk,
        requirements=[77, 78],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.unproven,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F060: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F060",
        cwe=396,
        execution_queue=ExecutionQueue.none,
        requirements=[359],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F061: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F061",
        cwe=390,
        execution_queue=ExecutionQueue.none,
        requirements=[75],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F063: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F063",
        cwe=22,
        execution_queue=ExecutionQueue.injection,
        requirements=[173],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F064: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F064",
        cwe=778,
        execution_queue=ExecutionQueue.http,
        requirements=[75],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.high,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F070: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F070",
        cwe=266,
        execution_queue=ExecutionQueue.aws,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F071: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F071",
        cwe=644,
        execution_queue=ExecutionQueue.http,
        requirements=[62],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F073: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F073",
        cwe=478,
        execution_queue=ExecutionQueue.aws,
        requirements=[161],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F075: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F075",
        cwe=284,
        execution_queue=ExecutionQueue.apk,
        requirements=[176],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.local,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.unproven,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F079: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F079",
        cwe=829,
        execution_queue=ExecutionQueue.f117,
        requirements=[302],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.unproven,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F080: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F080",
        cwe=311,
        execution_queue=ExecutionQueue.aws,
        requirements=[185],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.local,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.high,
            exploitability=cvss3_model.Exploitability.high,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F085: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F085",
        cwe=922,
        execution_queue=ExecutionQueue.leak,
        requirements=[329],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.functional,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F086: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F086",
        cwe=353,
        execution_queue=ExecutionQueue.http,
        requirements=[178, 262, 330],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F089: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F089",
        cwe=501,
        execution_queue=ExecutionQueue.control,
        requirements=[173],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.unproven,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F091: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F091",
        cwe=117,
        execution_queue=ExecutionQueue.f014,
        requirements=[80, 173],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F092: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F092",
        cwe=757,
        execution_queue=ExecutionQueue.ssl,
        requirements=[148, 149, 150, 181, 336],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.functional,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F094: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F094",
        cwe=757,
        execution_queue=ExecutionQueue.ssl,
        requirements=[148, 149, 150, 181, 336],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F096: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F096",
        cwe=502,
        execution_queue=ExecutionQueue.f014,
        requirements=[173, 321],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F099: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F099",
        cwe=311,
        execution_queue=ExecutionQueue.aws,
        requirements=[134, 135, 185, 227, 229, 264, 300],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.high,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.high,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F100: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F100",
        cwe=918,
        execution_queue=ExecutionQueue.f014,
        requirements=[173, 324],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F103: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F103",
        cwe=325,
        execution_queue=ExecutionQueue.apk,
        requirements=[178],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F107: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F107",
        cwe=90,
        execution_queue=ExecutionQueue.injection,
        requirements=[173],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F109: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F109",
        cwe=681,
        execution_queue=ExecutionQueue.aws,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.low,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F112: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F112",
        cwe=89,
        execution_queue=ExecutionQueue.sql,
        requirements=[169],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.low,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F117: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F117",
        cwe=377,
        execution_queue=ExecutionQueue.f117,
        requirements=[323],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.unproven,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F127: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F127",
        cwe=843,
        execution_queue=ExecutionQueue.control,
        requirements=[342],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.unproven,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F128: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F128",
        cwe=1004,
        execution_queue=ExecutionQueue.http,
        requirements=[29],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.high,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F129: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F129",
        cwe=1275,
        execution_queue=ExecutionQueue.http,
        requirements=[29],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F130: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F130",
        cwe=614,
        execution_queue=ExecutionQueue.http,
        requirements=[29],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.high,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F131: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F131",
        cwe=644,
        execution_queue=ExecutionQueue.http,
        requirements=[62, 181],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F132: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F132",
        cwe=644,
        execution_queue=ExecutionQueue.http,
        requirements=[62],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F133: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F133",
        cwe=310,
        execution_queue=ExecutionQueue.ssl,
        requirements=[148, 149, 150, 181],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F134: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F134",
        cwe=16,
        execution_queue=ExecutionQueue.http,
        requirements=[62, 266, 349],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F160: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F160",
        cwe=378,
        execution_queue=ExecutionQueue.control,
        requirements=[95, 96, 186],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.local,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F177: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F177",
        cwe=16,
        execution_queue=ExecutionQueue.aws,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F200: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F200",
        cwe=778,
        execution_queue=ExecutionQueue.aws,
        requirements=[75, 320],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F207: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F207",
        cwe=295,
        execution_queue=ExecutionQueue.apk,
        requirements=[93],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.unproven,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F211: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F211",
        cwe=405,
        execution_queue=ExecutionQueue.control,
        requirements=[72],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F237: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F237",
        cwe=209,
        execution_queue=ExecutionQueue.leak,
        requirements=[77, 176],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.local,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F241: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F241",
        cwe=306,
        execution_queue=ExecutionQueue.none,
        requirements=[227, 228, 229, 231, 235, 264, 319],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F246: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F246",
        cwe=311,
        execution_queue=ExecutionQueue.crypto,
        requirements=[134, 135, 185, 229, 264, 300],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.local,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F247: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F247",
        cwe=311,
        execution_queue=ExecutionQueue.aws,
        requirements=[134, 135, 185, 229, 264, 300],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F250: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F250",
        cwe=313,
        execution_queue=ExecutionQueue.aws,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F256: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F256",
        cwe=693,
        execution_queue=ExecutionQueue.aws,
        requirements=[186, 265],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F258: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F258",
        cwe=463,
        execution_queue=ExecutionQueue.aws,
        requirements=[186, 265],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.high,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F259: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F259",
        cwe=463,
        execution_queue=ExecutionQueue.aws,
        requirements=[186, 265],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.high,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F281: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F281",
        cwe=311,
        execution_queue=ExecutionQueue.aws,
        requirements=[181],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F320: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F320",
        cwe=90,
        execution_queue=ExecutionQueue.f014,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F325: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F325",
        cwe=250,
        execution_queue=ExecutionQueue.aws,
        requirements=[95, 96, 186],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.low,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F333: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F333",
        cwe=16,
        execution_queue=ExecutionQueue.aws,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.high,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.high,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F335: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F335",
        cwe=922,
        execution_queue=ExecutionQueue.aws,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F338: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F338",
        cwe=749,
        execution_queue=ExecutionQueue.f014,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.unavailable,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F366: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F366",
        cwe=749,
        execution_queue=ExecutionQueue.f014,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.low,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.unknown,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F372: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F372",
        cwe=650,
        execution_queue=ExecutionQueue.aws,
        requirements=[181],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.low,
            attack_vector=cvss3_model.AttackVector.adjacent,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F380: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F380",
        cwe=749,
        execution_queue=ExecutionQueue.f014,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.none,
            exploitability=cvss3_model.Exploitability.unproven,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.required,
        ),
    )
    F393: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F393",
        cwe=937,
        execution_queue=ExecutionQueue.sca,
        requirements=[48, 262],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.low,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.low,
            privileges_required=cvss3_model.PrivilegesRequired.low,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.confirmed,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
    )
    F396: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F396",
        cwe=255,
        execution_queue=ExecutionQueue.aws,
        requirements=[266],
        score=cvss3_model.Score(
            attack_complexity=cvss3_model.AttackComplexity.high,
            attack_vector=cvss3_model.AttackVector.network,
            availability_impact=cvss3_model.AvailabilityImpact.none,
            confidentiality_impact=cvss3_model.ConfidentialityImpact.low,
            exploitability=cvss3_model.Exploitability.poc,
            integrity_impact=cvss3_model.IntegrityImpact.none,
            privileges_required=cvss3_model.PrivilegesRequired.none,
            remediation_level=cvss3_model.RemediationLevel.official_fix,
            report_confidence=cvss3_model.ReportConfidence.reasonable,
            severity_scope=cvss3_model.SeverityScope.unchanged,
            user_interaction=cvss3_model.UserInteraction.none,
        ),
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

    @classmethod
    def from_historic(
        cls,
        historic_states: List[Dict[str, str]],
    ) -> VulnerabilitySourceEnum:
        # https://gitlab.com/fluidattacks/product/-/issues/4648
        return (
            VulnerabilitySourceEnum.SKIMS
            if any(
                historic_state["source"] in {"machine", "skims"}
                for historic_state in historic_states
            )
            # Let's return the source that first reported the vuln
            else VulnerabilitySourceEnum.INTEGRATES
        )


class VulnerabilityVerificationStateEnum(Enum):
    NOT_REQUESTED: str = "NOT_REQUESTED"
    REQUESTED: str = "REQUESTED"
    VERIFIED: str = "VERIFIED"


class VulnerabilityVerification(NamedTuple):
    date: datetime
    state: VulnerabilityVerificationStateEnum

    @classmethod
    def from_historic(
        cls,
        historic: List[Dict[str, str]],
    ) -> Tuple[VulnerabilityVerification, ...]:
        return tuple(
            VulnerabilityVerification(
                date=time_model.from_colombian(
                    string=item["date"],
                    fmt=time_model.INTEGRATES_1,
                ),
                state=VulnerabilityVerificationStateEnum(item["status"]),
            )
            for item in historic
            if item["status"] is not None
            if item["date"] is not None
        )


class GrammarMatch(NamedTuple):
    start_column: int
    start_line: int


class IntegratesVulnerabilityMetadata(NamedTuple):
    commit_hash: Optional[str] = None
    source: Optional[VulnerabilitySourceEnum] = None
    verification: Optional[Tuple[VulnerabilityVerification, ...]] = None
    uuid: Optional[str] = None


class NVDVulnerability(NamedTuple):
    code: str
    cvss: str
    description: str
    product: str
    url: str
    version: str


class SkimsAPKConfig(NamedTuple):
    exclude: Tuple[str, ...]
    include: Tuple[str, ...]


class SkimsHttpConfig(NamedTuple):
    include: Tuple[str, ...]


class SkimsPathConfig(NamedTuple):
    exclude: Tuple[str, ...]
    include: Tuple[str, ...]
    lib_path: bool
    lib_root: bool


class SkimsSslTarget(NamedTuple):
    host: str
    port: int


class SkimsSslConfig(NamedTuple):
    include: Tuple[SkimsSslTarget, ...]


class SkimsConfig(NamedTuple):
    apk: SkimsAPKConfig
    checks: Set[FindingEnum]
    group: Optional[str]
    http: SkimsHttpConfig
    language: LocalesEnum
    namespace: str
    output: Optional[str]
    path: SkimsPathConfig
    ssl: SkimsSslConfig
    start_dir: str
    working_dir: str


class SkimsVulnerabilityMetadata(NamedTuple):
    cwe: Tuple[int, ...]
    description: str
    snippet: str
    source_method: str


class IntegratesVulnerabilitiesLines(NamedTuple):
    commit_hash: str
    line: str
    path: str
    repo_nickname: str
    state: VulnerabilityStateEnum


class IntegratesVulnerabilitiesInputs(NamedTuple):
    field: str
    repo_nickname: str
    state: VulnerabilityStateEnum
    stream: str
    url: str


class Vulnerability(NamedTuple):
    finding: FindingEnum
    kind: VulnerabilityKindEnum
    state: VulnerabilityStateEnum
    what: str
    where: str
    namespace: str
    stream: Optional[str] = "skims"

    integrates_metadata: Optional[IntegratesVulnerabilityMetadata] = None
    skims_metadata: Optional[SkimsVulnerabilityMetadata] = None

    @property
    def digest(self) -> int:
        """Hash a Vulnerability according to Integrates rules."""
        return hash(
            (
                self.finding,
                self.kind,
                self.namespace,
                self.what,
                self.where,
            )
        )

    @property
    def what_on_integrates(self) -> str:
        if self.kind == VulnerabilityKindEnum.INPUTS:
            what = f"{self.what} ({self.namespace})"
        elif self.kind == VulnerabilityKindEnum.LINES:
            what = f"{self.namespace}/{self.what}"
        elif self.kind == VulnerabilityKindEnum.PORTS:
            what = f"{self.what} ({self.namespace})"
        else:
            raise NotImplementedError()

        return what

    @classmethod
    def what_from_integrates(
        cls, kind: VulnerabilityKindEnum, what_on_integrates: str
    ) -> Tuple[str, str]:
        if kind in {
            VulnerabilityKindEnum.INPUTS,
            VulnerabilityKindEnum.PORTS,
        }:
            if len(chunks := what_on_integrates.rsplit(" (", maxsplit=1)) == 2:
                what, namespace = chunks
                namespace = namespace[:-1]
            else:
                what, namespace = chunks[0], ""
        elif kind == VulnerabilityKindEnum.LINES:
            if len(chunks := what_on_integrates.split("/", maxsplit=1)) == 2:
                namespace, what = chunks
            else:
                namespace, what = "", chunks[0]
        else:
            raise NotImplementedError()

        return namespace, what


Vulnerabilities = Tuple[Vulnerability, ...]
