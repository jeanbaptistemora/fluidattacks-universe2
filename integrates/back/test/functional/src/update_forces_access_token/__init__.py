# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


async def update_access_token(
    *,
    user: str,
    group: str,
) -> dict:
    query: str = """
        mutation UpdateForcesAccessToken($groupName: String!) {
            updateForcesAccessToken(groupName: $groupName) {
                success
                sessionJwt
            }
        }
    """
    data: dict = {"query": query, "variables": {"groupName": group}}

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_group_data(
    *,
    user: str,
    group: str,
    session_jwt: str,
) -> dict:
    query: str = """
        query GetGroupData ($groupName: String!) {
            group(groupName: $groupName) {
                name
                businessId
                service
                userRole
                openVulnerabilities
            }
        }
    """
    data: dict = {"query": query, "variables": {"groupName": group}}

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
        session_jwt=session_jwt,
    )


async def get_me_data(
    *,
    user: str,
) -> dict:
    query: str = """
        query GetMeData {
            me {
                accessToken
            }
        }
    """
    data: dict = {"query": query}

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
