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
    *, user: str, unfulfilled_requirements: list[str] | None = None
) -> dict[str, Any]:
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    attack_vector_description: str = "This is an updated attack vector"
    records: str = "Clave plana"
    description: str = "I just have updated the description"
    recommendation: str = "edited recommendation"
    sorts: str = "YES"
    threat: str = "Updated threat"
    title: str = "060. Insecure service configuration - Host verification"
    query: str = f"""
        mutation UpdateFindingDescription(
            $unfulfilledRequirements: [String!]
        ){{
            updateDescription(
                attackVectorDescription: "{attack_vector_description}",
                description: "{description}",
                findingId: "{finding_id}",
                records: "{records}",
                recommendation: "{recommendation}",
                sorts: {sorts},
                threat: "{threat}",
                title: "{title}",
                unfulfilledRequirements: $unfulfilledRequirements
            ) {{
                finding {{
                    age
                    hacker
                    attackVectorDescription
                    closedVulnerabilities
                    consulting {{
                        content
                    }}
                    currentState
                    cvssVersion
                    description
                    historicState
                    id
                    isExploitable
                    lastVulnerability
                    openAge
                    openVulnerabilities
                    groupName
                    recommendation
                    records
                    releaseDate
                    remediated
                    reportDate
                    requirements
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
                    severityScore
                    state
                    threat
                    title
                    tracking {{
                        accepted
                        acceptedUndefined
                        closed
                        cycle
                        date
                        justification
                        assigned
                        open
                    }}
                    unfulfilledRequirements {{
                        id
                        title
                    }}
                    verified
                }}
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
