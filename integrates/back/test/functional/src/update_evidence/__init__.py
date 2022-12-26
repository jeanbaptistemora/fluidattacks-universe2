# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
import os
from starlette.datastructures import (
    UploadFile,
)


async def get_result(
    *, user: str, finding_id: str, should_use_invalid: bool = False
) -> dict:
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
    filename: str
    uploaded_file: UploadFile
    variables: dict
    data: dict
    result: dict
    path: str = os.path.dirname(os.path.abspath(__file__))
    if should_use_invalid:
        filename = f"{path}/test-anim.gif"
        with open(filename, "rb") as test_file:
            uploaded_file = UploadFile(
                "orgtest-group1-0123456789.gif", test_file, "image/gif"
            )
            variables = {
                "evidenceId": "ANIMATION",
                "findingId": finding_id,
                "file": uploaded_file,
            }
            data = {"query": query, "variables": variables}
            result = await get_graphql_result(
                data,
                stakeholder=user,
                context=get_new_context(),
            )

        return result

    filename = f"{path}/test-anim.webm"
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "orgtest-group1-0123456789.webm", test_file, "video/webm"
        )
        variables = {
            "evidenceId": "ANIMATION",
            "findingId": finding_id,
            "file": uploaded_file,
        }
        data = {"query": query, "variables": variables}
        result = await get_graphql_result(
            data,
            stakeholder=user,
            context=get_new_context(),
        )

    return result
