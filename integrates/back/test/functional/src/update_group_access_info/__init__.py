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
    group_context: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateGroupAccessInfo(
                groupContext: "{group_context}",
                groupName: "{group}",
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
