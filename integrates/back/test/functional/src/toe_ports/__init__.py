# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    group_name: str,
) -> Dict[str, Any]:
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
                        port
                        root {{
                            ... on GitRoot {{
                            __typename
                            id
                            nickname
                            }}
                            ... on IPRoot {{
                            __typename
                            id
                            nickname
                            }}
                            ... on URLRoot {{
                            __typename
                            id
                            nickname
                            }}
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
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
