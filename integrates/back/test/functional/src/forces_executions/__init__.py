# pylint: disable=import-error
from back.test.functional.src.utils import (
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
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
        query {{
            forcesExecutions(
                groupName: "{group}",
            ) {{
                executions {{
                    groupName
                    executionId
                    date
                    exitCode
                    gitBranch
                    gitCommit
                    gitOrigin
                    gitRepo
                    gracePeriod
                    kind
                    severityThreshold
                    strictness
                    vulnerabilities {{
                        numOfOpenVulnerabilities
                        numOfAcceptedVulnerabilities
                        numOfClosedVulnerabilities
                    }}
                }}
                __typename
            }}
        }}
    """
    data: Dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
