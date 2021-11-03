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


async def get_result_mutation(
    *,
    user: str,
) -> Dict[str, Any]:
    query: str = """
        mutation {
            removeStakeholder {
                success
            }
        }
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_result_me_query(
    *,
    user: str,
    organization_id: str,
) -> Dict[str, Any]:
    query: str = f"""
        query {{
            me(callerOrigin: "API") {{
                remember
                role
                tags(organizationId: "${organization_id}") {{
                    organization
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


async def get_result_stakeholder_query(
    *, user: str, stakeholder: str, group: str
) -> Dict[str, Any]:
    query: str = f"""
        query {{
            stakeholder(entity: GROUP,
                    groupName: "{group}",
                    userEmail: "{stakeholder}") {{
                email
                role
                responsibility
                firstLogin
                lastLogin
                groups {{
                    name
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
