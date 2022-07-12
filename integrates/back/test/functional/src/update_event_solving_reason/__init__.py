# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Optional,
)


async def get_result(
    *, user: str, event_id: str, reason: str, other: Optional[str]
) -> dict[str, Any]:
    query: str = f"""
        mutation  UploadFileMutation(
            $other: String
        ){{
            updateEventSolvingReason(
                eventId: "{event_id}"
                reason: {reason}
                other: $other
            ) {{
                success
            }}
        }}
    """
    data: dict[str, Any] = {"query": query, "variables": {"other": other}}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
