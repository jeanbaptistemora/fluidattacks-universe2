# pylint: disable=import-error
from back.tests.functional.utils import (
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
    disambiguation: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateGroupDisambiguation(
                disambiguation: "{disambiguation}",
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
