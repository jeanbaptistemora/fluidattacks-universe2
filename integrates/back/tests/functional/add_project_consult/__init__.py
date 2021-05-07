# Standard libraries
import json
import os
from typing import (
    Any,
    Dict,
)

# Local libraries
from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


async def query(
    *,
    user: str,
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            addProjectConsult(
                content: "Test consult",
                parent: "0",
                projectName: "{group}",
            ) {{
                success
                commentId
            }}
        }}
    """
    data: Dict[str, str] = {
        'query': query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
