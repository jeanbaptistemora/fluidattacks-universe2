from back.tests.functional.utils import (
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
    root_nickname: str,
    filename: str,
    sorts_risk_level: int,
) -> Dict[str, Any]:
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
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def query_get(
    *,
    user: str,
    group_name: str,
) -> Dict[str, Any]:
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
                        commitAuthor
                        filename
                        firstAttackAt
                        loc
                        modifiedCommit
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
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def query_services_get(*, user: str, group_name: str) -> Dict[str, Any]:
    query: str = f"""{{
        group(groupName: "{group_name}") {{
            name
            roots {{
                ... on GitRoot {{
                    id
                    servicesToeLines {{
                        filename
                        modifiedDate
                        modifiedCommit
                        loc
                        testedDate
                        testedLines
                        comments
                        sortsRiskLevel
                    }}
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
