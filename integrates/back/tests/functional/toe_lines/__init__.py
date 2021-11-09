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
) -> Dict[str, Any]:
    query: str = f"""{{
        group(groupName: "{group_name}"){{
            name
            roots {{
                ... on GitRoot {{
                    id
                    toeLines {{
                        attackedAt
                        attackedBy
                        attackedLines
                        bePresent
                        comments
                        commitAuthor
                        filename
                        firstAttackAt
                        loc
                        modifiedCommit
                        modifiedDate
                        seenAt
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
