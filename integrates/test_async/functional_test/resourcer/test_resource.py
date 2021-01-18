import json
import os
import pytest

from starlette.datastructures import UploadFile

from test_async.functional_test.resourcer.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_resource():
    group_name = 'unittesting'
    file_name = 'test.zip'
    query = f'''{{
        resources(projectName: "{group_name}"){{
            projectName
            environments
            files
            __typename
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert result['data']['resources']['projectName'] == 'unittesting'
    assert file_name in result['data']['resources']['files']
    assert 'shell.exe' in result['data']['resources']['files']
    assert 'shell2.exe' in result['data']['resources']['files']
    assert 'asdasd.py' in result['data']['resources']['files']
    assert 'https%3A%2F%2Fsomeoneatfluid.integrates.env.' in \
        result['data']['resources']['environments']
    assert 'https%3A%2F%2Fsomeoneatfluid2.integrates.env.' in \
        result['data']['resources']['environments']
    assert 'https%3A%2F%2Ffluidattacks.com%2F' in \
        result['data']['resources']['environments']
    assert 'https%3A%2F%2Funittesting.fluidattacks.com%2F' in \
        result['data']['resources']['environments']
    environments = json.loads(result['data']['resources']['environments'])
    files = json.loads(result['data']['resources']['files'])

    query = f'''
        mutation {{
            downloadFile (
                filesData: \"\\\"{file_name}\\\"\",
                projectName: "{group_name}"
            ) {{
                success
                url
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['downloadFile']
    assert result['data']['downloadFile']['success']
    assert 'url' in result['data']['downloadFile']

    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../../mock/test-anim.gif')
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, 'image/gif')
        file_data = [
            {'description': 'test',
                'fileName': test_file.name.split('/')[2],
                'uploadDate': ''}
        ]
        query = '''
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
        variables = {
            'file': uploaded_file,
            'filesData': json.dumps(file_data),
            'projectName': group_name
        }
    data = {'query': query, 'variables': variables}
    result = await get_result(data)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    query = '''
        mutation RemoveFileMutation($filesData: JSONString!, $projectName: String!) {
            removeFiles(filesData: $filesData, projectName: $projectName) {
                success
            }
        }
    '''
    file_data = {
        'description': '',
        'fileName': "",
        'uploadDate': ''
    }
    variables = {
        'filesData': json.dumps(file_data),
        'projectName': group_name
    }
    data = {'query': query, 'variables': variables}
    result = await get_result(data)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    query = f'''{{
        resources(projectName: "{group_name}"){{
            projectName
            environments
            files
            __typename
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert json.loads(result['data']['resources']['environments']) == environments
    assert json.loads(result['data']['resources']['files']) == files
