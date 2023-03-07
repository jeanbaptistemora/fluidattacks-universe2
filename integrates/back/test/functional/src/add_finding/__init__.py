# pylint: disable=import-error,dangerous-default-value
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding31Severity,
)
from decimal import (
    Decimal,
)
from typing import (
    Any,
)


async def get_result(
    *,
    user: str,
    description: str,
    threat: str,
    recommendation: str = "Recommendation",
    attack_vector_description: str = "This is an attack vector",
    min_time_to_remediate: int = 18,
    severity: Finding31Severity = Finding31Severity(
        attack_complexity=Decimal("0.01"),
        attack_vector=Decimal("0.85"),
        availability_impact=Decimal("0.22"),
        confidentiality_impact=Decimal("0.22"),
        exploitability=Decimal("0.94"),
        integrity_impact=Decimal("0.22"),
        privileges_required=Decimal("0.62"),
        severity_scope=Decimal("0"),
        remediation_level=Decimal("0.95"),
        report_confidence=Decimal("1"),
        user_interaction=Decimal("0.85"),
    ),
    title: str = "366. Inappropriate coding practices - Transparency Conflict",
    unfulfilled_requirements: list[str] = ["158"],
) -> dict[str, Any]:
    query: str = f"""
        mutation AddFinding($unfulfilledRequirements: [String!]!){{
            addFinding(
                attackVector: {severity.attack_vector}
                attackComplexity: {severity.attack_complexity}
                attackVectorDescription: "{attack_vector_description}"
                availabilityImpact: {severity.availability_impact}
                availabilityRequirement: {severity.availability_requirement}
                description: "{description}"
                groupName: "group1"
                confidentialityImpact: {severity.confidentiality_impact}
                confidentialityRequirement:
                {severity.confidentiality_requirement}
                exploitability: {severity.exploitability}
                integrityImpact: {severity.integrity_impact}
                integrityRequirement: {severity.integrity_requirement}
                minTimeToRemediate: {min_time_to_remediate}
                modifiedAttackComplexity: {severity.modified_attack_complexity}
                modifiedAttackVector: {severity.modified_attack_vector}
                modifiedAvailabilityImpact:
                {severity.modified_availability_impact}
                modifiedConfidentialityImpact:
                {severity.modified_confidentiality_impact}
                modifiedIntegrityImpact: {severity.modified_integrity_impact}
                modifiedPrivilegesRequired:
                {severity.modified_privileges_required}
                modifiedSeverityScope: {severity.modified_severity_scope}
                modifiedUserInteraction: {severity.modified_user_interaction}
                privilegesRequired: {severity.privileges_required}
                recommendation: "{recommendation}"
                remediationLevel: {severity.remediation_level}
                reportConfidence: {severity.report_confidence}
                severityScope: {severity.severity_scope}
                threat: "{threat}"
                title: "{title}"
                unfulfilledRequirements: $unfulfilledRequirements
                userInteraction: {severity.user_interaction}
            ) {{
                success
            }}
        }}
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {"unfulfilledRequirements": unfulfilled_requirements},
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
