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
    user: str,
    event: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            solveEvent(
                eventId: "{event}",
                affectation: "1",
                date: "2020-02-01T00:00:00Z"
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
