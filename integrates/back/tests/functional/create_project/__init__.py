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
    org: str,
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            createProject(
                organization: "{org}",
                description: "This is a new project from pytest",
                projectName: "{group}",
                subscription: CONTINUOUS,
                hasSkims: true,
                hasDrills: true,
                hasForces: true
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
