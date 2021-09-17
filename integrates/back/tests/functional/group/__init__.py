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
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
        query {{
            group(groupName: "{group}"){{
                analytics(documentName: "", documentType: "")
                name
                hasSquad
                hasForces
                hasAsm
                openVulnerabilities
                closedVulnerabilities
                lastClosedVulnerability
                maxSeverity
                meanRemediate
                meanRemediateCriticalSeverity
                meanRemediateHighSeverity
                meanRemediateLowSeverity
                meanRemediateMediumSeverity
                openFindings
                totalFindings
                totalTreatment
                subscription
                deletionDate
                userDeletion
                tags
                description
                serviceAttributes
                organization
                userRole
                maxOpenSeverity
                maxOpenSeverityFinding {{
                    hacker
                }}
                stakeholders{{
                    email
                }}
                consulting {{
                    content
                }}
                findings(
                    filters: {{
                        affectedSystems: "system1"
                    }}
                ) {{
                    id
                }}
                events {{
                    id
                }}
                roots {{
                    ...on GitRoot {{
                        id
                    }}
                }}
                drafts {{
                    id
                    title
                }}
                lastClosedVulnerabilityFinding {{
                    hacker
                }}
                maxSeverityFinding {{
                    hacker
                }}
                __typename
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
