from collections import OrderedDict

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphene.test import Client
from jose import jwt

from api.dataloaders.finding import FindingLoader
from api.schema import SCHEMA


class ProjectEntityTests(TestCase):

    def test_get_project(self):
        """ Check for project resources """
        query = '''
          query {
            project(projectName: "unittesting"){
              name,
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
        assert result['data']['project']['lastClosingVuln'] == 23
