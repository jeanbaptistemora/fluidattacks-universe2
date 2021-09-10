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


async def get_result(  # pylint: disable=too-many-locals
    *,
    user: str,
) -> Dict[str, Any]:
    finding_id: str = "475041513"
    affected_systems: str = "edited affected_systems"
    attack_vector_description: str = "This is an updated attack vector"
    records: str = "Clave plana"
    records_number: int = 12
    description: str = "I just have updated the description"
    recommendation: str = "edited recommendation"
    requirements: str = (
        "REQ.0132. Passwords (phrase type) must be at least 3 words long."
    )
    scenario: str = "UNAUTHORIZED_USER_EXTRANET"
    sorts: str = "YES"
    threat: str = "Updated threat"
    title: str = "051. Weak passwords reversed"
    finding_type: str = "SECURITY"
    query: str = f"""
        mutation {{
            updateDescription(
                affectedSystems: "{affected_systems}",
                attackVectorDescription: "{attack_vector_description}",
                description: "{description}",
                findingId: "{finding_id}",
                records: "{records}",
                recommendation: "{recommendation}",
                recordsNumber: {records_number},
                requirements: "{requirements}",
                scenario: "{scenario}",
                sorts: {sorts},
                threat: "{threat}",
                title: "{title}",
                findingType: "{finding_type}"
            ) {{
                finding {{
                    affectedSystems
                    age
                    hacker
                    attackVectorDescription
                    bugTrackingSystemUrl
                    closedVulnerabilities
                    compromisedAttributes
                    compromisedRecords
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
                    risk
                    scenario
                    severity
                    severityScore
                    state
                    threat
                    title
                    tracking
                    type
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
