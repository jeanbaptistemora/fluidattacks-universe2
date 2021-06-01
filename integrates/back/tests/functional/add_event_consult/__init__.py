from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
import json
import os
from typing import (
    Any,
    Dict,
)


async def query(
    *,
    user: str,
    event: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            addEventConsult(eventId: "{event}",
                            parent: "0",
                            content: "Test content of new event") {{
                success
                commentId
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
