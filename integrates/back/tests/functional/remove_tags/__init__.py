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
    finding: str,
    vuln_id: str,
    tag: str = "",
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            removeTags(
                findingId: "{finding}",
                vulnerabilities: ["{vuln_id}"]
                tag: "{tag}",
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
