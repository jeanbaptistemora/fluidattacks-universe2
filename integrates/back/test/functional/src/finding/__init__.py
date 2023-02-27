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
    *,
    user: str,
    finding_id: str,
) -> dict[str, Any]:
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
                    created
                }}
                currentState
                cvssVersion
                description
                draftsConnection {{
                    edges {{
                        node {{
                            id
                            state
                        }}
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                }}
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
                lastStateDate
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
                status
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
                    safe
                    vulnerable
                }}
                treatmentSummary {{
                    accepted
                    acceptedUndefined
                    inProgress
                    new
                    untreated
                }}
                verificationSummary {{
                    requested
                    onHold
                    verified
                }}
                verified
                vulnerabilitiesConnection {{
                    edges {{
                        node {{
                            currentState
                            id
                            state
                        }}
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
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
                zeroRiskConnection(state: VULNERABLE) {{
                    edges {{
                        node {{
                            currentState
                            id
                            state
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
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
