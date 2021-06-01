from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Dict,
    Optional,
)


async def query(
    *,
    email: str,
    group_name: str,
    id: str,
    new_root_id: Optional[str],
    reason: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            deactivateRoot(
                groupName: "{group_name}",
                id: "{id}",
                newRootId: "{new_root_id}",
                reason: {reason}
            ) {{
                success
            }}
        }}
    """
    data = {"query": query}

    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
