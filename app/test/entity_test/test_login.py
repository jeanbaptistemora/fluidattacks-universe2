import pytest

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphene.test import Client
from jose import jwt

from app.api.schema import SCHEMA


@pytest.mark.usefixtures(
    'create_users_table',
    'create_projects_table',
    'create_project_access_table')
class LoginTests(TestCase):

    def test_get_login(self):
        testing_client = Client(SCHEMA)
        query = '''
            {
              login {
              authorized
              remember
              }
            }
        '''
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
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert result['data']['login']['authorized']
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'no existing user',
                'user_role': 'admin',
                'company': 'no company'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert not result['data']['login']['authorized']

    def test_accept_legal(self):
        testing_client = Client(SCHEMA)
        query = '''
            mutation {
              acceptLegal(remember: true){
                success
              }
            }
        '''
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
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert result['data']['acceptLegal']['success']
