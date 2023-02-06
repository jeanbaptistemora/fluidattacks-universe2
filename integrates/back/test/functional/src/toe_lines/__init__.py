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
            $fromModifiedDate: DateTime
            $groupName: String!
            $hasVulnerabilities: Boolean
            $lastCommit: String
            $maxLoc: Int
            $minLoc: Int
            $rootId: ID
            $toModifiedDate: DateTime
        ) {
            group(groupName: $groupName) {
                name
                toeLines(
                    fromModifiedDate: $fromModifiedDate
                    hasVulnerabilities: $hasVulnerabilities
                    lastCommit: $lastCommit
                    maxLoc: $maxLoc
                    minLoc: $minLoc
                    rootId: $rootId
                    toModifiedDate: $toModifiedDate
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
    from_modified_date: Optional[str] = None,
    has_vulnerabilities: Optional[bool] = None,
    last_commit: Optional[str] = None,
    max_loc: Optional[int] = None,
    min_loc: Optional[int] = None,
    root_id: Optional[str] = None,
    to_modified_date: Optional[str] = None,
) -> dict[str, Any]:
    query: str = get_query()
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "filename": filename,
            "fromModifiedDate": from_modified_date,
            "groupName": group_name,
            "hasVulnerabilities": has_vulnerabilities,
            "lastCommit": last_commit,
            "maxLoc": max_loc,
            "minLoc": min_loc,
            "rootId": root_id,
            "toModifiedDate": to_modified_date,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
