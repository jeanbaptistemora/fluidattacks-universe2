from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Dict,
)


async def query(
    *,
    user: str,
    stakeholder: str,
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
        query {{
            stakeholder(entity: PROJECT,
                    projectName: "{group}",
                    userEmail: "{stakeholder}") {{
                email
                role
                responsibility
                phoneNumber
                firstLogin
                lastLogin
                projects {{
                    name
                }}
                __typename
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
