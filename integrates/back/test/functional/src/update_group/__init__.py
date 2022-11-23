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
        mutation {{
            updateGroup(
                comments: "",
                groupName: "{group}",
                subscription: ONESHOT,
                hasSquad: false,
                hasAsm: false,
                hasMachine: false,
                reason: NONE,
                tier: ONESHOT,
            ) {{
                success
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_query_group(
    *,
    email: str,
    group_name: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            group(groupName: "{group_name}"){{
                name
                __typename
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
