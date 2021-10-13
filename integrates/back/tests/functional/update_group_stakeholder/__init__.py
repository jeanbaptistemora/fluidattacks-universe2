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


async def get_result(
    *,
    user: str,
    stakeholder: str,
    group: str,
    responsibility: str,
    role: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            updateGroupStakeholder (
                email: "{stakeholder}"
                groupName: "{group}"
                responsibility: "{responsibility}"
                role: {role}
            ) {{
                success
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
