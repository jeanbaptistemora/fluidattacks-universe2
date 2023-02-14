# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def get_result(
    *,
    user: str,
    finding: str,
    vulnerability: str,
) -> dict[str, Any]:
    query: str = """
            mutation ConfirmVulnerabilities(
                $findingId: String!,
                $vulnerabilities: [String!]!
            ) {
                confirmVulnerabilities (
                    findingId: $findingId,
                    vulnerabilities: $vulnerabilities,
                ) {
                    success
                }
            }
        """
    variables: dict[str, Any] = {
        "findingId": finding,
        "vulnerabilities": [vulnerability],
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
