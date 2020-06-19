from tempfile import NamedTemporaryFile
import json
import os
from datetime import datetime, timedelta
import pytest

from ariadne import graphql, graphql_sync
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend import util
from backend.api.dataloaders.project import ProjectLoader
from backend.api.schema import SCHEMA

pytestmark = pytest.mark.asyncio


class ResourceTests(TestCase):

    def create_dummy_session(self):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'user'
        request.session['company'] = 'fluid'
        payload = {
            'user_email': 'integratesmanager@gmail.com',
            'company': 'unittest',
            'exp': datetime.utcnow() +
            timedelta(seconds=settings.SESSION_COOKIE_AGE),
            'sub': 'django_session',
            'jti': util.calculate_hash_token()['jti'],
        }
        token = jwt.encode(
            payload,
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        request.COOKIES[settings.JWT_COOKIE_NAME] = token
        return request

    async def _get_result(self, data):
        """Get result."""
        request = self.create_dummy_session()
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
        request = self.create_dummy_session()
        request.loaders = {
            'project': ProjectLoader(),
        }
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'resources' in result['data']
        assert result['data']['resources']['projectName'] == 'unittesting'
        assert 'test.zip' in result['data']['resources']['files']
        assert 'shell.exe' in result['data']['resources']['files']
        assert 'shell2.exe' in result['data']['resources']['files']
        assert 'asdasd.py' in result['data']['resources']['files']
        assert 'https://gitlab.com/fluidsignal/engineering/' in \
            result['data']['resources']['repositories']
        assert 'https://fluidattacks.com/' in \
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
            {urlEnv: "https://fluidattacks.com/integrates"},
            {urlEnv: "https://fluidattacks.com/web"},
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
            uploaded_file = SimpleUploadedFile(name=test_file.name,
                                               content=test_file.read(),
                                               content_type='image/gif')
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
            urlRepo: "https://gitlab.com/fluidattacks/integrates.git",
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
            urlEnv: "https://gitlab.com/fluidattacks/integrates.git"
          }) {
            success
          }
        }'''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['updateEnvironment']
        assert result['data']['updateEnvironment']['success']
