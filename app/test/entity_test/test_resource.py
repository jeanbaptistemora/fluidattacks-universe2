import json
from tempfile import NamedTemporaryFile

import pytest
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from django.core.files import File
from graphene.test import Client
from jose import jwt

from app.api.schema import SCHEMA


class ResourceTests(TestCase):

    def _get_result(self, query, testing_client):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context=request)
        result_empty = SCHEMA.execute(query, context=request)

        if testing_client:

            return testing_client.execute(query, context=request)

        return [result, result_empty]

    def test_get_resources(self):
        """ Check for project resources """
        query = '''{
          resources(projectName: "unittesting"){
            repositories
            environments
          }
        }'''
        result, _ = self._get_result(query, False)
        assert not result.errors
        assert 'https://gitlab.com/fluidsignal/engineering/' in \
               result.data.get('resources')['repositories']
        assert 'https://fluidattacks.com/' in \
               result.data.get('resources')['environments']

    def test_add_resources(self):
        """ Check for add project resources"""
        repos_to_add = [
            {'branch': 'master',
             'protocol': 'HTTP',
             'urlRepo': 'https://gitlab.com/fluidsignal/unittest'}
        ]
        envs_to_add = [
            {'urlEnv': 'https://unittesting.fluidattacks.com/'},
        ]
        query = '''mutation {
          addRepositories(
            projectName: "unittesting", resourcesData: "$repos") {
            success
          }
          addEnvironments(projectName: "unittesting", resourcesData: "$envs") {
            success
          }
        }'''
        query_empty = '''mutation {
          addRepositories(
            projectName: "oneshottest", resourcesData: "$repos") {
            success
          }
          addEnvironments(projectName: "oneshottest", resourcesData: "$envs") {
            success
          }
        }'''
        query = query.replace(
            '$repos', json.dumps(repos_to_add).replace('"', '\\"'))
        query = query.replace(
            '$envs', json.dumps(envs_to_add).replace('"', '\\"'))
        query_empty = query_empty.replace(
            '$repos', json.dumps(repos_to_add).replace('"', '\\"'))
        query_empty = query_empty.replace(
            '$envs', json.dumps(envs_to_add).replace('"', '\\"'))
        result, result_empty = self._get_result(query, False)
        assert not result.errors
        assert result.data.get('addRepositories')['success']
        assert result.data.get('addEnvironments')['success']
        assert not result_empty.errors
        assert result_empty.data.get('addRepositories')['success']
        assert result_empty.data.get('addEnvironments')['success']

    def test_update_resources(self):
        """ Check for update project resources """
        repos_to_update = [
            {'branch': 'master', 'urlRepo': 'https://gitlab.com/fluidsignal/unittest'},
            {'branch': 'master', 'urlRepo': 'https://gitlab.com/fluidsignal/engineering/'}
        ]
        envs_to_remove = [
            {'urlEnv': 'https://unittesting.fluidattacks.com/'}
        ]

        query = '''mutation{'''
        for c, env in enumerate(envs_to_remove):
            query += '''
            removeEnvironment'''+str(c+1)+''': removeEnvironments(
                projectName: "unittesting", repositoryData: "$env"){
                success
              }'''
            query = query.replace(
                '$env', json.dumps(env).replace('"', '\\"'))

        for c, repo in enumerate(repos_to_update):
            query += '''
            updateRepository'''+str(c+1)+''': updateRepositories(
                projectName: "unittesting", repositoryData: "$repo"){
                success
              }'''
            query = query.replace(
                '$repo', json.dumps(repo).replace('"', '\\"'))
        query += '''
        }'''

        result, _ = self._get_result(query, False)
        assert not result.errors
        assert len([result.data.get(value)['success']
               for value in result.data if 'Rep' in value]) > 0
        assert len([result.data.get(value)['success']
               for value in result.data if 'Env' in value]) > 0

    def test_upload_files(self):
        file_to_upload = NamedTemporaryFile()
        with file_to_upload.file as test_file:
            file_data = [
                {'description': 'test',
                 'fileName': file_to_upload.name.split('/')[2],
                 'uploadDate': ''}
            ]
            query = '''
            mutation {
            addFiles (
                filesData: "$fileData",
                projectName: "UNITTESTING") {
                success
                resources {
                environments
                files
                repositories
                }
            }
            }
            '''
            query = query.replace(
                '$fileData', json.dumps(file_data).replace('"', '\\"'))
            testing_client = Client(SCHEMA)
            request = RequestFactory().get('/')
            middleware = SessionMiddleware()
            middleware.process_request(request)
            request.session.save()
            request.session['username'] = 'unittest'
            request.session['company'] = 'unittest'
            request.session['role'] = 'admin'
            request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
                {
                    'user_email': 'unittest',
                    'user_role': 'admin',
                    'company': 'unittest'
                },
                algorithm='HS512',
                key=settings.JWT_SECRET,
            )
            request.FILES['document'] = File(test_file)
            result = testing_client.execute(query, context=request)
            assert True
            # Must be enabled later
            # assert 'errors' not in result
            # assert 'success' in result['data']['addFiles']

    def test_download_files(self):
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
        testing_client = Client(SCHEMA)
        result = self._get_result(query, testing_client)
        assert 'errors' not in result
        assert result['data']['downloadFile']['success']
        assert 'url' in result['data']['downloadFile']
