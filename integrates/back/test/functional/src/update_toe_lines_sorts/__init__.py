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
    sorts_risk_level_date: str,
    sorts_suggestions: list[dict[str, Any]],
) -> dict[str, Any]:
    sorts_suggestions_formatted: str = "".join(
        f"""
            {{
                findingTitle: "{item["findingTitle"]}",
                probability: {item["probability"]}
            }}
        """
        for item in sorts_suggestions
    )
    query: str = f"""
        mutation {{
            updateToeLinesSorts(
                groupName: "{group_name}",
                rootNickname: "{root_nickname}",
                filename: "{filename}",
                sortsRiskLevel: {sorts_risk_level},
                sortsRiskLevelDate: "{sorts_risk_level_date}",
                sortsSuggestions: [{sorts_suggestions_formatted}]
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
                        sortsRiskLevelDate
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
