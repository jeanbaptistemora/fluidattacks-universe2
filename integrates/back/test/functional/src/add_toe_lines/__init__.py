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
    filename: str,
    group_name: str,
    root_id: str,
    last_author: str,
    last_commit: str,
    loc: int,
    modified_date: str,
    user: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            addToeLines(
                groupName: "{group_name}",
                rootId: "{root_id}",
                filename: "{filename}",
                lastAuthor: "{last_author}",
                lastCommit: "{last_commit}",
                loc: {loc},
                modifiedDate: "{modified_date}",
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
