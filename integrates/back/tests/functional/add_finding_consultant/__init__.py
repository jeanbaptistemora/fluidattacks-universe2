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
    content: str,
    finding: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            addFindingConsult(
                content: "{content}",
                findingId: "{finding}",
                type: CONSULT,
                parent: "0"
            ) {{
                success
                commentId
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
