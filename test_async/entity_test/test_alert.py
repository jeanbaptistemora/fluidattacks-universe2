import pytest
from datetime import datetime, timedelta

from ariadne import graphql, graphql_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend import util
from backend.api.schema import SCHEMA

pytestmark = pytest.mark.asyncio


class AlertTests(TestCase):

    def create_dummy_session(self):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'integratesuser@gmail.com'
        request.session['company'] = 'unittest'
        payload = {
            'user_email': 'unittest',
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

    async def test_get_alert(self):
        """Check for project alert"""
        query = '''{
            alert(projectName:"unittesting", organization:"fluid"){
                message
                __typename
            }
        }'''
        data = {'query': query}
        request = self.create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        if 'alert' in result['data']:
            message = result['data']['alert']['message']
            assert message == 'unittest'
        assert 'alert' in result['data']

    @pytest.mark.changes_db
    async def test_set_alert(self):
        """Check for set_alert mutation."""
        query = '''
            mutation {
                setAlert(company: "fluid", message: "Test", projectName: "unittesting") {
                    success
                }
            }
        '''
        data = {'query': query}
        request = self.create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['setAlert']
