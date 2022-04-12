# pylint: disable=import-error
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
    org_id: str,
) -> Dict[str, Any]:
    query: str = f"""{{
        me(callerOrigin: "API") {{
            accessToken
            callerOrigin
            hasMobileApp
            isConcurrentSession
            organizations {{
                name
                groups {{
                    hasForces
                    hasSquad
                    name
                }}
            }}
            phone{{
                callingCountryCode
                countryCode
                nationalNumber
            }}
            permissions
            remember
            role
            sessionExpiration
            subscriptionsToEntityReport{{
                entity
                frequency
                subject

            }}
            tags(organizationId: "{org_id}") {{
                name
                groups {{
                    name
                }}
            }}
            __typename
        }}
    }}"""
    data: Dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_vulnerabilities(
    *,
    user: str,
) -> Dict[str, Any]:
    query: str = """
        query GetMeAssignedVulnerabilies {
            me {
                vulnerabilitiesAssigned {
                    id
                    historicTreatment {
                        assigned
                    }
                }
                userEmail
                __typename
            }
        }
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
