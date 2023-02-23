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
    min_time_to_remediate: int = 18,
    severity: float = 1.0,
    title: str = "366. Inappropriate coding practices - Transparency Conflict",
    unfulfilled_requirements: list[str] = ["158"],
) -> dict[str, Any]:
    query: str = f"""
        mutation AddFinding($unfulfilledRequirements: [String!]!){{
            addFinding(
                attackVector: {severity}
                attackComplexity: {severity}
                attackVectorDescription: "This is an attack vector"
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
                threat: "Attacker"
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
