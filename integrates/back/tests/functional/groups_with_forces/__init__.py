# Standard libraries
import json
import os
from typing import (
    Any,
    Dict,
    List,
)

# Third party libraries
from starlette.datastructures import (
    UploadFile,
)

# Local libraries
from backend.api import (
    get_new_context,
)
from back.tests.functional.utils import (
    get_graphql_result,
)


async def query(
    *,
    user: str,
) -> Dict[str, Any]:
    query: str = """{
        groupsWithForces
    }"""
    data: Dict[str, Any] = {
        'query': query
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
