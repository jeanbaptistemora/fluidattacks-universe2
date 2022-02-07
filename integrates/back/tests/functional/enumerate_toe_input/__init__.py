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
    component: str,
    entry_point: str,
    group_name: str,
    seen_first_time_by: str,
    user: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            enumerateToeInput(
                component: "{component}",
                groupName: "{group_name}",
                entryPoint: "{entry_point}",
                seenFirstTimeBy: "{seen_first_time_by}",
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
