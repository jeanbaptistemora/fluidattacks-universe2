from ariadne import graphql, graphql_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend.api.schema import SCHEMA


class ResourceTests(TestCase):

    async def test_get_resources(self):
        """Check for project resources"""
        query = '''{
          resources(projectName: "unittesting"){
            repositories
            environments
          }
        }'''
        data = {'query': query}
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'user'
        request.session['company'] = 'fluid'
        request.session['role'] = 'customer'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesuser@gmail.com',
                'user_role': 'customer',
                'company': 'fluid'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'resources' in result['data']
        assert 'https://gitlab.com/fluidsignal/engineering/' in \
            result['data']['resources']['repositories']
        assert 'https://fluidattacks.com/' in \
            result['data']['resources']['environments']
