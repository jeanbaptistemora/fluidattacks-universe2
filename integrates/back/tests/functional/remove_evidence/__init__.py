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
    finding: str,
    evidence: str,
) -> Dict[str, Any]:
    variables: Dict[str, str] = {
            'evidenceId': evidence,
            'findingId': finding
    }
    query: str = '''
        mutation removeEvidenceMutation(
            $evidenceId: EvidenceType!, $findingId: String!
        ) {
            removeEvidence(
                evidenceId: $evidenceId, findingId: $findingId
            ) {
                success
            }
        }
    '''
    data: Dict[str, Any] = {
        'query': query,
        'variables': variables
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
