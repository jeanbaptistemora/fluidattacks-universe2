from tempfile import NamedTemporaryFile
import json
import os

from ariadne import graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend.api.schema import SCHEMA


class ForcesExecutionsTests(TestCase):

    async def _get_result(self, data):
        """Get result."""
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesuser@gmail.com',
                'user_role': 'customer',
                'company': 'unittest',
                'first_name': 'unit',
                'last_name': 'test'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        return result

    async def test_project_name(self):
        """Check for project_name field"""
        query = '''{
          forcesExecutions(projectName: "unittesting"){
            projectName
          }
        }'''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert result['data']['forcesExecutions']['projectName'] \
            == 'unittesting'
