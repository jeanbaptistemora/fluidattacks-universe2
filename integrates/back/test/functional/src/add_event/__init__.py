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
)


async def get_result(
    *,
    user: str,
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            addEvent(
                groupName: "{group}",
                actionAfterBlocking: TRAINING,
                actionBeforeBlocking: DOCUMENT_GROUP,
                accessibility: ENVIRONMENT,
                context: CLIENT,
                detail: "hacker create new event",
                eventDate: "2020-02-01T00:00:00Z",
                eventType: INCORRECT_MISSING_SUPPLIES
                rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690"
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
