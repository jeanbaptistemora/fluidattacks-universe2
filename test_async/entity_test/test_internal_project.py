import pytest
from datetime import datetime, timedelta

from ariadne import graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend import util
from backend.api.schema import SCHEMA
from test_async.utils import create_dummy_session


class InternalProjectTests(TestCase):

    @pytest.mark.asyncio
    async def test_internal_project(self):
        """Check for internal project"""
        query = '''{
            internalProjectNames{
                projectName
                __typename
            }
        }'''
        data = {'query': query}
        request = create_dummy_session('integratesuser@gmail.com')
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'internalProjectNames' in result['data']
