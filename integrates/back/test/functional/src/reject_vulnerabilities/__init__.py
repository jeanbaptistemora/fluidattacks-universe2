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
    Optional,
)


async def get_result(
    *,
    user: str,
    finding: str,
    vulnerability: str,
    justification: str,
    other_justification: Optional[str],
) -> Dict[str, Any]:
    query: str = """
            mutation RejectVulnerabilities(
                $findingId: String!,
                $justification: VulnerabilityRejectionJustification!,
                $otherJustification: String,
                $vulnerabilities: [String!]!
            ) {
                rejectVulnerabilities (
                    findingId: $findingId,
                    justification: $justification,
                    otherJustification: $otherJustification,
                    vulnerabilities: $vulnerabilities,
                ) {
                    success
                }
            }
        """

    variables: dict[str, Any] = {
        "findingId": finding,
        "justification": justification,
        "otherJustification": other_justification,
        "vulnerabilities": [vulnerability],
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
