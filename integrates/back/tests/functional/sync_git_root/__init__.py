# pylint: disable=import-error
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
    user: str,
    group: str,
    root_id: str,
) -> Dict[str, Any]:
    query: str = f"""
      mutation {{
        syncGitRoot(
            groupName: "{group}"
            rootId: "{root_id}"
        ) {{
            success
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
