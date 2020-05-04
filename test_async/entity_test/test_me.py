import pytest

from datetime import datetime, timedelta

from ariadne import graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend.api.dataloaders.project import ProjectLoader
from backend.api.schema import SCHEMA

pytestmark = pytest.mark.asyncio


class MeTests(TestCase):

    async def test_me(self):
        """Check Me query"""
        query = '''{
            me(callerOrigin: "API") {
                accessToken
                authorized
                projects {
                    name
                    description
                }
                tags {
                    name
                    projects {
                        name
                    }
                }
                remember
                role
                permissions
                callerOrigin
                __typename
            }
        }'''
        data = {'query': query}
        request = RequestFactory().get('/')
        request.loaders = {
            'project': ProjectLoader(),
        }
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'integratesmanager@gmail.com'
        request.session['company'] = 'fluid'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesmanager@gmail.com',
                'company': 'fluid'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'me' in result['data']
        assert 'role' in result['data']['me']
        assert result['data']['me']['role'] == 'admin'
        assert result['data']['me']['callerOrigin'] == 'API'
        assert 'projects' in result['data']['me']
        assert 'tags' in result['data']['me']
        for tag in result['data']['me']['tags']:
            assert 'name' in tag
            assert 'projects' in tag
        for project in result['data']['me']['projects']:
            assert 'name' in project
            assert 'description' in project

    async def test_sign_in(self):
        """Check for signIn mutation."""
        query = '''
            mutation {
                signIn(
                    authToken: "badtoken",
                    provider: "google",
                    pushToken: "badpushtoken"
                ) {
                    authorized
                    sessionJwt
                    success
                }
            }
        '''
        data = {'query': query}
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' in result
        assert result['errors'][0]['message'] == 'INVALID_AUTH_TOKEN'

    async def test_update_access_token(self):
        """Check for updateAccessToken mutation."""
        query = '''
            mutation updateAccessToken ($expirationTime: Int!) {
                updateAccessToken(expirationTime: $expirationTime) {
                    sessionJwt
                    success
                }
            }
        '''
        expiration_time = datetime.utcnow() + timedelta(weeks=8)
        expiration_time = int(expiration_time.timestamp())

        data = {
            'query': query,
            'variables': {
                'expirationTime': expiration_time
            }
        }
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'company': 'unittest',
                'first_name': 'Admin',
                'last_name': 'At Fluid'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'updateAccessToken' in result['data']
        assert 'success' in result['data']['updateAccessToken']

    async def test_invalidate_access_token(self):
        """Check invalidateAccessToken query"""
        query = '''
            mutation {
                invalidateAccessToken {
                    success
                }
            }
        '''
        data = {'query': query}
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'invalidateAccessToken' in result['data']
        assert 'success' in result['data']['invalidateAccessToken']

    async def test_accept_legal(self):
        """Check acceptLegal query"""
        query = '''
            mutation {
                acceptLegal(remember: true) {
                    success
                }
            }
        '''
        data = {'query': query}
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'acceptLegal' in result['data']
        assert 'success' in result['data']['acceptLegal']
