import os
from collections import OrderedDict

import pytest
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphene.test import Client
from jose import jwt

from backend.api.schema import SCHEMA


class BreakBuildExecutionsTests(TestCase):

    def _get_result(self, query, testing_client):
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
        if testing_client:

            return testing_client.execute(query, context=request)

        return SCHEMA.execute(query, context=request)

    def test_project_name(self):
        valid_project_name = 'unittesting'
        query = f'''
          query {{
            breakBuildExecutions(
                projectName: "{valid_project_name}",
            ) {{
              projectName
            }}
          }}
        '''
        testing_client = Client(SCHEMA)
        result = self._get_result(query, testing_client)
        assert not result.get('errors')
        assert result['data']['breakBuildExecutions']['projectName'] \
            == valid_project_name
