from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphene.test import Client
from jose import jwt

from app.api.dataloaders.event import EventLoader
from app.api.schema import SCHEMA


class EventTests(TestCase):

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
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        request.loaders = {'event': EventLoader()}
        if testing_client:

            return testing_client.execute(query, context=request)

        return dict(SCHEMA.execute(query, context_value=request).data)

    def test_get_event(self):
        """Check for eventuality"""
        query = '''{
            event(identifier:"418900971"){
                detail
            }
        }'''
        result = self._get_result(query, False)
        if 'event' in list(result.keys()):
            detail = dict(result['event'])['detail']
            assert detail == 'Integrates unit test'
        assert 'event' in result

    def test_get_events(self):
        """Check for eventualities"""
        query = '''{
            project(projectName:"unittesting") {
                events {
                    detail
                }
            }
        }'''
        result = self._get_result(query, False)
        assert 'events' in result['project']
        detail = dict(result['project']['events'][0])['detail']
        assert len(detail) >= 1

    def test_update_event(self):
        query = '''
        mutation {
          updateEvent(eventId: "418900971", affectation: "0"){
            success
              event {
                accessibility,
                affectation,
                affectedComponents,
                analyst,
                client,
                clientProject,
                eventDate,
                detail,
                evidence,
                id,
                projectName,
                eventStatus,
                eventType
            }
          }
        }
        '''
        testing_client = Client(SCHEMA)
        result = self._get_result(query, testing_client)
        assert 'errors' not in result
        assert result['data']['updateEvent']['event']['eventStatus'] == 'CLOSED'
