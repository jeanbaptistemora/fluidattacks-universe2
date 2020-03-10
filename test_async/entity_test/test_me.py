from datetime import datetime, timedelta

from ariadne import graphql_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend.api.schema import SCHEMA


class MeTests(TestCase):

    def test_me(self):
        """Check Me query"""
        query = '''{
            me {
                role
                projects {
                    name
                    description
                }
            }
        }'''
        data = {'query': query}
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
        _, result = graphql_sync(SCHEMA, data, context_value=request)
        assert 'me' in result['data']
        assert 'role' in result['data']['me']
        assert result['data']['me']['role'] == 'admin'
        assert 'projects' in result['data']['me']

    def test_sign_in(self):
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
        _, result = graphql_sync(SCHEMA, data, context_value=request)
        assert 'errors' in result
        assert result['errors'][0]['message'] == 'INVALID_AUTH_TOKEN'

    def test_update_access_token(self):
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
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest',
                'first_name': 'Admin',
                'last_name': 'At Fluid'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = graphql_sync(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'updateAccessToken' in result['data']
        assert 'success' in result['data']['updateAccessToken']

    def test_invalidate_access_token(self):
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
        _, result = graphql_sync(SCHEMA, data, context_value=request)
        assert 'invalidateAccessToken' in result['data']
        assert 'success' in result['data']['invalidateAccessToken']

    def test_accept_legal(self):
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
        _, result = graphql_sync(SCHEMA, data, context_value=request)
        assert 'acceptLegal' in result['data']
        assert 'success' in result['data']['acceptLegal']
