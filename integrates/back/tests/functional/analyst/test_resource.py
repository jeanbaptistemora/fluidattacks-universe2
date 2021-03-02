# Standard libraries
import json
import os
import pytest

# Third party libraries
from starlette.datastructures import UploadFile

# Local libraries
from backend.api import get_new_context
from test_functional.analyst.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_resource():
    context = get_new_context()
    group_name = 'unittesting'
    file_name = 'test.zip'
    query = f'''{{
        resources(projectName: "{group_name}"){{
            projectName
            files
            __typename
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert result['data']['resources']['projectName'] == 'unittesting'
    assert file_name in result['data']['resources']['files']
    assert 'shell.exe' in result['data']['resources']['files']
    assert 'shell2.exe' in result['data']['resources']['files']
    assert 'asdasd.py' in result['data']['resources']['files']
    files = json.loads(result['data']['resources']['files'])

    context = get_new_context()
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
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['downloadFile']
    assert result['data']['downloadFile']['success']
    assert 'url' in result['data']['downloadFile']

    context = get_new_context()
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../../test_unit/mock/test-anim.gif')
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
    result = await get_result(data, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    context = get_new_context()
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
    result = await get_result(data, context=context)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    context = get_new_context()
    query = f'''{{
        resources(projectName: "{group_name}"){{
            projectName
            files
            __typename
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data, context=context)
    assert json.loads(result['data']['resources']['files']) == files
