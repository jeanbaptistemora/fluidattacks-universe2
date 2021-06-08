from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
import os
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    Dict,
)


async def get_result(
    *,
    user: str,
    draft: str,
) -> Dict[str, Any]:
    query: str = """
        mutation UpdateEvidenceMutation(
            $evidenceId: EvidenceType!, $file: Upload!, $findingId: String!
        ) {
            updateEvidence(
                evidenceId: $evidenceId, file: $file, findingId: $findingId
            ) {
                success
            }
        }
    """
    path: str = os.path.dirname(os.path.abspath(__file__))
    filename: str = f"{path}/test-anim.gif"
    with open(filename, "rb") as test_file:
        uploaded_file: UploadFile = UploadFile(
            test_file.name, test_file, "image/gif"
        )
        variables: Dict[str, Any] = {
            "evidenceId": "ANIMATION",
            "findingId": draft,
            "file": uploaded_file,
        }
        data: Dict[str, Any] = {"query": query, "variables": variables}
        result: Dict[str, Any] = await get_graphql_result(
            data,
            stakeholder=user,
            context=get_new_context(),
        )
    return result
