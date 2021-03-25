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
    group: str,
) -> Dict[str, Any]:
    path: str = os.path.dirname(os.path.abspath(__file__))
    filename: str = 'test-anim.gif'
    file_path: str = f'{path}/{filename}'
    result: Dict[str, Any] = []
    with open(file_path, 'rb') as test_file:
        uploaded_file: UploadFile = UploadFile(filename, test_file, 'image/gif')
        file_data: Dict[str, str] = [
            {'description': 'test',
                'fileName': filename,
                'uploadDate': ''}
        ]
        query: str = '''
            mutation UploadFileMutation(
                $file: Upload!, $filesData: JSONString!, $projectName: String!
            ) {
                addFiles (
                    file: $file,
                    filesData: $filesData,
                    projectName: $projectName) {
                        success
                }
            }
        '''
        variables: Dict[str, Any] = {
            'file': uploaded_file,
            'filesData': json.dumps(file_data),
            'projectName': group
        }
        data: Dict[str, Any] = {'query': query, 'variables': variables}
        result = await get_graphql_result(
            data,
            stakeholder=user,
            context=get_new_context(),
        )
    return result
