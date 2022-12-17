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
            detail
            eventDate
            eventStatus
            eventType
            evidences{{
                file1 {{
                    fileName
                    date
                }}
                image1 {{
                    fileName
                    date
                }}
                image2 {{
                    fileName
                    date
                }}
                image3 {{
                    fileName
                    date
                }}
                image4 {{
                    fileName
                    date
                }}
                image5 {{
                    fileName
                    date
                }}
                image6 {{
                    fileName
                    date
                }}
            }}
            groupName
            hacker
            id
            __typename
        }}
    }}"""
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
