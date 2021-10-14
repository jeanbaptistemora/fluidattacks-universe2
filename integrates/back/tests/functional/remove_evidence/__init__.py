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
    finding: str,
    evidence: str,
) -> Dict[str, Any]:
    variables: Dict[str, str] = {"evidenceId": evidence, "findingId": finding}
    query: str = """
        mutation removeEvidenceMutation(
            $evidenceId: EvidenceType!, $findingId: String!
        ) {
            removeEvidence(
                evidenceId: $evidenceId, findingId: $findingId
            ) {
                finding {
                    evidence
                }
                success
            }
        }
    """
    data: Dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
