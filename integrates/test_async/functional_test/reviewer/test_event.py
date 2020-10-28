import pytest

from test_async.functional_test.reviewer.utils import get_result

pytestmark = pytest.mark.asyncio
 

async def test_event():
    event_id = '540462628'
    group_name = 'unittesting'
    query = f'''{{
        event(identifier: "{event_id}"){{
            id
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
            consulting {{
                content
            }}
            analyst
            __typename
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'event' in result['data']
    assert result['data']['event']['id'] == event_id
    assert result['data']['event']['analyst'] == 'unittest@fluidattacks.com'
    assert result['data']['event']['accessibility'] == 'Repositorio'
    assert result['data']['event']['affectation'] == ''
    assert result['data']['event']['affectedComponents'] == ''
    assert result['data']['event']['client'] == 'Fluid Attacks'
    assert result['data']['event']['closingDate'] == '-'
    assert result['data']['event']['consulting'] == [
        {'content': 'Test customeradmin content'},
        {'content': 'Test executive content'},
    ]
    assert result['data']['event']['context'] == 'FLUID'
    assert result['data']['event']['detail'] == 'test test test'
    assert result['data']['event']['eventDate'] == '2019-04-02 03:02:00'
    assert result['data']['event']['eventStatus'] == 'CREATED'
    assert result['data']['event']['eventType'] == 'HIGH_AVAILABILITY_APPROVAL'
    assert result['data']['event']['evidence'] == ''
    assert result['data']['event']['evidenceFile'] == ''
    assert result['data']['event']['historicState'] == [
        {
            'analyst': 'unittest@fluidattacks.com',
            'date': '2019-04-02 03:02:00',
            'state': 'OPEN'
        },
        {
            'analyst': 'unittest@fluidattacks.com',
            'date': '2019-09-25 09:36:27',
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
    assert len(event['detail']) >= 1

    event_content = 'Test reviewer content'
    query = f'''
        mutation {{
            addEventConsult(eventId: "{event_id}",
                            parent: "0",
                            content: "{event_content}") {{
                success
                commentId
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addEventConsult']
    assert result['data']['addEventConsult']['success']
    assert 'commentId' in result['data']['addEventConsult']

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
            consulting {{
                content
            }}
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'event' in result['data']
    assert result['data']['event']['consulting'] == [
        {'content': 'Test customeradmin content'},
        {'content': 'Test executive content'},
        {'content': event_content}
    ]

    query = f'''{{
        events(projectName: "{group_name}"){{
            id
            projectName
            detail
            consulting {{
                content
            }}
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'events' in result['data']
    events = result['data']['events']
    event = [event for event in events if event['id'] == event_id][0]
    assert event['consulting'] == [
        {'content': 'Test customeradmin content'},
        {'content': 'Test executive content'},
        {'content': event_content}
    ]
