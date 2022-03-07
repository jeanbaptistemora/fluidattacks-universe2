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
                forcesToken
                name
                hasSquad
                hasForces
                hasAsm
                hasMachine
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
                    id
                }}
                stakeholders{{
                    email
                }}
                consulting {{
                    content
                }}
                findings(
                    filters: {{
                        verified: false
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
                        vulnerabilities {{
                            id
                        }}
                    }}
                }}
                drafts {{
                    id
                    title
                }}
                lastClosedVulnerabilityFinding {{
                    id
                }}
                maxSeverityFinding {{
                    id
                }}
                language
                groupContext
                service
                tier
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


async def get_vulnerabilities(
    *,
    user: str,
    group: str,
) -> Dict[str, Any]:
    query: str = """
        query GetGroupVulnerabilies($groupName: String!) {
            group(groupName: $groupName) {
                name
                vulnerabilitiesAssigned {
                    id
                    historicTreatment {
                        assigned
                    }
                }
                __typename
            }
        }
    """
    data: Dict[str, Any] = {"query": query, "variables": {"groupName": group}}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
