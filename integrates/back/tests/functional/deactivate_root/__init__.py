# Standard
from typing import Any, Dict

# Local
from back.tests.functional.utils import get_graphql_result
from backend.api import get_new_context


async def query(
    *,
    email: str,
    group_name: str,
    id: str,
    new_repo: str,
    reason: str
) -> Dict[str, Any]:
    query: str = f'''
        mutation {{
            deactivateRoot(
                groupName: "{group_name}",
                id: "{id}",
                newRepo: "{new_repo}",
                reason: {reason}
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}

    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
