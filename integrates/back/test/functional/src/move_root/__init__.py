# pylint: disable=import-error
from back.test.functional.src.utils import (
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
    root_id: str,
    source_group_name: str,
    target_group_name: str,
    user: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            moveRoot(
                groupName: "{source_group_name}",
                id: "{root_id}",
                targetGroupName: "{target_group_name}"
            ) {{
                success
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
