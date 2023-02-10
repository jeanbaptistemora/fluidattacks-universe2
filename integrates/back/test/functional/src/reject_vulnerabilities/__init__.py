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


async def get_result(
    *,
    user: str,
    finding: str,
    vulnerability: str,
    reasons: list[str],
    other_reason: Optional[str],
) -> dict[str, Any]:
    query: str = """
            mutation RejectVulnerabilities(
                $findingId: String!,
                $reasons: [VulnerabilityRejectionReason!]!,
                $otherReason: String,
                $vulnerabilities: [String!]!
            ) {
                rejectVulnerabilities (
                    findingId: $findingId,
                    reasons: $reasons,
                    otherReason: $otherReason,
                    vulnerabilities: $vulnerabilities,
                ) {
                    success
                }
            }
        """

    variables: dict[str, Any] = {
        "findingId": finding,
        "reasons": reasons,
        "otherReason": other_reason,
        "vulnerabilities": [vulnerability],
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
