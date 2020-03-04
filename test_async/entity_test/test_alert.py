from ariadne import graphql_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend.api.schema import SCHEMA


class AlertTests(TestCase):

    def test_get_alert(self):
        """Check for project alert"""
        query = '''{
            alert(project_name:"unittesting", organization:"fluid"){
                message
            }
        }'''
        data = {'query': query}
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
        _, result = graphql_sync(SCHEMA, data, context_value=request)
        if 'alert' in result['data']:
            message = result['data']['alert']['message']
            assert message == 'unittest'
        assert 'alert' in result['data']
