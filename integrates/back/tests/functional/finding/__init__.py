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
    finding: str,
) -> Dict[str, Any]:
    query: str = f"""
        query {{
            finding(identifier: "{finding}"){{
                id
                groupName
                releaseDate
                severity
                cvssVersion
                state
                lastVulnerability
                remediated
                age
                isExploitable
                severityScore
                reportDate
                historicState
                currentState
                newRemediated
                verified
                hacker
                portsVulnerabilities {{
                    specific
                }}
                inputsVulnerabilities {{
                    specific
                }}
                linesVulnerabilities {{
                    specific
                }}
                consulting {{
                    content
                }}
                records
                evidence
                title
                scenario
                actor
                description
                requirements
                attackVectorDescription
                threat
                recommendation
                affectedSystems
                compromisedAttributes
                compromisedRecords
                bugTrackingSystemUrl
                risk
                type
                tracking
                observations{{
                    content
                }}
                vulnerabilities{{
                    id
                }}
                openVulnerabilities
                closedVulnerabilities
                treatmentSummary {{
                    accepted
                    acceptedUndefined
                    inProgress
                    new
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
