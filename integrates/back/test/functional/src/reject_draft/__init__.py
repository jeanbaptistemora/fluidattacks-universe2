# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def get_result(
    *,
    user: str,
    finding_id: str,
    reasons: str,
    other: str | None = None,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            rejectDraft(
                findingId: "{finding_id}"
                other: "{other}"
                reasons: [{reasons}]
            ) {{
                success
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
