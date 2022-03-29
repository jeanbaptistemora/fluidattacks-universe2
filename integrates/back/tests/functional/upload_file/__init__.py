# pylint: disable=import-error
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
)


async def get_result(
    *,
    user: str,
    finding: str,
    yaml_file_name: str,
) -> dict[str, Any]:
    query: str = """
            mutation UploadFileMutation(
                $file: Upload!, $findingId: String!
            ) {
                uploadFile (
                    file: $file,
                    findingId: $findingId
                ) {
                    success
                }
            }
        """
    path: str = os.path.dirname(os.path.abspath(__file__))
    filename: str = f"{path}/{yaml_file_name}"
    with open(filename, "rb") as test_file:
        uploaded_file: UploadFile = UploadFile(
            test_file.name, test_file, "text/x-yaml"
        )
        variables: dict[str, Any] = {
            "file": uploaded_file,
            "findingId": finding,
        }
        data: dict[str, Any] = {"query": query, "variables": variables}
        result: dict[str, Any] = await get_graphql_result(
            data,
            stakeholder=user,
            context=get_new_context(),
        )
    return result
