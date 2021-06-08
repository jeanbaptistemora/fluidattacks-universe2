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
    group_name: str,
) -> Dict[str, Any]:
    query: str = f"""
        query {{
            finding(
                groupName: "{group_name}"
                identifier: "{finding_id}"
            ){{
                actor
                affectedSystems
                age
                analyst
                attackVectorDesc
                btsUrl
                closedVulnerabilities
                compromisedAttributes
                compromisedRecords
                consulting {{
                    content
                }}
                currentState
                cvssVersion
                cweUrl
                description
                evidence
                historicState
                id
                inputsVulns {{
                    specific
                }}
                isExploitable
                lastVulnerability
                linesVulns {{
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
                projectName
                recommendation
                records
                releaseDate
                remediated
                reportDate
                requirements
                risk
                scenario
                severity
                severityScore
                sorts
                state
                threat
                title
                tracking
                type
                verified
                vulnerabilities {{
                    id
                }}
                zeroRisk {{
                    id
                }}
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
