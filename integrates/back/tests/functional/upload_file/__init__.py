# Standard libraries
import json
import os
from typing import (
    Any,
    Dict,
)

# Third party libraries
from starlette.datastructures import (
    UploadFile,
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
    filename: str = f'{path}/test-vulns.yaml'
    with open(filename, 'rb') as test_file:
        uploaded_file: UploadFile = UploadFile(test_file.name, test_file, 'text/x-yaml')
        variables: Dict[str, Any] = {
            'file': uploaded_file,
            'findingId': finding,
        }
        data: Dict[str, Any] = {'query': query, 'variables': variables}
        result: Dict[str, Any] = await get_graphql_result(
            data,
            stakeholder=user,
            context=get_new_context(),
        )
    return result
