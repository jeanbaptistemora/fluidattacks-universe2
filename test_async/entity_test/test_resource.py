from tempfile import NamedTemporaryFile
import json
import os

from ariadne import graphql, graphql_sync
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend.api.schema import SCHEMA


class ResourceTests(TestCase):

    def _get_result(self, data):
        """Get result."""
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'user'
        request.session['company'] = 'fluid'
        request.session['role'] = 'customer'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesuser@gmail.com',
                'user_role': 'customer',
                'company': 'fluid'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = graphql_sync(SCHEMA, data, context_value=request)
        return result

    async def test_get_resources(self):
        """Check for project resources"""
        query = '''{
          resources(projectName: "unittesting"){
            repositories
            environments
          }
        }'''
        data = {'query': query}
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'user'
        request.session['company'] = 'fluid'
        request.session['role'] = 'customer'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesuser@gmail.com',
                'user_role': 'customer',
                'company': 'fluid'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'resources' in result['data']
        assert 'https://gitlab.com/fluidsignal/engineering/' in \
            result['data']['resources']['repositories']
        assert 'https://fluidattacks.com/' in \
            result['data']['resources']['environments']

    def test_add_repositories(self):
        """Check for addRepositories mutation."""
        query = '''mutation {
          addRepositories(projectName: "unittesting", repos: [
            {
              urlRepo: "https://gitlab.com/fluidattacks/integrates.git",
              branch: "master",
              protocol: "HTTPS"
            },
            {
              urlRepo: "git@gitlab.com:fluidattacks/serves.git",
              branch: "master",
              protocol: "SSH"
            },
            {
              urlRepo: "https://gitlab.com/fluidattacks/web.git",
              branch: "master",
              protocol: "HTTPS"
            }
          ]) {
            success
          }
        }'''
        data = {'query': query}
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['addRepositories']
        assert result['data']['addRepositories']['success']

    def test_add_environments(self):
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
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['addEnvironments']
        assert result['data']['addEnvironments']['success']

    def test_add_files(self):
        """Check for addFiles mutation."""
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../../test/mock/test-anim.gif')
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
        result = self._get_result(data)
        assert 'errors' not in result
        assert 'success' in result['data']['addFiles']
        assert result['data']['addFiles']['success']
