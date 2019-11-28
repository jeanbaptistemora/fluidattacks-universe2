from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphene.test import Client
from jose import jwt
from .test_utils import Request

from app.api.dataloaders.event import EventLoader
from app.api.schema import SCHEMA


class EventTests(TestCase):

    def test_get_event(self):
        """Check for eventuality"""
        query = '''{
            event(identifier:"418900971"){
                detail
            }
        }'''
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'admin',
            'useremail': 'unittest'
        })
        request.loaders = {'event': EventLoader()}
        result = dict(SCHEMA.execute(query, context_value=request).data)
        if 'event' in list(result.keys()):
            detail = dict(result['event'])['detail']
            assert detail == 'Integrates unit test'
        assert 'event' in result

    def test_get_events(self):
        """Check for eventualities"""
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'admin',
            'useremail': 'unittest'
        })
        request.loaders = {'event': EventLoader()}
        query = '''{
            project(projectName:"unittesting") {
                events {
                    detail
                }
            }
        }'''
        result = dict(SCHEMA.execute(query, context_value=request).data)
        assert 'events' in result['project']
        detail = dict(result['project']['events'][0])['detail']
        assert len(detail) >= 1

    def test_update_event(self):
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'admin',
            'useremail': 'unittest'
        })
        request.loaders = {'event': EventLoader()}
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
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert result['data']['updateEvent']['event']['eventStatus'] == 'CLOSED'
