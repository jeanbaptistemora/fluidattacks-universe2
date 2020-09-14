import os
from datetime import datetime, timedelta
import pytest

from ariadne import graphql_sync, graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from jose import jwt
from backend import util
from backend.api.dataloaders.event import EventLoader
from backend.api.schema import SCHEMA
from backend.api.dataloaders.event import EventLoader
from test_async.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


class EventTests(TestCase):

    async def test_event(self):
        """Check for event."""
        query = '''{
            event(identifier: "418900971"){
                client
                evidence
                projectName
                clientProject
                eventType
                detail
                eventDate
                eventStatus
                historicState
                affectation
                accessibility
                affectedComponents
                context
                subscription
                evidenceFile
                closingDate
                comments {
                    content
                }
                __typename
            }
        }'''
        data = {'query': query}
        request = await create_dummy_session()
        request.loaders = {
            'event': EventLoader(),
        }
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
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
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'events' in result['data']
        assert result['data']['events'][0]['projectName'] == 'unittesting'
        assert len(result['data']['events'][0]['detail']) >= 1

    @pytest.mark.changes_db
    async def test_create_event(self):
        """Check for createEvent mutation."""
        query = '''
            mutation {
                createEvent(projectName: "unittesting",
                            actionAfterBlocking: TRAINING,
                            actionBeforeBlocking: DOCUMENT_PROJECT,
                            accessibility: ENVIRONMENT,
                            context: CLIENT,
                            detail: "Test",
                            eventDate: "2020-02-01T00:00:00Z",
                            eventType: INCORRECT_MISSING_SUPPLIES) {
                    success
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['createEvent']

    @pytest.mark.changes_db
    async def test_solve_event(self):
        """Check for solveEvent mutation."""
        query = '''
            mutation {
                solveEvent(eventId: "418900971",
                           affectation: "1",
                           date: "2020-02-01T00:00:00Z") {
                    success
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        if 'errors' not in result:
            assert 'errors' not in result
            assert 'success' in result['data']['solveEvent']
        else:
            assert 'The event has already been closed' in result['errors'][0]['message']

    @pytest.mark.changes_db
    async def test_add_event_consult(self):
        """Check for addEventConsult mutation."""
        query = '''
            mutation {
                addEventConsult(eventId: "538745942",
                                parent: "0",
                                content: "Test comment") {
                    success
                    commentId
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session(username='integratesmanager@gmail.com')
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['addEventConsult']
        assert 'commentId' in result['data']['addEventConsult']

    @pytest.mark.changes_db
    async def test_update_event_evidence(self):
        """Check for updateEventEvidence mutation."""
        query = '''
            mutation updateEventEvidence(
                $eventId: String!, $evidenceType: EventEvidenceType!, $file: Upload!
             ) {
                updateEventEvidence(eventId: $eventId,
                                    evidenceType: $evidenceType,
                                    file: $file) {
                    success
                }
            }
        '''
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-anim.gif')
        with open(filename, 'rb') as test_file:
            uploaded_file = SimpleUploadedFile(name=test_file.name,
                                               content=test_file.read(),
                                               content_type='image/gif')
            variables = {
                'eventId': '538745942',
                'evidenceType': 'IMAGE',
                'file': uploaded_file
            }
            data = {'query': query, 'variables': variables}
            request = await create_dummy_session()
            _, result = await graphql(SCHEMA, data, context_value=request)
        if 'errors' not in result:
            assert 'errors' not in result
            assert 'success' in result['data']['updateEventEvidence']
        else:
            pytest.skip("Expected error")

    @pytest.mark.changes_db
    async def test_download_event_file(self):
        """Check for downloadEventFile mutation."""
        query = '''
            mutation {
                downloadEventFile(eventId: "484763304",
                                  fileName: "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad") {
                    success
                    url
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['downloadEventFile']
        assert 'url' in result['data']['downloadEventFile']

    @pytest.mark.changes_db
    async def test_remove_event_evidence(self):
        """Check for removeEventEvidence mutation."""
        query = '''
            mutation {
                removeEventEvidence(eventId: "484763304",
                                    evidenceType: FILE) {
                    success
                }
            }
        '''
        data = {'query': query}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['removeEventEvidence']
