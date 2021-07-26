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
)


async def get_result(
    *,
    user: str,
    finding: str,
    open_vulnerabilities: List[str],
    closed_vulnerabilities: List[str],
) -> Dict[str, Any]:
    query: str = """
        mutation VerifyRequestVulnerabilities(
            $findingId: String!
            $justification: String!
            $openVulnerabilities: [String]!
            $closedVulnerabilities: [String]!
        ) {
            verifyRequestVulnerabilities(
                findingId: $findingId
                justification: $justification
                openVulnerabilities: $openVulnerabilities
                closedVulnerabilities: $closedVulnerabilities
            ) {
                success
            }
        }
    """
    data: Dict[str, Any] = {
        "query": query,
        "variables": {
            "findingId": finding,
            "justification": "Vulnerabilities verified",
            "openVulnerabilities": open_vulnerabilities,
            "closedVulnerabilities": closed_vulnerabilities,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_vulnerability(
    *,
    user: str,
    vulnerability_id: str,
) -> Dict[str, Any]:
    query: str = f"""
        {{
            vulnerability(uuid: "{vulnerability_id}") {{
                currentState
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
