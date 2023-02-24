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
    group_name: str,
) -> dict[str, Any]:
    query: str = f"""{{
        group(groupName: "{group_name}"){{
            toePorts {{
                edges {{
                    node {{
                        address
                        attackedAt
                        attackedBy
                        bePresent
                        bePresentUntil
                        firstAttackAt
                        seenAt
                        seenFirstTimeBy
                        hasVulnerabilities
                        port
                        root {{
                            __typename
                            id
                            nickname
                        }}
                    }}
                    cursor
                }}
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
            }}
        }}
      }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
