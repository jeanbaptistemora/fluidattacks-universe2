from db_model.findings.enums import (
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
from db_model.findings.types import (
    Finding,
    Finding31Severity,
)
from typing import (
    Any,
)


def get_finding_machine_severity(
    criteria_vulnerability: dict[str, Any],
) -> Finding31Severity:
    return Finding31Severity(
        attack_complexity=AttackComplexity[
            criteria_vulnerability["score"]["base"]["attack_complexity"]
        ].value,
        attack_vector=AttackVector[
            criteria_vulnerability["score"]["base"]["attack_vector"]
        ].value,
        availability_impact=AvailabilityImpact[
            criteria_vulnerability["score"]["base"]["availability"]
        ].value,
        confidentiality_impact=ConfidentialityImpact[
            criteria_vulnerability["score"]["base"]["confidentiality"]
        ].value,
        exploitability=Exploitability[
            criteria_vulnerability["score"]["temporal"][
                "exploit_code_maturity"
            ]
        ].value,
        integrity_impact=IntegrityImpact[
            criteria_vulnerability["score"]["base"]["integrity"]
        ].value,
        privileges_required=PrivilegesRequired[
            criteria_vulnerability["score"]["base"]["privileges_required"]
        ].value,
        remediation_level=RemediationLevel[
            criteria_vulnerability["score"]["temporal"]["remediation_level"]
        ].value,
        report_confidence=ReportConfidence[
            criteria_vulnerability["score"]["temporal"]["report_confidence"]
        ].value,
        severity_scope=SeverityScope[
            criteria_vulnerability["score"]["base"]["scope"]
        ].value,
        user_interaction=UserInteraction[
            criteria_vulnerability["score"]["base"]["user_interaction"]
        ].value,
    )


def has_machine_description(
    finding: Finding, criteria_vulnerability: dict[str, Any], language: str
) -> bool:
    return all(
        (
            finding.description.strip()
            == criteria_vulnerability[language]["description"].strip(),
            finding.threat.strip()
            == criteria_vulnerability[language]["threat"].strip(),
            finding.severity
            == get_finding_machine_severity(criteria_vulnerability),
        )
    )
