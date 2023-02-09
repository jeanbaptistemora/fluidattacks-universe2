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
    org_id: str,
) -> dict[str, Any]:
    query: str = f"""{{
        me(callerOrigin: "API") {{
            accessToken
            callerOrigin
            enrolled
            isConcurrentSession
            notificationsPreferences{{
                email
            }}
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
            pendingEvents{{
                eventDate
                detail
                id
                groupName
                eventStatus
                eventType
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
            tours{{
                newGroup
                newRoot
            }}
            trial {{
                completed
                extensionDate
                extensionDays
                startDate
                state
            }}
            userEmail
            userName
            vulnerabilitiesAssigned{{
                id
            }}
            __typename
        }}
    }}"""
    data: dict[str, str] = {
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
) -> dict[str, Any]:
    query: str = """
        query GetMeAssignedVulnerabilities {
            me {
                findingReattacksConnection {
                    edges {
                        node {
                            groupName
                            id
                            state
                            status
                            verificationSummary {
                                requested
                            }
                            vulnerabilitiesToReattackConnection {
                                edges {
                                    node {
                                        lastRequestedReattackDate
                                    }
                                }
                            }
                        }
                    }
                }
                reattacks {
                    edges {
                        node {
                            lastRequestedReattackDate
                        }
                    }
                }
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
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_has_drafts_rejected(
    *,
    user: str,
) -> dict[str, Any]:
    query: str = """
        query GetMeHasDraftsRejected {
            me {
                hasDraftsRejected
                userEmail
                __typename
            }
        }
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
