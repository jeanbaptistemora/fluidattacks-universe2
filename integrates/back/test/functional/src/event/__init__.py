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
    query: str = f"""{{
        event(identifier: "{event}"){{
            affectedReattacks {{
                id
            }}
            client
            closingDate
            consulting {{
                content
                id
                fullName
                created
            }}
            context
            detail
            eventDate
            eventStatus
            eventType
            evidence
            evidenceDate
            evidenceFile
            evidenceFileDate
            groupName
            hacker
            historicState
            id
            subscription
            __typename
        }}
    }}"""
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
