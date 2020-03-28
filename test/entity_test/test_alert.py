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
            alert(projectName:"unittesting", organization:"fluid"){
                message
            }
        }'''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context_value=request)
        if 'alert' in result.data:
            message = result.data['alert']['message']
            assert message == 'unittest'
        assert 'alert' in result.data
