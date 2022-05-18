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
    root_nickname: str,
    filename: str,
    sorts_risk_level: int,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateToeLinesSorts(
                groupName: "{group_name}",
                rootNickname: "{root_nickname}",
                filename: "{filename}",
                sortsRiskLevel: {sorts_risk_level}
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


async def query_get(
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
                            nickname
                        }}
                        seenAt
                        sortsRiskLevel
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
