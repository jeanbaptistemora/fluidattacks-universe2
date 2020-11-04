import json
import os
import pytest

from starlette.datastructures import UploadFile
from urllib.parse import quote

from backend.utils import datetime as datetime_utils
from test_async.functional_test.executive.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_resource():
    today = datetime_utils.get_as_str(
        datetime_utils.get_now(),
        date_format='%Y-%m-%d'
    )
    state_today = datetime_utils.get_as_str(
        datetime_utils.get_now(),
        date_format='%Y/%m/%d'
    )
    group_name = 'unittesting'
    url_env = 'https://url.env.executive.com'
    query = f'''mutation {{
        addEnvironments(projectName: "{group_name}", envs: [
            {{urlEnv: "{url_env}"}}
        ]) {{
            success
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addEnvironments']
    assert result['data']['addEnvironments']['success']

    url_repo = 'https://gitlab.com/fluidattacks/url_repo/executive.git'
    query = f'''mutation {{
        addRepositories(projectName: "{group_name}", repos: [
            {{
                urlRepo: "{url_repo}",
                branch: "master",
                protocol: HTTPS
            }}
        ]) {{
            success
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addRepositories']
    assert result['data']['addRepositories']['success']

    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../../mock/test-anim.gif')
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
        result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addFiles']
    assert result['data']['addFiles']['success']

    query = f'''{{
        resources(projectName: "{group_name}"){{
            projectName
            repositories
            environments
            files
            __typename
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    environments = json.loads(result['data']['resources']['environments'])
    env = [env for env in environments if env['urlEnv'] == quote(url_env, safe='')][0]
    assert today in env['historic_state'][0]['date']
    assert env['historic_state'][0]['state'] == 'ACTIVE'
    assert env['historic_state'][0]['user'] == 'integratesexecutive@gmail.com'
    repositories = json.loads(result['data']['resources']['repositories'])
    repo = [repo for repo in repositories if repo['urlRepo'] == quote(url_repo, safe='')][0]
    assert repo['branch'] == 'master'
    assert today in repo['historic_state'][0]['date']
    assert repo['historic_state'][0]['state'] == 'ACTIVE'
    assert repo['historic_state'][0]['user'] == 'integratesexecutive@gmail.com'
    assert repo['protocol'] == 'HTTPS'
    files = json.loads(result['data']['resources']['files'])
    file = [file for file in files if file['uploadDate'][:-6] == today][0]
    assert file['uploader'] == 'integratesexecutive@gmail.com'
    file_name = file['fileName']

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
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['downloadFile']
    assert result['data']['downloadFile']['success']
    assert 'url' in result['data']['downloadFile']

    query = f'''mutation {{
        updateEnvironment(projectName: "{group_name}", state: INACTIVE, env: {{
            urlEnv: "{url_env}"
        }}) {{
            success
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['updateEnvironment']
    assert result['data']['updateEnvironment']['success']

    query = f'''mutation {{
        updateRepository(projectName: "{group_name}", state: INACTIVE, repo: {{
            urlRepo: "{url_repo}",
            branch: "master",
            protocol: HTTPS
        }}) {{
            success
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['updateRepository']

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
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['removeFiles']
    assert result['data']['removeFiles']['success']

    query = f'''{{
        resources(projectName: "{group_name}"){{
            projectName
            repositories
            environments
            files
            __typename
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    environments = json.loads(result['data']['resources']['environments'])
    env = [env for env in environments if env['urlEnv'] == quote(url_env, safe='')][0]
    assert state_today in env['historic_state'][1]['date']
    assert env['historic_state'][1]['state'] == 'INACTIVE'
    assert env['historic_state'][1]['user'] == 'integratesexecutive@gmail.com'
    repositories = json.loads(result['data']['resources']['repositories'])
    repo = [repo for repo in repositories if repo['urlRepo'] == quote(url_repo, safe='')][0]
    assert repo['branch'] == 'master'
    assert state_today in repo['historic_state'][1]['date']
    assert repo['historic_state'][1]['state'] == 'INACTIVE'
    assert repo['historic_state'][1]['user'] == 'integratesexecutive@gmail.com'
    assert repo['protocol'] == 'HTTPS'
    files = json.loads(result['data']['resources']['files'])
    today_files = [file for file in files if file['uploadDate'][:-6] == today]
    assert today_files == []
