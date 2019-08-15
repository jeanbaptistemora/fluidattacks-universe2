from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphene.test import Client
from jose import jwt

from app.api.schema import SCHEMA


class ProjectEntityTests(TestCase):

    def test_get_resources(self):
        """ Check for project resources """
        query = '''
          query {
            project(projectName: "detailedtest"){
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
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert 'totalFindings' in result['data']['project']
