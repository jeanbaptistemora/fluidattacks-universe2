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
    tag: str,
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            removeTag (
            tag: "{tag}",
            projectName: "{group}",
            ) {{
            success
            }}
        }}
    """
    data: Dict[str, Any] = {
        'query': query
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
