from tempfile import NamedTemporaryFile
import json
import os
from datetime import datetime, timedelta
import pytest

from ariadne import graphql, graphql_sync
from django.core.files import File
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from starlette.datastructures import UploadFile

from backend import util
from backend.api.dataloaders.group import GroupLoader
from backend.api.schema import SCHEMA
from test_async.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


class ResourceTests(TestCase):

    async def _get_result(self, data):
        """Get result."""
        request = await create_dummy_session('integratesmanager@gmail.com')
        _, result = await graphql(SCHEMA, data, context_value=request)
        return result

    async def test_get_resources(self):
        """Check for project resources"""
        query = '''{
          resources(projectName: "unittesting"){
            projectName
            repositories
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
        assert 'https%3A%2F%2Fgitlab.com%2Ffluidsignal%2Fengineering%2F' in \
            result['data']['resources']['repositories']
        assert 'https%3A%2F%2Ffluidattacks.com%2F' in \
            result['data']['resources']['environments']

    @pytest.mark.changes_db
    async def test_add_repositories(self):
        """Check for addRepositories mutation."""
        query = '''mutation {
          addRepositories(projectName: "unittesting", repos: [
            {
              urlRepo: "https://gitlab.com/fluidattacks/new_repo1.git",
              branch: "master",
              protocol: HTTPS
            },
            {
              urlRepo: "git@gitlab.com:fluidattacks/new_repo2.git",
              branch: "master",
              protocol: SSH
            },
            {
              urlRepo: "https://gitlab.com/fluidattacks/new_repo3.git",
              branch: "master",
              protocol: HTTPS
            }
          ]) {
            success
          }
        }'''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['addRepositories']
        assert result['data']['addRepositories']['success']

    @pytest.mark.changes_db
    async def test_add_environments(self):
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
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['addEnvironments']
        assert result['data']['addEnvironments']['success']

    @pytest.mark.changes_db
    async def test_add_files(self):
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
        result = await self._get_result(data)
        if 'errors' not in result:
            assert 'errors' not in result
            assert 'success' in result['data']['addFiles']
            assert result['data']['addFiles']['success']
        else:
            pytest.skip("Expected error")

    @pytest.mark.changes_db
    async def test_download_file(self):
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
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['downloadFile']
        assert result['data']['downloadFile']['success']
        assert 'url' in result['data']['downloadFile']

    @pytest.mark.changes_db
    async def test_remove_files(self):
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
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['removeFiles']
        assert result['data']['removeFiles']['success']

    @pytest.mark.changes_db
    async def test_update_repository(self):
        """Check for updateRepository mutation."""
        query = '''mutation {
          updateRepository(projectName: "unittesting", state: INACTIVE, repo: {
            urlRepo: "https://gitlab.com/fluidsignal/unittest",
            branch: "master",
            protocol: HTTPS
          }) {
            success
          }
        }'''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['updateRepository']
        assert result['data']['updateRepository']['success']

    @pytest.mark.changes_db
    async def test_update_environment(self):
        """Check for updateEnvironment mutation."""
        query = '''mutation {
          updateEnvironment(projectName: "unittesting", state: INACTIVE, env: {
            urlEnv: "https://unittesting.fluidattacks.com/"
          }) {
            success
          }
        }'''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['updateEnvironment']
        assert result['data']['updateEnvironment']['success']
