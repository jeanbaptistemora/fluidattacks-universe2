from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Dict,
)


async def get_result(
    *,
    user: str,
    draft: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            updateSeverity (
            findingId: "{draft}",
            attackComplexity: "0.77", attackVector: "0.62",
            availabilityImpact: "0", availabilityRequirement: "1",
            confidentialityImpact: "0", confidentialityRequirement: "1",
            cvssVersion: "3.1", exploitability: "0.91",
            integrityImpact: "0.22", integrityRequirement: "1",
            modifiedAttackComplexity: "0.77", modifiedAttackVector: "0.62",
            modifiedAvailabilityImpact: "0",
            modifiedConfidentialityImpact: "0",
            modifiedIntegrityImpact: "0.22",
            modifiedPrivilegesRequired: "0.62",
            modifiedSeverityScope: "0", modifiedUserInteraction: "0.85",
            privilegesRequired: "0.62", remediationLevel: "0.97",
            reportConfidence: "0.92",
            severity: "2.9", severityScope: "0", userInteraction: "0.85"
            ) {{
                 finding {{
                    severity {{
                        attackComplexity
                        attackVector
                        availabilityImpact
                        availabilityRequirement
                        confidentialityImpact
                        confidentialityRequirement
                        exploitability
                        integrityImpact
                        integrityRequirement
                        modifiedAttackComplexity
                        modifiedAttackVector
                        modifiedAvailabilityImpact
                        modifiedConfidentialityImpact
                        modifiedIntegrityImpact
                        modifiedPrivilegesRequired
                        modifiedSeverityScope
                        modifiedUserInteraction
                        privilegesRequired
                        remediationLevel
                        reportConfidence
                        severityScope
                        userInteraction
                    }}
                }}
                success
            }}
        }}
    """
    data: Dict[str, str] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
