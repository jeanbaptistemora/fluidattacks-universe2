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
    attacked_at: str,
    be_present: bool,
    component: str,
    entry_point: str,
    group_name: str,
    user: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            updateToeInput(
                attackedAt: "{attacked_at}",
                bePresent: {str(be_present).lower()},
                component: "{component}",
                groupName: "{group_name}",
                entryPoint: "{entry_point}",
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
