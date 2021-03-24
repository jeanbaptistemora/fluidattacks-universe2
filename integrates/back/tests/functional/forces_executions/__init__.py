# Standard libraries
from typing import (
    Any,
    Dict,
)

# Local libraries
from backend.api import (
    get_new_context,
)
from back.tests.functional.utils import (
    get_graphql_result,
)


async def query(
    *,
    user: str,
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
        query {{
            forcesExecutions(
                projectName: "{group}",
                fromDate: "2020-02-01T00:00:00Z",
                toDate: "2020-02-28T23:59:59Z"
            ) {{
                fromDate
                toDate
                executions {{
                    projectName
                    execution_id
                    date
                    exitCode
                    gitBranch
                    gitCommit
                    gitOrigin
                    gitRepo
                    kind
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
        'query': query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
