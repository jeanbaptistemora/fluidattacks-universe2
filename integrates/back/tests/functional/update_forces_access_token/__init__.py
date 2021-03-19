# Standard libraries
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
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            updateForcesAccessToken(projectName: "{group}"){{
                success
                sessionJwt
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
