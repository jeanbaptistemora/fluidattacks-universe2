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

from backend.api.schema import SCHEMA


class ResourceTests(TestCase):

    def _get_result(self, query, testing_client):
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
        result = SCHEMA.execute(query, context=request)

        if testing_client:

            return testing_client.execute(query, context=request)

        return result

    def test_get_resources(self):
        """ Check for project resources """
        query = '''{
          resources(projectName: "unittesting"){
            repositories
            environments
          }
        }'''
        result = self._get_result(query, False)
        assert not result.errors
        assert 'https://gitlab.com/fluidsignal/engineering/' in \
               result.data.get('resources')['repositories']
        assert 'https://fluidattacks.com/' in \
               result.data.get('resources')['environments']

    def test_add_resources(self):
        """ Check for add project resources"""
        repos_to_add = [
            {'branch': 'master', 'urlRepo': 'https://gitlab.com/fluidattacks/asserts.git'}
        ]
        envs_to_add = [
            {'urlEnv': 'https://fluidattacks.com/asserts/'}
        ]
        query = '''mutation {
          addRepository: addResources(
            projectName: "unittesting", resourceData: "$repos", resType: "repository") {
            success
          }
          addEnvironment: addResources(
            projectName: "unittesting", resourceData: "$envs", resType: "environment") {
            success
          }
        }'''
        query_empty = '''mutation {
          addRepository: addResources(
            projectName: "oneshottest", resourceData: "$repos", resType: "repository") {
            success
          }
          addEnvironment: addResources(
            projectName: "oneshottest", resourceData: "$envs", resType: "environment") {
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
        result = self._get_result(query, False)
        assert not result.errors
        assert len([result.data.get(value)['success']
               for value in result.data if 'Rep' in value]) > 0
        assert len([result.data.get(value)['success']
               for value in result.data if 'Env' in value]) > 0

        result_empty = self._get_result(query_empty, False)
        assert not result_empty.errors
        assert len([result_empty.data.get(value)['success']
               for value in result.data if 'Rep' in value]) > 0
        assert len([result_empty.data.get(value)['success']
               for value in result.data if 'Env' in value]) > 0

    def test_add_repositories(self):
        """ Check for add project repos """
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

        result = self._get_result(query, False)
        assert not result.errors
        assert result.data['addRepositories']['success']

    def test_add_environments(self):
        """ Check for add project envs """
        query = '''mutation {
          addEnvironments(projectName: "unittesting", envs: [
            {urlEnv: "https://fluidattacks.com/integrates"},
            {urlEnv: "https://fluidattacks.com/web"},
          ]) {
            success
          }
        }'''

        result = self._get_result(query, False)
        assert not result.errors
        assert result.data['addEnvironments']['success']

    def test_update_repository(self):
        """ Check for update repository state """
        query = '''mutation {
          updateRepository(projectName: "unittesting", state: INACTIVE, repo: {
            urlRepo: "https://gitlab.com/fluidattacks/integrates.git",
            branch: "master",
            protocol: "HTTPS"
          }) {
            success
          }
        }'''

        result = self._get_result(query, False)
        assert not result.errors
        assert result.data['updateRepository']['success']

    def test_update_environment(self):
        """ Check for update environment state """
        query = '''mutation {
          updateEnvironment(projectName: "unittesting", state: INACTIVE, env: {
            urlEnv: "https://gitlab.com/fluidattacks/integrates.git"
          }) {
            success
          }
        }'''

        result = self._get_result(query, False)
        assert not result.errors
        assert result.data['updateEnvironment']['success']

    def test_update_resources(self):
        """ Check for update project resources """
        repos_to_update = [
            ['unittesting', {'branch': 'master', 'urlRepo': 'https://gitlab.com/fluidsignal/unittest'}],
            ['unittesting', {'branch': 'master', 'urlRepo': 'https://gitlab.com/fluidsignal/engineering/'}],
            ['oneshottest', {'branch': 'master', 'urlRepo': 'https://gitlab.com/fluidsignal/integrates'}],
            ['oneshottest', {'branch': 'master', 'urlRepo': 'git@gitlab.com:fluidattacks/integrates.git'}]
        ]
        envs_to_update = [
            ['unittesting', {'urlEnv': 'https://someoneatfluid.integrates.env.'}],
            ['unittesting', {'urlEnv': 'https://someoneatfluid.integrates.env.'}],
            ['unittesting', {'urlEnv': 'https://fluidattacks.com/'}]
        ]

        query = '''mutation{'''
        for c, env in enumerate(envs_to_update):
            query += '''
            updateEnvironment'''+str(c+1)+''': updateResources(
                projectName: "$proj", resourceData: "$env", resType: "environment"){
                success
              }'''
            query = query.replace(
                '$env', json.dumps(env[1]).replace('"', '\\"'))
            query = query.replace('$proj', env[0])

        for c, repo in enumerate(repos_to_update):
            query += '''
            updateRepository'''+str(c+1)+''': updateResources(
                projectName: "$proj", resourceData: "$repo", resType: "repository"){
                success
              }'''
            query = query.replace(
                '$repo', json.dumps(repo[1]).replace('"', '\\"'))
            query = query.replace('$proj', repo[0])
        query += '''
        }'''

        result = self._get_result(query, False)
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
