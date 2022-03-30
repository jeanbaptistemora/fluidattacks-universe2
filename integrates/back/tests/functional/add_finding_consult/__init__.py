# pylint: disable=import-error
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
    content: str,
    finding: str,
    mutation_type: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            addFindingConsult(
                content: "{content}",
                findingId: "{finding}",
                type: {mutation_type},
                parentComment: "0"
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
