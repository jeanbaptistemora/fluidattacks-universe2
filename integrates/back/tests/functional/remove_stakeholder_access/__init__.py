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
    group: str,
    stakeholder: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            removeStakeholderAccess (
                projectName: "{group}",
                userEmail: "{stakeholder}"
            )
            {{
                removedEmail
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
