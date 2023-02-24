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
    event: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            downloadEventFile(
                eventId: "{event}",
                fileName: "unittesting_418900971_evidence_file_1.csv"
            ) {{
                success
                url
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
