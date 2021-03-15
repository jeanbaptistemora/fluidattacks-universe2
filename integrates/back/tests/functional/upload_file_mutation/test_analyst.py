# Standard libraries
import os
import pytest

# Third party libraries
from starlette.datastructures import UploadFile

# Local libraries
from backend.api import get_new_context
from back.tests.functional.utils import (
    get_graphql_result,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('upload_file_mutation')
async def test_analyst(populate: bool):
    assert populate
    context = get_new_context()
    user: str = 'analyst@gmail.com'
    finding: str = '475041513'
    path = os.path.dirname(os.path.abspath(__file__))
    filename: str = f'{path}/test-vulns.yaml'
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, 'text/x-yaml')
        query = '''
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
        '''
        variables = {
            'file': uploaded_file,
            'findingId': finding,
        }
        data = {'query': query, 'variables': variables}
        result = await get_graphql_result(
            data,
            stakeholder=user,
            context=context,
        )
    assert 'errors' not in result
    assert result['data']['uploadFile']['success']
