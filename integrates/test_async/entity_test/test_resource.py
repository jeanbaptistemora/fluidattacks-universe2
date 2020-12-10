from tempfile import NamedTemporaryFile
import json
import os
from datetime import datetime, timedelta
import pytest

from ariadne import graphql, graphql_sync
from jose import jwt
from starlette.datastructures import UploadFile

from backend import util
from backend.api.dataloaders.group import GroupLoader
from backend.api.schema import SCHEMA
from test_async.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


async def _get_result(data):
    """Get result."""
    request = await create_dummy_session('integratesmanager@gmail.com')
    _, result = await graphql(SCHEMA, data, context_value=request)
    return result

async def test_get_resources():
    """Check for project resources"""
    query = '''{
      resources(projectName: "unittesting"){
        projectName
        environments
        files
        __typename
      }
    }'''
    data = {'query': query}
    request = await create_dummy_session('integratesmanager@gmail.com')
    request.loaders = {
        'group': GroupLoader(),
    }
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert 'resources' in result['data']
    assert result['data']['resources']['projectName'] == 'unittesting'
    assert 'test.zip' in result['data']['resources']['files']
    assert 'shell.exe' in result['data']['resources']['files']
    assert 'shell2.exe' in result['data']['resources']['files']
    assert 'asdasd.py' in result['data']['resources']['files']
    assert 'https%3A%2F%2Ffluidattacks.com%2F' in \
        result['data']['resources']['environments']

@pytest.mark.changes_db
async def test_add_environments():
    """Check for addEnvironments mutation."""
    query = '''mutation {
      addEnvironments(projectName: "unittesting", envs: [
        {urlEnv: "https://integrates.fluidattacks.com/test"},
        {urlEnv: "https://fluidattacks.com/test"},
      ]) {
        success
      }
    }'''
    data = {'query': query}
    result = await _get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addEnvironments']
    assert result['data']['addEnvironments']['success']

@pytest.mark.changes_db
async def test_add_files():
    """Check for addFiles mutation."""
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../mock/test-anim.gif')
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
            'projectName': 'UNITTESTING'
        }
    data = {'query': query, 'variables': variables}
    result = await _get_result(data)
    if 'errors' not in result:
        assert 'errors' not in result
        assert 'success' in result['data']['addFiles']
        assert result['data']['addFiles']['success']
    else:
        pytest.skip("Expected error")

@pytest.mark.changes_db
async def test_download_file():
    """Check for downloadFile mutation."""
    query = '''
        mutation {
          downloadFile (
            filesData: \"\\\"unittesting-422286126.yaml\\\"\",
            projectName: "unittesting") {
              success
              url
            }
        }
    '''
    data = {'query': query}
    result = await _get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['downloadFile']
    assert result['data']['downloadFile']['success']
    assert 'url' in result['data']['downloadFile']

@pytest.mark.changes_db
async def test_remove_files():
    """Check for removeFiles mutation."""
    file_data = {
        'description': 'test',
        'fileName': 'shell.exe',
        'uploadDate': ''
    }
    query = '''
        mutation RemoveFileMutation($filesData: JSONString!, $projectName: String!) {
            removeFiles(filesData: $filesData, projectName: $projectName) {
            success
            }
        }
    '''
    variables = {
        'filesData': json.dumps(file_data),
        'projectName': 'UNITTESTING'
    }
    data = {'query': query, 'variables': variables}
    result = await _get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['removeFiles']
    assert result['data']['removeFiles']['success']

@pytest.mark.changes_db
async def test_update_environment():
    """Check for updateEnvironment mutation."""
    query = '''mutation {
      updateEnvironment(projectName: "unittesting", state: INACTIVE, env: {
        urlEnv: "https://unittesting.fluidattacks.com/"
      }) {
        success
      }
    }'''
    data = {'query': query}
    result = await _get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['updateEnvironment']
    assert result['data']['updateEnvironment']['success']
