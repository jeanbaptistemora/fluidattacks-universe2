# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Dict,
    Optional,
)


async def get_result(
    *,
    user: str,
    finding_id: str,
    reason: str,
    other: Optional[str] = None,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            rejectDraft(
                findingId: "{finding_id}"
                other: "{other}"
                reason: {reason}
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
