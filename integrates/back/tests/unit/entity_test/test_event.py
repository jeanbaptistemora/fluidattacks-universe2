import os
from datetime import datetime, timedelta
import pytest

from ariadne import graphql_sync, graphql
from jose import jwt
from starlette.datastructures import UploadFile

from backend import util
from backend.api import apply_context_attrs
from backend.api.schema import SCHEMA
from backend.utils import datetime as datetime_utils
from test_unit.utils import create_dummy_session

pytestmark = pytest.mark.asyncio


async def test_event():
    """Check for event."""
    query = '''{
        event(identifier: "418900971"){
            client
            evidence
            projectName
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
            consulting {
                content
            }
            __typename
        }
    }'''
    data = {'query': query}
    request = await create_dummy_session()
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert 'event' in result['data']
    assert result['data']['event']['projectName'] == 'unittesting'
    assert result['data']['event']['detail'] == 'Integrates unit test'

async def test_events():
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
async def test_create_event():
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
async def test_solve_event():
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
async def test_add_event_consult():
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
async def test_update_event_evidence():
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
        uploaded_file = UploadFile(test_file.name, test_file, 'image/gif')
        variables = {
            'eventId': '540462628',
            'evidenceType': 'IMAGE',
            'file': uploaded_file
        }
        data = {'query': query, 'variables': variables}
        request = await create_dummy_session()
        _, result = await graphql(SCHEMA, data, context_value=request)

    assert 'errors' not in result
    assert 'success' in result['data']['updateEventEvidence']

    date_str = datetime_utils.get_as_str(datetime_utils.get_now())
    query = '''
        query GetEvent($eventId: String!) {
            event(identifier: $eventId) {
                evidence
                evidenceDate
            }
        }
    '''
    variables = {'eventId': '540462628'}
    data = {'query': query, 'variables': variables}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert 'errors' not in result
    assert result['data']['event']['evidence'] == (
        'unittesting-540462628-evidence.gif'
    )
    assert result['data']['event']['evidenceDate'].split(' ')[0] == (
        date_str.split(' ')[0]
    )

@pytest.mark.changes_db
async def test_download_event_file():
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
async def test_remove_event_evidence():
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
