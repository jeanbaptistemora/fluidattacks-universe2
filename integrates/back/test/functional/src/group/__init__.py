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
    group: str,
) -> dict[str, Any]:
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
                managed
                maxAcceptanceDays
                maxAcceptanceSeverity
                maxNumberAcceptances
                meanRemediate
                meanRemediateCriticalSeverity
                meanRemediateHighSeverity
                meanRemediateLowSeverity
                meanRemediateMediumSeverity
                minAcceptanceSeverity
                minBreakingSeverity
                openFindings
                subscription
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
                language
                groupContext
                service
                tier
                businessId
                businessName
                sprintDuration
                sprintStartDate
                vulnerabilityGracePeriod
                vulnerabilities(stateStatus: "open") {{
                    edges {{
                        node {{
                            currentState
                            id
                            state
                        }}
                    }}
                }}
                __typename
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
