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
    address: str,
    group_name: str,
    port: str,
    root_id: str,
    be_present: bool,
    has_recent_attack: bool,
    user: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateToePort(
                address: "{address}",
                groupName: "{group_name}",
                port: {port},
                rootId: "{root_id}",
                bePresent: {str(be_present).lower()},
                hasRecentAttack: {str(has_recent_attack).lower()},
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
