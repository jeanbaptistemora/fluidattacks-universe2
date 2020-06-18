from datetime import datetime, timedelta
import pytest

from ariadne import graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend import util
from backend.api.schema import SCHEMA

pytestmark = pytest.mark.asyncio


class CacheTests(TestCase):

    def create_dummy_session(self):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
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

    @pytest.mark.changes_db
    async def test_invalidate_cache(self):
        """Check for invalidate_cache mutation."""
        query = '''
            mutation {
                invalidateCache(pattern: "unittest") {
                    success
                }
            }
        '''
        data = {'query': query}
        request = self.create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['invalidateCache']
