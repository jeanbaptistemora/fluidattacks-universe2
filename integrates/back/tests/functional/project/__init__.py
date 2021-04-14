# Standard libraries
import json
import os
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
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
        query {{
            project(projectName: "{group}"){{
                analytics(documentName: "", documentType: "")
                name
                hasDrills
                hasForces
                hasIntegrates
                openVulnerabilities
                closedVulnerabilities
                lastClosingVuln
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
                    analyst
                }}
                stakeholders{{
                    email
                }}
                consulting {{
                    content
                }}
                findings(filters: {{affectedSystems: "system1", actor: "SOME_CUSTOMERS"}}) {{
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
                lastClosingVulnFinding {{
                    analyst
                }}
                maxSeverityFinding {{
                    analyst
                }}
                __typename
            }}
        }}
    """
    data: Dict[str, Any] = {
        'query': query
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
