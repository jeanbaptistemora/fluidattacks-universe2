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


async def get_stakeholder_organizations(
    *,
    email: str,
) -> dict[str, Any]:
    query: str = """{
        me(callerOrigin: "API") {
            organizations {
                id
                groups {
                    name
                }
            }
            __typename
        }
    }"""
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )


async def get_result(
    *,
    email: str,
    group_name: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            unsubscribeFromGroup(groupName: "{group_name}"){{
                success
            }}
        }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
