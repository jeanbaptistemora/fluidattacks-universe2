import os
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from backend.utils import datetime as datetime_utils
from test_async.functional_test.resourcer.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_event():
    today = datetime_utils.get_as_str(
        datetime_utils.get_now(),
        date_format='%Y-%m-%d'
    )
    group_name = 'unittesting'
    event_detail = 'resoucer create new event'
    event_date = '2020-01-31 19:00:00'
    event_type = 'INCORRECT_MISSING_SUPPLIES'
    query = f'''
        mutation {{
            createEvent(
                projectName: "{group_name}",
                actionAfterBlocking: TRAINING,
                actionBeforeBlocking: DOCUMENT_PROJECT,
                accessibility: ENVIRONMENT,
                context: CLIENT,
                detail: "{event_detail}",
                eventDate: "2020-02-01T00:00:00Z",
                eventType: {event_type}
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['createEvent']

    query = f'''
        query {{
            project(projectName: "{group_name}"){{
                events {{
                    id
                    analyst
                    detail
                }}
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'events' in result['data']['project']
    events = result['data']['project']['events']
    event = [event for event in events if event['detail'] == event_detail][0]
    event_id = event['id']

    consult_content = 'Test content of new event'
    query = f'''
        mutation {{
            addEventConsult(eventId: "{event_id}",
                            parent: "0",
                            content: "{consult_content}") {{
                success
                commentId
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addEventConsult']
    assert result['data']['addEventConsult']

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
    filename = os.path.join(filename, '../../mock/test-anim.gif')
    with open(filename, 'rb') as test_file:
        uploaded_file = SimpleUploadedFile(name=test_file.name,
                                            content=test_file.read(),
                                            content_type='image/gif')
        variables = {
            'eventId': event_id,
            'evidenceType': 'IMAGE',
            'file': uploaded_file
        }
        data = {'query': query, 'variables': variables}

    result = await get_result(data)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    query = f'''{{
        event(identifier: "{event_id}"){{
            analyst
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
            closingDate
            consulting {{
                content
            }}
            __typename
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'event' in result['data']
    assert result['data']['event']['analyst'] == 'integratesresourcer@fluidattacks.com'
    assert result['data']['event']['accessibility'] == 'Ambiente'
    assert result['data']['event']['affectation'] == ''
    assert result['data']['event']['affectedComponents'] == ''
    assert result['data']['event']['client'] == 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    assert result['data']['event']['closingDate'] == '-'
    assert result['data']['event']['consulting'] == [{'content': consult_content}]
    assert result['data']['event']['context'] == 'CLIENT'
    assert result['data']['event']['detail'] == event_detail
    assert result['data']['event']['eventDate'] == event_date
    assert result['data']['event']['eventStatus'] == 'CREATED'
    assert result['data']['event']['eventType'] == event_type
    assert result['data']['event']['evidence'] == ''
    result['data']['event']['historicState'][1]['date'] = (
        result['data']['event']['historicState'][1]['date'][:-9]
    )
    assert result['data']['event']['historicState'] == [
        {
            'analyst': 'integratesresourcer@fluidattacks.com',
            'date': event_date,
            'state': 'OPEN'
        },
        {
            'analyst': 'integratesresourcer@fluidattacks.com',
            'date': today,
            'state': 'CREATED'
        }
    ]

    assert result['data']['event']['projectName'] == group_name
    assert result['data']['event']['subscription'] == 'CONTINUOUS'

    query = f'''{{
        events(projectName: "{group_name}"){{
            id
            projectName
            detail
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'events' in result['data']
    events = result['data']['events']
    event = [event for event in events if event['id'] == event_id][0]
    assert event['projectName'] == group_name
    assert event['detail'] == event_detail

    query = f'''
        mutation {{
            solveEvent(
                eventId: "{event_id}",
                affectation: "1",
                date: "2020-02-01T00:00:00Z"
            ) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['solveEvent']

    query = f'''
        mutation {{
            removeEventEvidence(eventId: "{event_id}",
                                evidenceType: IMAGE) {{
                success
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    query = f'''
        mutation {{
            downloadEventFile(
                eventId: "{event_id}",
                fileName: "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad"
            ) {{
                success
                url
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['downloadEventFile']
    assert result['data']['downloadEventFile']
    assert 'url' in result['data']['downloadEventFile']

    query = f'''{{
        event(identifier: "{event_id}"){{
            eventStatus
            evidence
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'event' in result['data']
    assert result['data']['event']['eventStatus'] == 'SOLVED'
    assert result['data']['event']['evidence'] == ''

    query = f'''{{
        events(projectName: "{group_name}"){{
            id
            eventStatus
            detail
            evidence
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'events' in result['data']
    events = result['data']['events']
    event = [event for event in events if event['id'] == event_id][0]
    assert event['eventStatus'] == 'SOLVED'
    assert event['evidence'] == ''
