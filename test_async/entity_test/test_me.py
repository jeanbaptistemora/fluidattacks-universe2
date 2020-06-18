import pytest

from datetime import datetime, timedelta

from ariadne import graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend import util
from backend.api.dataloaders.project import ProjectLoader
from backend.api.schema import SCHEMA

pytestmark = pytest.mark.asyncio


class MeTests(TestCase):

    def create_dummy_session(self, username='unittest'):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = username
        request.session['company'] = 'unittest'
        payload = {
            'user_email': username,
            'company': 'unittest',
            'first_name': 'Admin',
            'last_name': 'At Fluid',
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

    async def test_me(self):
        """Check Me query"""
        query = '''{
            me(callerOrigin: "API") {
                accessToken
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
        request = self.create_dummy_session('integratesuser@gmail.com')
        request.loaders = {
            'project': ProjectLoader(),
        }
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'me' in result['data']
        assert 'role' in result['data']['me']
        assert result['data']['me']['role'] == 'internal_manager'
        assert result['data']['me']['callerOrigin'] == 'API'
        assert 'projects' in result['data']['me']
        assert 'tags' in result['data']['me']
        for tag in result['data']['me']['tags']:
            assert 'name' in tag
            assert 'projects' in tag
            if tag['name'] == 'test-projects':
                expected_prjs = ['unittesting', 'oneshottest']
                output = [proj['name'] for proj in tag['projects']]
                assert sorted(output) == sorted(expected_prjs)
        for project in result['data']['me']['projects']:
            assert 'name' in project
            assert 'description' in project

    @pytest.mark.changes_db
    async def test_sign_in(self):
        """Check for signIn mutation."""
        query = '''
            mutation {
                signIn(
                    authToken: "badtoken",
                    provider: GOOGLE
                ) {
                    sessionJwt
                    success
                }
            }
        '''
        data = {'query': query}
        request = self.create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert not result['data']['signIn']['success']

    @pytest.mark.changes_db
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
        request = self.create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'updateAccessToken' in result['data']
        assert 'success' in result['data']['updateAccessToken']

    @pytest.mark.changes_db
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
        request = self.create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'invalidateAccessToken' in result['data']
        assert 'success' in result['data']['invalidateAccessToken']

    @pytest.mark.changes_db
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
        request = self.create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'acceptLegal' in result['data']
        assert 'success' in result['data']['acceptLegal']
