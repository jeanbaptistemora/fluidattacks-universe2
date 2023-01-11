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


def get_query() -> str:
    return """
        query(
            $groupName: String!
        ) {
            group(groupName: $groupName) {
                name
                toeLines {
                    edges {
                        node {
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
                            root {
                                id
                                nickname
                            }
                            seenAt
                            sortsRiskLevel
                            sortsRiskLevelDate
                            sortsSuggestions {
                                findingTitle
                                probability
                            }
                        }
                        cursor
                    }
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                }
            }
        }
    """


async def get_result(
    *,
    user: str,
    group_name: str,
) -> dict[str, Any]:
    query: str = get_query()
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "groupName": group_name,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
