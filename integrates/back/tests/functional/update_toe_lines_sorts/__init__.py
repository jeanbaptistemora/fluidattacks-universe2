# Standard libraries
import json
import os
from typing import (
    Any,
    Dict
)

# Local libraries
from back.tests.functional.utils import get_graphql_result
from dataloaders import get_new_context


async def query(
    *,
    user: str,
    group_name: str,
    filename: str,
    sorts_risk_level: str
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            updateToeLinesSorts(
                groupName: "{group_name}",
                filename: "{filename}",
                sortsRiskLevel: {sorts_risk_level}
            ) {{
                success
            }}
        }}
    """
    data: Dict[str, Any] = {
        'query': query
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def query_get(
    *,
    user: str,
    group_name: str
) -> Dict[str, Any]:
    query: str = f"""{{
        group: project(projectName: "{group_name}") {{
            name
            roots {{
                ... on GitRoot {{
                    id
                    toeLines {{
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
    data: Dict[str, Any] = {
        'query': query
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
