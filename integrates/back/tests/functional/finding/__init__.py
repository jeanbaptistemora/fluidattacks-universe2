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
    finding_id: str,
) -> Dict[str, Any]:
    query: str = f"""
        query {{
            finding(
                identifier: "{finding_id}"
            ){{
                affectedSystems
                age
                hacker
                attackVectorDesc
                attackVectorDescription
                closedVulnerabilities
                consulting {{
                    content
                }}
                currentState
                cvssVersion
                description
                evidence
                groupName
                historicState
                id
                inputsVulns {{
                    specific
                }}
                inputsVulnerabilities {{
                    specific
                }}
                isExploitable
                lastVulnerability
                linesVulns {{
                    specific
                }}
                linesVulnerabilities {{
                    specific
                }}
                newRemediated
                observations{{
                    content
                }}
                openAge
                openVulnerabilities
                portsVulns {{
                    specific
                }}
                portsVulnerabilities {{
                    specific
                }}
                projectName
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
                sorts
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
                treatmentSummary {{
                    accepted
                    acceptedUndefined
                    inProgress
                    new
                }}
                verified
                vulnerabilities {{
                    id
                }}
                vulnsToReattack {{
                    id
                }}
                vulnerabilitiesToReattack {{
                    id
                }}
                zeroRisk {{
                    id
                }}
                where
                __typename
            }}
        }}
    """
    data: Dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
