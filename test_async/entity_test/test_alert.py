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
from test_async.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


class AlertTests(TestCase):

    async def test_get_alert(self):
        """Check for project alert"""
        query = '''{
            alert(projectName:"unittesting", organization:"fluid"){
                message
                __typename
            }
        }'''
        data = {'query': query}
        request = create_dummy_session('integratesuser@gmail.com')
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
        request = create_dummy_session('unittest', 'fluid')
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['setAlert']
