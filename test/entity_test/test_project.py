from collections import OrderedDict

import pytest
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphene.test import Client
from jose import jwt

from backend.api.dataloaders.finding import FindingLoader
from backend.api.schema import SCHEMA
from backend.exceptions import AlreadyPendingDeletion, NotPendingDeletion, PermissionDenied
from .test_utils import Request


class ProjectEntityTests(TestCase):

    def test_get_project(self):
        """ Check for project resources """
        query = '''
          query {
            project(projectName: "unittesting"){
              name,
              hasDrills,
              hasForces,
              hasIntegrates,
              totalFindings,
              description,
              subscription,
              lastClosingVuln,
            }
          }
        '''
        testing_client = Client(SCHEMA)
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
        request.loaders = {'finding': FindingLoader()}
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert result['data']['project']
        assert result['data']['project']['hasDrills'] == True
        assert result['data']['project']['hasForces'] == True
        assert result['data']['project']['hasIntegrates'] == True
        assert result['data']['project']['lastClosingVuln'] == 23

    def test_request_remove(self):
        query = '''
            mutation {{
                requestRemoveProject(projectName: "{project_name}") {{
                    success
              }}
            }}
        '''
        testing_client = Client(SCHEMA)
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'admin',
            'useremail': 'integratesmanager@gmail.com'
        })
        result = testing_client.execute(
            query.format(project_name='OneshottesT'),
            context_value=request
        )
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(PermissionDenied())
        result = testing_client.execute(
            query.format(project_name='pendingproject'),
            context_value=request
        )
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(AlreadyPendingDeletion())

    def test_reject_request_remove(self):
        query = '''
            mutation {{
                rejectRemoveProject(projectName: "{project_name}") {{
                    success
              }}
            }}
        '''
        testing_client = Client(SCHEMA)
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'admin',
            'useremail': 'integratesmanager@gmail.com'
        })
        result = testing_client.execute(
            query.format(project_name='PendingprojecT'),
            context_value=request
        )
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(PermissionDenied())
        result = testing_client.execute(
            query.format(project_name='unittesting'),
            context_value=request
        )
        assert 'errors' in result
        assert result['errors'][0]['message'] == str(NotPendingDeletion())
