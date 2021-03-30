# Standard libraries
from typing import (
    Any,
    Dict,
)

# Local libraries
from backend.api import (
    get_new_context,
)
from back.tests.functional.utils import (
    get_graphql_result,
)


async def query(
    *,
    user: str,
    finding: str,
) -> Dict[str, Any]:
    query: str = f'''
        query {{
            finding(identifier: "{finding}"){{
                id
                projectName
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
                analyst
                portsVulns {{
                    specific
                }}
                inputsVulns {{
                    specific
                }}
                linesVulns {{
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
                attackVectorDesc
                threat
                recommendation
                affectedSystems
                compromisedAttributes
                compromisedRecords
                cweUrl
                btsUrl
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
                __typename
            }}
        }}
    '''
    data: Dict[str, str] = {
        'query': query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
