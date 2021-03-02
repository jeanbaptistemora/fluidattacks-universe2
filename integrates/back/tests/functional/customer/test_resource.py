# Local libraries
import json
import os
import pytest

# Third party libraries
from starlette.datastructures import UploadFile
from urllib.parse import quote

# Local libraries
from backend.api import get_new_context
from backend.utils import datetime as datetime_utils
from back.tests.functional.customer.utils import get_result


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('old')
async def test_resource():
    context = get_new_context()
    today = datetime_utils.get_as_str(
        datetime_utils.get_now(),
        date_format='%Y-%m-%d'
    )
    group_name = 'unittesting'

    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../../unit/mock/test-anim.gif')
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile('test-anim.gif', test_file, 'image/gif')
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
    assert 'errors' not in result
    assert 'success' in result['data']['addFiles']
    assert result['data']['addFiles']['success']

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
    files = json.loads(result['data']['resources']['files'])
    file = [file for file in files if file['uploadDate'][:-6] == today][0]
    assert file['uploader'] == 'integratescustomer@gmail.com'
    file_name = file['fileName']

    context = get_new_context()
    query = f'''
            mutation {{
              downloadFile (
                filesData: \"\\\"{file_name}\\\"\",
                projectName: "{group_name}") {{
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
    query = '''
        mutation RemoveFileMutation($filesData: JSONString!, $projectName: String!) {
            removeFiles(filesData: $filesData, projectName: $projectName) {
                success
            }
        }
    '''
    file_data = {
        'description': '',
        'fileName': file_name,
        'uploadDate': ''
    }
    variables = {
        'filesData': json.dumps(file_data),
        'projectName': group_name
    }
    data = {'query': query, 'variables': variables}
    result = await get_result(data, context=context)
    assert 'errors' not in result
    assert 'success' in result['data']['removeFiles']
    assert result['data']['removeFiles']['success']

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
    files = json.loads(result['data']['resources']['files'])
    today_files = [file for file in files if file['uploadDate'][:-6] == today]
    assert today_files == []
