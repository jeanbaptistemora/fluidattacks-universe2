# pylint: disable=import-error,dangerous-default-value
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def get_result(
    *,
    user: str,
    description: str,
    recommendation: str,
    attack_vector_description: str = "This is an attack vector",
    min_time_to_remediate: int = 18,
    severity: float = 1.0,
    title: str = "366. Inappropriate coding practices - Transparency Conflict",
    threat: str = "Attacker",
    unfulfilled_requirements: list[str] = ["158"],
) -> dict[str, Any]:
    query: str = f"""
        mutation AddFinding($unfulfilledRequirements: [String!]!){{
            addFinding(
                attackVector: {severity}
                attackComplexity: {severity}
                attackVectorDescription: "{attack_vector_description}"
                availabilityImpact: {severity}
                description: "{description}"
                groupName: "group1"
                confidentialityImpact: {severity}
                exploitability: {severity}
                integrityImpact: {severity}
                minTimeToRemediate: {min_time_to_remediate}
                privilegesRequired: {severity}
                recommendation: "{recommendation}"
                remediationLevel: {severity}
                reportConfidence: {severity}
                severityScope: {severity}
                threat: "{threat}"
                title: "{title}"
                unfulfilledRequirements: $unfulfilledRequirements
                userInteraction: {severity}
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


async def get_result_new_finding(
    *,
    user: str,
    description: str,
    recommendation: str,
    attack_vector_description: str = "This is an attack vector",
    min_time_to_remediate: int = 18,
    title: str = "366. Inappropriate coding practices - Transparency Conflict",
    threat: str = "Attacker",
    unfulfilled_requirements: list[str] = ["158"],
) -> dict[str, Any]:
    # severity is equivalent to vulnerability 011 in criteria
    query: str = f"""
        mutation AddFinding($unfulfilledRequirements: [String!]!){{
            addFinding(
                attackVector: 0.85
                attackComplexity: 0.44
                attackVectorDescription: "{attack_vector_description}"
                availabilityImpact: 0.22
                description: "{description}"
                groupName: "group1"
                confidentialityImpact: 0.22
                exploitability: 0.94
                integrityImpact: 0.22
                minTimeToRemediate: {min_time_to_remediate}
                privilegesRequired: 0.62
                recommendation: "{recommendation}"
                remediationLevel: 0.95
                reportConfidence: 1
                severityScope: 0
                threat: "{threat}"
                title: "{title}"
                unfulfilledRequirements: $unfulfilledRequirements
                userInteraction: 0.85
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
