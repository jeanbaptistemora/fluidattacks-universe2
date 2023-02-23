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
    title: str = "366. Inappropriate coding practices - Transparency Conflict",
    unfulfilled_requirements: list[str] = ["158"],
) -> dict[str, Any]:
    query: str = f"""
        mutation AddFinding($unfulfilledRequirements: [String!]!){{
            addFinding(
                attackVector: 1.0
                attackComplexity: 1.0
                attackVectorDescription: "This is an attack vector"
                availabilityImpact: 1.0
                description: "{description}"
                groupName: "group1"
                confidentialityImpact: 1.0
                exploitability: 1.0
                integrityImpact: 1.0
                minTimeToRemediate: {min_time_to_remediate}
                privilegesRequired: 1.0
                recommendation: "{recommendation}"
                remediationLevel: 1.0
                reportConfidence: 1.0
                severityScope: 1.0
                threat: "Attacker"
                title: "{title}"
                unfulfilledRequirements: $unfulfilledRequirements
                userInteraction: 1.0
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
