from ariadne import graphql_sync, graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend.api.schema import SCHEMA
from backend.api.dataloaders.event import EventLoader


class EventTests(TestCase):

    def test_event(self):
        """Check for event."""
        query = '''{
            event(identifier: "418900971"){
                projectName
                detail
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
        assert 'event' in result['data']
        assert result['data']['event']['projectName'] == 'unittesting'
        assert result['data']['event']['detail'] == 'Integrates unit test'

    async def test_events(self):
        """Check for events."""
        query = '''{
            events(projectName: "unittesting"){
                projectName
                detail
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
        request.loaders = {'event': EventLoader()}
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'events' in result['data']
        assert result['data']['events'][0]['projectName'] == 'unittesting'
        assert len(result['data']['events'][0]['detail']) >= 1
