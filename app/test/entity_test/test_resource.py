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


@pytest.mark.usefixtures(
    'create_users_table',
    'create_projects_table',
    'create_project_access_table')
class ResourceTests(TestCase):

    def test_get_resources(self):
        """ Check for project resources """
        query = '''{
          resources(projectName: "unittesting"){
            repositories
            environments
          }
        }'''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context_value=request)
        assert not result.errors
        assert 'https://gitlab.com/fluidsignal/engineering/' in \
               result.data.get('resources')['repositories']
        assert 'https://fluidattacks.com/' in \
               result.data.get('resources')['environments']

    def test_add_resources(self):
        """ Check for add project resources"""
        repos_to_add = [
            {'branch': 'master',
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
        query = query.replace(
            '$repos', json.dumps(repos_to_add).replace('"', '\\"'))
        query = query.replace(
            '$envs', json.dumps(envs_to_add).replace('"', '\\"'))
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context_value=request)
        assert not result.errors
        assert result.data.get('addRepositories')['success']
        assert result.data.get('addEnvironments')['success']

    def test_remove_resources(self):
        """ Check for remove project resources """
        repo_to_remove = {
            'branch': 'master',
            'urlRepo': 'https://gitlab.com/fluidsignal/unittest'}
        env_to_remove = {'urlEnv': 'https://unittesting.fluidattacks.com/'}
        query = '''mutation{
          removeRepositories(
            projectName: "unittesting", repositoryData: "$repo"){
            success
          }
          removeEnvironments(
            projectName: "unittesting", repositoryData: "$env"){
            success
          }
        }'''
        query = query.replace(
            '$repo', json.dumps(repo_to_remove).replace('"', '\\"'))
        query = query.replace(
            '$env', json.dumps(env_to_remove).replace('"', '\\"'))
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context_value=request)
        assert not result.errors
        assert result.data.get('removeRepositories')['success']
        assert result.data.get('removeEnvironments')['success']

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
            result = testing_client.execute(query, context_value=request)
            assert 'errors' not in result
            assert 'success' in result['data']['addFiles']
