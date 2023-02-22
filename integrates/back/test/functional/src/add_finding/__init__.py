# pylint: disable=import-error
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
    *, user: str, description: str, recommendation: str
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
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
                minTimeToRemediate: 18
                privilegesRequired: 1.0
                recommendation: "{recommendation}"
                remediationLevel: 1.0
                reportConfidence: 1.0
                severityScope: 1.0
                threat: "Attacker"
                title:
                "366. Inappropriate coding practices - Transparency Conflict"
                unfulfilledRequirements: ["158"]
                userInteraction: 1.0
            ) {{
                success
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
