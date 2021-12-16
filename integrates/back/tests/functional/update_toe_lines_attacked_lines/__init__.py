from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)


async def get_result(
    *,
    user: str,
    attacked_at: str,
    attacked_lines: Optional[int],
    group_name: str,
    comments: str,
    filenames: List[str],
    root_id: str,
) -> Dict[str, Any]:
    variables: Dict[str, Any] = {
        "attackedAt": attacked_at,
        "comments": comments,
        "filenames": filenames,
        "groupName": group_name,
        "rootId": root_id,
    }
    if attacked_lines:
        variables["attackedLines"] = attacked_lines
    query: str = f"""
        mutation UpdateToeLinesAttackedLinesMutation(
            $attackedAt: DateTime!,
            $attackedLines: Int,
            $comments: String!,
            $filenames: [String!]!,
            $groupName: String!,
            $rootId: String!
        ) {{
            updateToeLinesAttackedLines(
                attackedLines:  $attackedLines,
                groupName: $groupName,
                rootId:  $rootId,
                filenames: $filenames,
                attackedAt:  $attackedAt,
                comments: $comments
            ) {{
                success
            }}
        }}
    """
    data: Dict[str, Any] = {
        "query": query,
        "variables": variables,
    }
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
                            id
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
