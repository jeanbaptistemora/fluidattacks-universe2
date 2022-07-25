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
    event_id: str,
    event_type: str,
    affected_components: list[str],
) -> dict[str, Any]:
    query: str = f"""
        mutation  UpdateEventMutation(
            $affectedComponents: [AffectedComponents]
        ){{
            updateEvent(
                eventId: "{event_id}"
                affectedComponents: $affectedComponents
                eventType: {event_type}
            ) {{
                success
            }}
        }}
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {"affectedComponents": affected_components},
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
