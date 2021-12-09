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
    finding: str,
    yaml_file_name: str,
) -> Dict[str, Any]:
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
        variables: Dict[str, Any] = {
            "file": uploaded_file,
            "findingId": finding,
        }
        data: Dict[str, Any] = {"query": query, "variables": variables}
        result: Dict[str, Any] = await get_graphql_result(
            data,
            stakeholder=user,
            context=get_new_context(),
        )
    return result
