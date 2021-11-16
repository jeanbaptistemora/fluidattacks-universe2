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
) -> Dict[str, Any]:
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    affected_systems: str = "edited affected_systems"
    attack_vector_description: str = "This is an updated attack vector"
    records: str = "Clave plana"
    description: str = "I just have updated the description"
    recommendation: str = "edited recommendation"
    sorts: str = "YES"
    threat: str = "Updated threat"
    title: str = "051. Cracked weak credentials"
    query: str = f"""
        mutation {{
            updateDescription(
                affectedSystems: "{affected_systems}",
                attackVectorDescription: "{attack_vector_description}",
                description: "{description}",
                findingId: "{finding_id}",
                records: "{records}",
                recommendation: "{recommendation}",
                sorts: {sorts},
                threat: "{threat}",
                title: "{title}",
            ) {{
                finding {{
                    affectedSystems
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
                    evidence
                    historicState
                    id
                    inputsVulnerabilities {{
                        specific
                    }}
                    isExploitable
                    lastVulnerability
                    linesVulnerabilities {{
                        specific
                    }}
                    newRemediated
                    openAge
                    openVulnerabilities
                    portsVulnerabilities {{
                        specific
                    }}
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
                        manager
                        open
                    }}
                    verified
                    vulnerabilities {{
                        id
                    }}
                }}
                success
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
