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
    evidence: str,
) -> dict[str, Any]:
    variables: dict[str, str] = {"evidenceId": evidence, "findingId": finding}
    query: str = """
        mutation removeEvidenceMutation(
            $evidenceId: EvidenceType!, $findingId: String!
        ) {
            removeEvidence(
                evidenceId: $evidenceId, findingId: $findingId
            ) {
                finding {
                    evidence {
                        evidence1 {
                            date
                            description
                            url
                        }
                    }
                }
                success
            }
        }
    """
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
