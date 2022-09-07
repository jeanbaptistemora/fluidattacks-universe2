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
)


async def get_result(
    *,
    user: str,
    group_name: str,
) -> dict[str, Any]:
    query: str = f"""{{
        group(groupName: "{group_name}"){{
            name
            toeLines {{
                edges {{
                    node {{
                        attackedAt
                        attackedBy
                        attackedLines
                        bePresent
                        bePresentUntil
                        comments
                        lastAuthor
                        filename
                        firstAttackAt
                        loc
                        lastCommit
                        modifiedDate
                        root {{
                            id
                            nickname
                        }}
                        seenAt
                        sortsRiskLevel
                        sortsSuggestions {{
                            findingTitle
                            probability
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
