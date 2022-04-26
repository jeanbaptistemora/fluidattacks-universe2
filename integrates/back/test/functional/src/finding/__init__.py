# pylint: disable=import-error
from back.test.functional.src.utils import (
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
                evidence {{
                    animation {{
                        date
                        description
                        url
                    }}
                    evidence1 {{
                        date
                        description
                        url
                    }}
                    evidence2 {{
                        date
                        description
                        url
                    }}
                    evidence3 {{
                        date
                        description
                        url
                    }}
                    evidence4 {{
                        date
                        description
                        url
                    }}
                    evidence5 {{
                        date
                        description
                        url
                    }}
                    exploitation {{
                        date
                        description
                        url
                    }}
                }}
                groupName
                historicState
                id
                isExploitable
                lastVulnerability
                minTimeToRemediate
                observations{{
                    content
                }}
                openAge
                openVulnerabilities
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
                vulnerabilitiesConnection {{
                    edges {{
                        node {{
                            id
                        }}
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                }}
                vulnerabilitiesToReattack {{
                    id
                }}
                vulnerabilitiesToReattackConnection {{
                    edges {{
                        node {{
                            id
                        }}
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                }}
                zeroRisk {{
                    id
                }}
                zeroRiskConnection {{
                    edges {{
                        node {{
                            id
                        }}
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
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
