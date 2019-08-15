from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt

from app.api.schema import SCHEMA


class EventTests(TestCase):

    def test_get_event(self):
        """Check for eventuality"""
        query = '''{
            event(identifier:"418900971"){
                detail
            }
        }'''
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
        result = dict(SCHEMA.execute(query, context_value=request).data)
        if 'event' in result.keys():
            detail = dict(result['event'])['detail']
            assert detail == 'Integrates unit test'
        assert 'event' in result

class TestGetEvents(TestCase):

    def test_get_events(self):
        """Check for eventualities"""
        query = '''{
            events(projectName:"unittesting"){
                detail
            }
        }'''
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
        result = dict(SCHEMA.execute(query, context_value=request).data)
        if 'events' in result:
            detail = dict(result['events'][0])['detail']
            assert len(detail) >= 1
        assert 'events' in result
