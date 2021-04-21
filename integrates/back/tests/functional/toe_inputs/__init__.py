# Standard libraries
import json
import os
from typing import (
    Any,
    Dict,
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
    group_name: str,
) -> Dict[str, Any]:
    query: str = f"""{{
        project(projectName: "{group_name}"){{
            toeInputs {{
                commit
                component
                createdDate
                entryPoint
                seenFirstTimeBy
                testedDate
                verified
                vulns
            }}
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
