# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Optional,
)


def get_query() -> str:
    return """
        query(
            $groupName: String!
            $maxLoc: Int
            $minLoc: Int
            $rootId: ID
        ) {
            group(groupName: $groupName) {
                name
                toeLines(
                    maxLoc: $maxLoc
                    minLoc: $minLoc
                    rootId: $rootId
                ) {
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
    filename: Optional[str] = None,
    max_loc: Optional[int] = None,
    min_loc: Optional[int] = None,
    root_id: Optional[str] = None,
) -> dict[str, Any]:
    query: str = get_query()
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "filename": filename,
            "groupName": group_name,
            "maxLoc": max_loc,
            "minLoc": min_loc,
            "rootId": root_id,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
