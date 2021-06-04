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


async def query(
    *,
    user: str,
    finding_id: str,
    group_name: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            deleteFinding(
                groupName: "{group_name}"
                findingId: "{finding_id}"
                justification: NOT_REQUIRED
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
