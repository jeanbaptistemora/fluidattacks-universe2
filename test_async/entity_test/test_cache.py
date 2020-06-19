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
from test_async.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


class CacheTests(TestCase):

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
        request = create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['invalidateCache']
