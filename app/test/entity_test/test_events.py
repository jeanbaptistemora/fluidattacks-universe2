from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphene.test import Client
from jose import jwt
from .test_utils import Request

from app.api.dataloaders.event import EventLoader
from app.api.schema import SCHEMA
from app.domain import event as event_domain


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

    def test_solve_event(self):
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'admin',
            'useremail': 'unittest'
        })
        query = '''
        mutation {
          solveEvent(
            eventId: "418900971",
            affectation: 0,
            date: "2019-12-02T05:00:00.000Z"
          ) {
            success
          }
        }
        '''
        testing_client = Client(SCHEMA)
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert result['data']['solveEvent']['success']
        event = event_domain.get_event('418900971')
        assert event['historic_state'][-1]['state'] == 'SOLVED'
